import logging

from fastapi import APIRouter, Request, Response, status
from fastapi.responses import FileResponse
from telegram import Update

from config.config import SECRET_TOKEN


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    if SECRET_TOKEN:
        header_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if header_token != SECRET_TOKEN:
            logger.warning("Forbidden: invalid secret token header")
            return Response(status_code=status.HTTP_403_FORBIDDEN)

    try:
        payload = await request.json()
    except Exception:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    update = Update.de_json(payload, request.app.state.bot_app.bot)
    
    await request.app.state.bot_app.update_queue.put(update)
    return Response(status_code=status.HTTP_200_OK)

@router.get('/app')
async def start_web_app(request: Request):
    return FileResponse(path='templates/index.html')