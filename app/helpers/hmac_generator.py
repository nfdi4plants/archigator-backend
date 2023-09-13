import hmac
import hashlib
import json
import urllib.parse
import base64
import jwt
import time

class HmacGenerator:
    def __init__(self, secret: str):
        # self.project_id = project_id
        # self.project_name = project_name
        self.secret = secret.encode("utf-8")

    def base64url(self, data):
        data =  json.dumps(data, separators=(",", ":")).encode("utf-8")
        return base64.urlsafe_b64encode(data).replace(b"=", b"")

    def generate_signature(self, project_id, project_name):
        header_dict = {
            "alg": "HS256",
            "typ": "JWT"
        }

        header = self.base64url(header_dict)

        payload_dict = {
            "project_name": project_name,
            "project_id": project_id
        }

        payload = self.base64url(payload_dict)

        message = header + b"." + payload
        signature = base64.urlsafe_b64encode(hmac.new(key=self.secret, msg=message,
                                                      digestmod=hashlib.sha256).digest()).replace(b"=", b"")

        jwt_token = message + b"." + signature

        return jwt_token

    def generate_order_signature(self, project_id, requests_id):
        header_dict = {
            "alg": "HS256",
            "typ": "JWT"
        }

        header = self.base64url(header_dict)

        payload_dict = {
            "project_id": project_id,
            "request_id": requests_id
        }

        payload = self.base64url(payload_dict)

        message = header + b"." + payload
        signature = base64.urlsafe_b64encode(hmac.new(key=self.secret, msg=message,
                                                      digestmod=hashlib.sha256).digest()).replace(b"=", b"")

        jwt_token = message + b"." + signature

        return jwt_token


    def build_url(self, base_url, *res, **params):
        url = base_url
        for r in res:
            url = '{}/{}'.format(url, r)
        if params:
            url = '{}?{}'.format(url, urllib.parse.urlencode(params))
        return url


    # def decodeJWT(self, token: str) -> dict:
    #     try:
    #         decoded_token = jwt.decode(token, self.secret, algorithms=["HS256"])
    #         return decoded_token if decoded_token["expires"] >= time.time() else None
    #     except:
    #         return {}
