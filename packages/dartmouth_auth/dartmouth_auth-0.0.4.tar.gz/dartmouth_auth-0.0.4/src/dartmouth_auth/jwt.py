"""JWT management"""

import requests

import os

from dartmouth_auth.definitions import ENV_NAMES, JWT_URL


def get_jwt(dartmouth_api_key: str = None, jwt_url: str = None) -> str | None:
    """Obtain a JSON Web Token

    :param dartmouth_api_key: A Dartmouth API key. If set to None, will try to use environment variable DARTMOUTH_API_KEY. Defaults to None
    :type dartmouth_api_key: str, optional
    :param jwt_url: he URL of the endpoint returning the JWT. If set to None, defaults to "https://api.dartmouth.edu/api/jwt". Defaults to None
    :type jwt_url: str, optional
    :raises ValueError: No API key is provided and no environment variable DARTMOUTH_API_KEY can be found.
    :return: A JWT if the API key was valid, else None.
    :rtype: str | None
    """
    if jwt_url is None:
        jwt_url = JWT_URL
    if dartmouth_api_key is None:
        dartmouth_api_key = os.getenv(ENV_NAMES["dartmouth_api_key"])
    if dartmouth_api_key:
        r = requests.post(
            url=jwt_url,
            headers={"Authorization": dartmouth_api_key},
        )
        try:
            jwt = r.json()
            jwt = jwt["jwt"]
            return jwt
        except Exception:
            raise KeyError("Could not authenticate. Is your Dartmouth API key valid?")
    raise KeyError(
        f"Dartmouth API key not provided as argument or defined as environment variable {ENV_NAMES['dartmouth_api_key']}."
    )


if __name__ == "__main__":
    print(get_jwt())
