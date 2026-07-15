from datetime import datetime

from db.db import SessionLocal
from db.models import Request


def save_request(
    *,
    user_id: int | None,
    username: str | None,
    full_name: str | None,
    machine_info: str,
    problem: str,
    table_error: str | None,
    amount: str | None,
    requisites: str | None,
) -> tuple[int, str]:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with SessionLocal() as session:
        request = Request(
            user_id=user_id,
            username=username,
            full_name=full_name,
            machine_info=machine_info,
            problem=problem,
            table_error=table_error,
            amount=amount,
            requisites=requisites,
            created_at=created_at,
        )
        session.add(request)
        session.commit()
        session.refresh(request)

    return request.id, created_at
