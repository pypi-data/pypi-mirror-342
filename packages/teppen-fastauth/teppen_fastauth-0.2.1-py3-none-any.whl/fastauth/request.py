import requests
from .model import User, Users, Organizations, OrganizationDetail
from .env import AUTH_APP_HOST, AUTH_APP_PROTOCOL
from .exceptions import AuthenticationServerException
from typing import List, Optional


def get_user(user_id: int) -> Optional[User]:
    url = f"{AUTH_APP_PROTOCOL}://{AUTH_APP_HOST}/api/users/{user_id}"
    res = requests.get(url)

    if res.status_code >= 500:
        raise AuthenticationServerException("Authentication server error")

    if res.status_code != 200:
        return None

    return User.model_validate(res.json())


def get_users(
    user_ids: Optional[List[int]] = None,
    email: Optional[str] = None,
    only_before_assign: bool = False,
) -> Users:
    url = f"{AUTH_APP_PROTOCOL}://{AUTH_APP_HOST}/api/users"

    query_params = []

    if user_ids is not None:
        for user_id in user_ids:
            query_params.append(f"user_id={user_id}")

    if email is not None:
        query_params.append(f"email={email}")

    if only_before_assign:
        query_params.append("only_before_assign=True")

    if len(query_params) > 0:
        url += "?" + "&".join(query_params)

    res = requests.get(url)

    if res.status_code >= 500:
        raise AuthenticationServerException("Authentication server error")

    return Users.model_validate(res.json())


def get_organization(id: int) -> Optional[dict]:
    url = f"{AUTH_APP_PROTOCOL}://{AUTH_APP_HOST}/api/organizations/{id}"
    res = requests.get(url)

    if res.status_code >= 500:
        raise AuthenticationServerException("Authentication server error")

    if res.status_code != 200:
        return None

    return OrganizationDetail.model_validate(res.json())


def get_organizations() -> dict:
    url = f"{AUTH_APP_PROTOCOL}://{AUTH_APP_HOST}/api/organizations"
    res = requests.get(url)

    if res.status_code >= 500:
        raise AuthenticationServerException("Authentication server error")

    return Organizations.model_validate(res.json())
