import os

JWKS_ENDPOINT = os.getenv("JWKS_ENDPOINT")
JWT_ALGORITHM = "RS256"
HOST_RESOURCE_APP = os.getenv("HOST_RESOURCE_APP")

if JWKS_ENDPOINT is None:
    raise Exception("環境変数 JWKS_ENDPOINT は必須です。")

if HOST_RESOURCE_APP is None:
    raise Exception("環境変数 HOST_RESOURCE_APP は必須です。")

JWT_AUDIENCE = []

if "://" in HOST_RESOURCE_APP:
    JWT_AUDIENCE.append(HOST_RESOURCE_APP)
    JWT_AUDIENCE.append(HOST_RESOURCE_APP.split("://")[1])
else:
    JWT_AUDIENCE.append(HOST_RESOURCE_APP)
    JWT_AUDIENCE.append(f"http://{HOST_RESOURCE_APP}")
    JWT_AUDIENCE.append(f"https://{HOST_RESOURCE_APP}")

AUTH_APP_HOST = JWKS_ENDPOINT.split("/")[2]
AUTH_APP_PROTOCOL = JWKS_ENDPOINT.split(":")[0]

os.environ["NO_PROXY"] = AUTH_APP_HOST
