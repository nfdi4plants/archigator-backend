from fastapi import APIRouter

from app.api.endpoints import systemhooks
from app.api.endpoints import status
from app.api.endpoints import setup
from app.api.endpoints import publish
from app.api.endpoints import info
from app.api.endpoints import order
from app.api.endpoints import Mail


api_router = APIRouter(prefix="/api/v1")

# api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhooks"])
api_router.include_router(systemhooks.router, prefix="/hooks", tags=["System Hooks"])
api_router.include_router(status.router, prefix="/status", tags=["Status"])
api_router.include_router(info.router, prefix="/info", tags=["Information"])
api_router.include_router(setup.router, prefix="/setup", tags=["Setup"])
api_router.include_router(publish.router, prefix="/publish", tags=["Publish"])
api_router.include_router(publish.router, prefix="/auth", tags=["Auth"])
api_router.include_router(order.router, prefix="/order", tags=["Order"])

api_router.include_router(order.router, prefix="/mail", tags=["Mail"])
