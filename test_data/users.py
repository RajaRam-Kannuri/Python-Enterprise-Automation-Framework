import os

from core.models.user import LabsUser, TeamRoles, TestRoles, User

DEFAULT_PASSWORD = "Pass123$"

PROD_USERS = {
    "all_roles": User(
        email="alice@company.com",
        password="WV8cjtp*j6ZLf!",
    ),
    "platform_lab_user": User(
        email="jane@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.ADMIN, TestRoles.LEARNER, TestRoles.INSTRUCTOR, TestRoles.AUTHOR},
    ),
}


DEFAULT_LABS_USERS = {
    "labs_internal_user": LabsUser(
        email="autotest@alemira.dev",
        password="N89wzbzr1RNi7xmKX2tCrbc0",
        organization_name=os.environ.get("ORGANIZATION", "Primary Demo"),
    ),
    "labs_user_for_lms": LabsUser(
        email="ungzese@example.com",
        password="N89wzbzr1RNi7xmKX2tCrbc0",
        organization_name=os.environ.get("ORGANIZATION", "Autotest"),
    ),
}

DEFAULT_DOMAIN_USERS = {
    "all_roles": User(
        email="zara@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.ADMIN, TestRoles.LEARNER, TestRoles.INSTRUCTOR, TestRoles.AUTHOR},
        team_roles={TeamRoles.LEAD, TeamRoles.CONTRIBUTOR, TeamRoles.REVIEWER},
    ),
    "admin": User(
        email="debugautoadmin01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.ADMIN},
        team_roles={TeamRoles.LEAD},
    ),
    "learner": User(
        email="autolearner01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.LEARNER},
    ),
    "instructor": User(
        email="autoinstructor01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.INSTRUCTOR},
    ),
    "author": User(
        email="autoauthor01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.AUTHOR},
        team_roles={TeamRoles.CONTRIBUTOR},
    ),
    "platform_lab_user": User(
        email="jane@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.ADMIN, TestRoles.LEARNER, TestRoles.INSTRUCTOR, TestRoles.AUTHOR},
    ),
}

CUSTOM_DOMAIN_USERS = {
    "admin": User(
        email="customautoadmin01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.ADMIN},
        team_roles={TeamRoles.LEAD},
    ),
    "learner": User(
        email="customautolearner01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.LEARNER},
    ),
    "instructor": User(
        email="customautoinstructor01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.INSTRUCTOR},
    ),
    "author": User(
        email="customautoauthor01@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.AUTHOR},
        team_roles={TeamRoles.CONTRIBUTOR},
    ),
    "platform_lab_user": User(
        email="customjane@company.com",
        password=DEFAULT_PASSWORD,
        roles={TestRoles.ADMIN, TestRoles.LEARNER, TestRoles.INSTRUCTOR, TestRoles.AUTHOR},
        team_roles={TeamRoles.LEAD, TeamRoles.CONTRIBUTOR, TeamRoles.REVIEWER},
    ),
}
