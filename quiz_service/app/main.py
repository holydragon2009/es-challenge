import logging

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.api.routes.organizations import cronjob_sync_organizations
from app.core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, VERSION, API_PREFIX
from app.core.events import create_start_app_handler
from app.db.db import engine
from app.db.repositories.organization_repository import OrganizationRepository
from app.db.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    # application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)

    logging.info("get_application start...")

    return application


app = get_application()


@app.on_event("startup")
@repeat_every(seconds=60 * 60, logger=logger, wait_first=True)  # every 1 hour
async def run_cronjob_sync_organizations_periodically():
    async with AsyncSession(engine) as session:
        organization_repo = OrganizationRepository(session=session)
        user_repo = UserRepository(session=session)
        await cronjob_sync_organizations(organization_repo=organization_repo, user_repo=user_repo)


