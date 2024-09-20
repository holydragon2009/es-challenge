import logging

import requests
import socketio

from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.errors.http_error import http_error_handler
from app.api.errors.validation_error import http422_error_handler
from app.api.routes.api import router as api_router
from app.core.config import ALLOWED_HOSTS, DEBUG, PROJECT_NAME, VERSION, API_PREFIX
from app.core.events import create_start_app_handler
from app.services.redis import cache

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
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')


@sio.event
def event_ws_received(sid, data, redis_client: cache = Depends(cache)):
    print('message ', data)
    event_type = data["event_type"]
    user_id = data["user_id"]
    quiz_id = data["quiz_id"]

    if event_type == "join_quiz":
        # put(quiz_id, user_id, socket_id) to Redis Hash Table
        redis_client.hset("ws_type", quiz_id, user_id, sid)

        # call to join quiz http api
        res = requests.post(
            url='quiz/{quiz_id}/join',
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        res.raise_for_status()  # Check if the response returned a 4xx or 5xx
        print(
            f"POST Response Status: {res.status_code}, Response Body: {res.text}")
    elif event_type == "get_user_score":
        # get("ws_type", quiz_id, user_id, sid) from Redis Hash Table
        user_score = data["user_score"]
        user_sid = redis_client.hget("ws_type", quiz_id, user_id)

        # emit user's calculated score to client app with sid
        sio.emit(to=user_sid, data=user_score)
    elif event_type == "get_quiz_leaderboard":
        # get all values of ("leaderboard_type", quiz_id, user_id, score) from Redis Hash Table
        user_score = data["user_score"]
        leaderboard_result = redis_client.hget("leaderboard_type", quiz_id)

        # emit user's calculated score to client app with sid
        for item in leaderboard_result:
            user_id = item["user_id"]
            user_sid = redis_client.hget("ws_type", quiz_id, user_id)

            # emit leaderboard of this quiz_id to client app with sid
            sio.emit(to=user_sid, data=leaderboard_result)


@sio.on("connect")
async def connect(sid, env):
    print("New Client Connected to This id :"+" "+str(sid))


@sio.on("disconnect")
async def disconnect(sid):
    print("Client Disconnected: "+" "+str(sid))
