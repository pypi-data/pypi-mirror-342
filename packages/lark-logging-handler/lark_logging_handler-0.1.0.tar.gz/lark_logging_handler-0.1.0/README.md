# Lark Logging Handler

A Python logging handler that sends log messages to Lark (Feishu) as beautiful interactive cards.

## Features

- Sends log messages to Lark users or chat groups
- Renders logs as interactive cards with colored headers based on log level
- Supports asynchronous message delivery (non-blocking)
- Configurable notification threshold (only send warnings/errors by default)
- Force notifications for specific log messages regardless of level
- Add custom metadata fields to enhance your log messages

## Quick Start

```python
import logging
from lark_logging import LarkHandler, Subscriber

# Create logger and handler
logger = logging.getLogger("MyApp")
handler = LarkHandler(
    app_id="YOUR_APP_ID",
    app_secret="YOUR_APP_SECRET",
    subscribers=[
        # Send to email, chat, or user IDs
        Subscriber("email", "user@example.com"),
        Subscriber("chat_id", "oc_abcdef123456")
    ]
)

# Add handler to logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Use the logger
logger.info("System started successfully")
logger.warning("Low disk space detected")
logger.error("Database connection failed")

# Send low-level logs with force notification
logger.debug("Important debug info", extra={"notify": True})

# Add custom fields to your logs
logger.warning("Task failed", extra={
    "task": "data_sync",
    "component": "auth_service",
    "retry_count": 3
})

# For scripts, wait for messages to be sent (not needed for services)
handler.flush_and_wait(timeout=5)
```

## Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `app_id` | Lark application App ID | Required |
| `app_secret` | Lark application App Secret | Required |
| `subscribers` | List of message recipients | `[]` |
| `level` | Minimum log level to capture | `logging.NOTSET` |
| `notification_level` | Minimum level to send to Lark | `logging.WARNING` |
| `queue_size` | Max size of async message queue | `100` |
