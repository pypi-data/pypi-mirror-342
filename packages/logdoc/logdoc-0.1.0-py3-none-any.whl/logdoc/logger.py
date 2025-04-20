# logdoc/logger.py
import json
import logging
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

def log_event(action: str, context: dict = None):
    entry = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S"),

        "action": action,
        "context": context or {}
    }
    print(json.dumps(entry))
