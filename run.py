import copy
import logging

import uvicorn
from uvicorn.config import LOGGING_CONFIG

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S',
)


class RenameUvicornErrorFilter(logging.Filter):
    """
    Filtro para renomear o logger 'uvicorn.error' para 'uvicorn.server' para mensagens informativas.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Renomeia o logger 'uvicorn.error' para 'uvicorn.server' para mensagens informativas.
        """
        if record.name == "uvicorn.error" and record.levelno < logging.WARNING:
            record.name = "uvicorn.server"
        return True


LOG_CONFIG = copy.deepcopy(LOGGING_CONFIG)

LOG_CONFIG.setdefault("filters", {})
LOG_CONFIG["filters"]["rename_uvicorn"] = {"()": "__main__.RenameUvicornErrorFilter"}

for handler_name in ("default", "error"):
    if handler_name in LOG_CONFIG.get("handlers", {}):
        LOG_CONFIG["handlers"][handler_name].setdefault("filters", []).append("rename_uvicorn")

LOG_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
LOG_CONFIG["formatters"]["default"]["datefmt"] = "%Y-%m-%d %H:%M:%S"
LOG_CONFIG["formatters"]["access"][
    "fmt"] = "%(asctime)s | %(levelname)s | %(client_addr)s | %(request_line)s | %(status_code)s"
LOG_CONFIG["formatters"]["access"]["datefmt"] = "%Y-%m-%d %H:%M:%S"

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        use_colors=True,
        reload=True,
        # log_config=LOG_CONFIG,
        # log_level='trace',
        # workers=4,
    )
