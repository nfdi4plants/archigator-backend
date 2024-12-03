import jwt
import os

from fastapi import APIRouter, Body, Depends, HTTPException, status, Response, Request, Header
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


from app.gitlab.api import Gitlab_API
from app.invenio.api import Invenio_API
from app.api.models.status_response import StatusResponse, Gituser, ProjectPipeline, UserProject, Test, Tests, Receipt
from app.api.models.jw_token import JwtToken, OrderToken

router = APIRouter()



@router.get("/id/{order_token}", summary="Receipt information", status_code=status.HTTP_200_OK,
            responses={200: {"model": Receipt}, 500: {"model": Receipt}})
            # dependencies=[Depends(JWTBearer())])
async def receipt(order_token: str):
    """
    :param order_token: The token for the order to retrieve the receipt information.
    :return: The receipt information for the given order token.

    This method retrieves the receipt information for a given order token. It decodes the token, retrieves the project and request details from external APIs, and creates a receipt object
    * with the relevant information. The receipt object is then returned as a JSON response.

    Example usage:
        receipt("sample_token")
    """
    try:
        print("publication", order_token)
        # scheme, token = publication.split(" ")
        # print("scheme", scheme)
        # print("token", token)
        # if scheme.lower() != "token":
        #     raise HTTPException(status_code=401, detail="Invalid authentication scheme.")
        decoded_token = jwt.decode(order_token, os.getenv("ARCHIGATOR_SECRET"), algorithms=["HS256"])
        print("dec token", decoded_token)
        jwt_token = OrderToken(**decoded_token)
        print("jwtr ", jwt_token)
    except (ValueError, jwt.exceptions.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token.")

    print("getting receipt")
    gitlab_api = Gitlab_API()
    invenio_api = Invenio_API()

    # if jwt_token.project_id is None:
    #     return HTTPException(status_code=404)

    try:
        # project = gitlab_api.get_project(jwt_token.project_id)
        project = gitlab_api.get_project(jwt_token.project_id)
        print("project", project)
    except:
        project = None

    try:
        print("trying getting request")
        print("jwt token", jwt_token)
        review = invenio_api.get_request(jwt_token.request_id)
        print("review", review)
        # review = invenio_api.get_request("71d0aa32-472b-4fb1-bcf3-6a85bdbcc162")

    except:
        review = Request()

    try:
        comments = invenio_api.get_comments(jwt_token.request_id)
    except:
        comments = []

    try:
        receipt = Receipt(status=review.status, web_url=project.web_url, investigation_name=review.title, comments=comments, order_id=review.id)
    except:
        receipt = Receipt()

    # response_json = jsonable_encoder(response)
    response_json = jsonable_encoder(receipt)

    return JSONResponse(response_json)