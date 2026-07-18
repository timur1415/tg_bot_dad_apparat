import logging

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel

from db.db import SessionLocal
from db.models import Request as RequestModel

router = APIRouter(prefix="/api/admin", tags=["admin"])
logger = logging.getLogger(__name__)

ALLOWED_STATUSES = {"new", "in_progress", "waiting", "resolved"}


class RequestStatusPatch(BaseModel):
    status: str


@router.get("/requests")
async def list_requests():
    with SessionLocal() as session:
        records = session.query(RequestModel).order_by(RequestModel.id.desc()).all()

    return [
        {
            "id": record.id,
            "user_id": record.user_id,
            "username": record.username,
            "full_name": record.full_name,
            "machine_info": record.machine_info,
            "problem": record.problem,
            "table_error": record.table_error,
            "amount": record.amount,
            "requisites": record.requisites,
            "photo_file_id": record.photo_file_id,
            "status": record.status,
            "created_at": record.created_at,
        }
        for record in records
    ]


@router.get("/requests/{request_id}/photo")
async def get_request_photo(request_id: int, request: Request):
    with SessionLocal() as session:
        record = session.get(RequestModel, request_id)
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )
        if not record.photo_file_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Photo not found",
            )

    try:
        telegram_file = await request.app.state.bot_app.bot.get_file(record.photo_file_id)
        photo_bytes = await telegram_file.download_as_bytearray()
    except Exception as exc:
        logger.exception("Failed to load photo for request_id=%s", request_id)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Failed to fetch photo from Telegram",
        ) from exc

    return Response(content=bytes(photo_bytes), media_type="image/jpeg")


@router.patch("/requests/{request_id}")
async def update_request_status(request_id: int, payload: RequestStatusPatch):
    if payload.status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported status",
        )

    with SessionLocal() as session:
        record = session.get(RequestModel, request_id)
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Request not found",
            )

        record.status = payload.status
        session.commit()

    return {"ok": True}
