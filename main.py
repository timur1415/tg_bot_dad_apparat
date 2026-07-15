import logging
from bot_init import create_application
from db.db import init_db


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    init_db()
    application = create_application()

    application.run_polling()
