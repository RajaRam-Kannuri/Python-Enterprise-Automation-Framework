from requests import Session

from core.api.auth import authorization_ways
from core.models.user import User
from settings import settings
from util.api.allure_reporting import record_response


class SessionManager:
    def __init__(self):
        self.__sessions = {}

    def get_session(self, user_key: str) -> Session:
        user = settings.stand_config.users.get(user_key, None)
        if user_key not in self.__sessions.keys():
            session = Session()
            session.hooks["response"].append(record_response)
            appropriate_auth_function = authorization_ways[type(user)]
            appropriate_auth_function(session=session, user=user)
            self.__sessions[user_key] = session
        return self.__sessions[user_key]

    def get_user_key_by_session(self, session: Session) -> str | None:
        for key, value in self.__sessions.items():
            if session is value:
                return key
        return None

    def get_user_by_session(self, session: Session) -> User:
        user_key = self.get_user_key_by_session(session)
        if not user_key:
            raise RuntimeError("No user associated with this session")

        user = settings.stand_config.users.get(user_key, None)
        if not user:
            raise RuntimeError("Unknown user for session")

        return user
