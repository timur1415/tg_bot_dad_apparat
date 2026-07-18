from contextlib import asynccontextmanager

from fastapi import FastAPI
from telegram import Update

from bot_init import create_application
from config.config import SECRET_TOKEN, TELEGRAM_WEBHOOK_PATH, WEBHOOK_URL
from db.db import init_db
from server.router.admin_router import router as admin_router
from server.router.telegram_router import router as telegram_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    application = create_application()

    app.state.bot_app = application

    await application.initialize()
    await application.start()
    if WEBHOOK_URL:
        await application.bot.set_webhook(
            url=WEBHOOK_URL + TELEGRAM_WEBHOOK_PATH,
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            secret_token=SECRET_TOKEN,
        )

    yield

    try:
        await application.bot.delete_webhook()
    finally:
        await application.stop()
        await application.shutdown()



def init_fastapi_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(telegram_router)
    app.include_router(admin_router)

    return app


app = init_fastapi_app()