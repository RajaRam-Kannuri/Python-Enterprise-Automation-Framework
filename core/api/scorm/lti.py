from bs4 import BeautifulSoup
from requests import Session

from core.api.auth import emulate_login
from core.api.lms.objective_workflow import ObjectiveWorkflow
from core.api.scorm.attempts import AttemptsApi
from core.models.lms.activity_part import ActivityPart
from core.models.lms.activity_workflow_aggregate import ActivityWorkflow
from core.models.lti.launch import LaunchForm
from core.models.lti.lti_resource_library import LtiResourceInitModel, LtiResourceLinkModel
from core.models.scorm.attempts import Adl, CreateExitAttempt, Nav
from core.models.user import User
from settings import settings
from util.helpers import extract_value_from_html, get_query_parameter


def get_resource_launch_id(session: Session, lti_form: LtiResourceInitModel, user: User) -> str:
    login_response = emulate_login(session, user, login_form_url=lti_form.auth_uri, login_form_data=lti_form.dict())

    form = BeautifulSoup(login_response.text, "html.parser").find("form")
    launch_action_url = form.get("action")
    launch_form = LaunchForm(
        id_token=extract_value_from_html(form, "id_token"),
        scope=extract_value_from_html(form, "scope"),
        state=extract_value_from_html(form, "state"),
        session_state=extract_value_from_html(form, "session_state"),
    )

    launch_id = _launch_resource(launch_action_url, launch_form, session)
    return launch_id


def resource_launch_id_from_activity(
    learner_session: Session,
    objective_workflow: ObjectiveWorkflow,
    composite_activity_workflow: ActivityWorkflow,
    activity_workflow: ActivityWorkflow,
    activity_part: ActivityPart,
) -> str:
    payload = LtiResourceLinkModel(
        activity_workflow_ids=[composite_activity_workflow.id, activity_workflow.id],
        activity_part_ids=[activity_part.id],
    )
    lti_form = objective_workflow.get_lti_form(payload)

    return get_resource_launch_id(learner_session, lti_form, settings.stand_config.platform_users.get("learner"))


def lti_exit_attempt(
    session: Session,
    resource_launch_id: str,
    activity_workflow: ActivityWorkflow,
):
    attempts_api = AttemptsApi(session)
    payload = CreateExitAttempt(adl=Adl(nav=Nav(request="exitAll")))
    attempts_api.exit_attempts(payload, resource_launch_id, activity_workflow.id)


def _launch_resource(launch_action_url: str, launch_body: LaunchForm, session: Session) -> str:
    launch_response = session.post(launch_action_url, data=launch_body.dict(), allow_redirects=False)

    if not launch_response.ok:
        raise ValueError("Failed to launch resource.")

    location = launch_response.headers.get("Location")
    launch_id = get_query_parameter(location, "resourceLaunchId")

    return launch_id
