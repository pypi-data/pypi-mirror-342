from auth0.authentication import GetToken
from auth0.management import Auth0
from d4k_ms_base.service_environment import ServiceEnvironment


class Auth0Management:
    def __init__(self) -> None:
        se = ServiceEnvironment()
        self._domain = se.get("AUTH0_DOMAIN")
        self._client_id = se.get("AUTH0_MNGT_CLIENT_ID")
        self._client_secret = se.get("AUTH0_MNGT_CLIENT_SECRET")
        self._auth0 = None

    def token(self):
        get_token = GetToken(self._domain, self._client_id, self._client_secret)
        token = get_token.client_credentials(f"https://{self._domain}/api/v2/")
        self._auth0 = Auth0(self._domain, token["access_token"])

    def user_list(self) -> list:
        try:
            return self._auth0.users.list()
        except Auth0.exceptions.Auth0Error as e:
            self.token()
            return self._auth0.users.list()

    def user_roles(self, id: str) -> list:
        try:
            return self._auth0.users.list_roles(id)
        except Auth0.exceptions.Auth0Error as e:
            self.token() 
            return self._auth0.users.list_roles(id)
