import json
import os
import requests
import jwt


from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, HTTPBearer
from starlette.status import (
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR
)

load_dotenv()

KEYCLOAK_ISSUER = os.environ.get("OAUTH_ISSUER", "https://auth.nfdi4plants.org")
KEYCLOAK_PUBLIC_KEY_URL = f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"
KEYCLOAK_CLIENT_ID = "account"

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=os.getenv("OAUTH_ISSUER"))

# oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token")

oauth2_scheme = HTTPBearer()

async def fetch_public_key():
    response = requests.get(KEYCLOAK_PUBLIC_KEY_URL)
    response.raise_for_status()

    public_keys = []
    jwk_set = response.json()
    for key_dict in jwk_set["keys"]:
        print("key=", key_dict)
        print("algorithm", key_dict["alg"])
        if key_dict["alg"].lower() == os.getenv("OAUTH_ALGORITHM", "RS256").lower():
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key_dict))
            public_keys.append(public_key)
        print("pub key is", public_keys)


    return public_keys

    # print("resp", response.json())
    #
    # return response.json()["keys"][1]["x5c"][0]
    # return response.json()["keys"][0]

async def validate_access_token(token: dict = Depends(oauth2_scheme)):
    print("type", type(token))
    try:
        print("this is my token", token.credentials)
        public_keys = await fetch_public_key()
        print("pub key", public_keys)

        for key in public_keys:

            print("key===", key)


            decoded_token = jwt.decode(token.credentials, key, algorithms=["RS256"], audience=KEYCLOAK_CLIENT_ID)
        print("decoded token", decoded_token)

        return decoded_token

        # if not valid_token:
        #     raise HTTPException(status_code=401, detail="Invalid access token")

    except Exception as e:
        print("error decoding token", e)
        raise HTTPException(status_code=401, detail="Invalid Access Token")