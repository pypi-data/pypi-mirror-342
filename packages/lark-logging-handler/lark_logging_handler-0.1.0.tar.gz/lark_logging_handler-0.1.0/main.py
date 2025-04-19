import logging

from lark_logging_handler import LarkHandler, Subscriber

# 创建日志实例
logger = logging.getLogger("Lark")
# 创建飞书处理器
lark_handler = LarkHandler(
    app_id="YOUR_APP_ID",
    app_secret="YOUR_APP_SECRET",
    subscribers=[
        Subscriber("email", "gtoxlili@outlook.com")
    ],
    level=logging.DEBUG,
    notification_level=logging.WARNING,
)
# 注册处理器
logger.addHandler(lark_handler)

if __name__ == '__main__':
    # 使用日志
    logger.info("这是普通信息, 不会发给飞书")
    logger.warning("这是警告消息，会发送到飞书")
    logger.error("这是错误消息，会发送到飞书")
    logger.debug("这是调试消息，不会发送到飞书")

    # 强制推送
    logger.debug("这是调试消息，会发送到飞书", extra={
        "notify": True
    })

    # 带额外信息的日志
    logger.info("任务执行失败", extra={
        "task": "数据同步",
        "component": "用户服务",
        "error": "连接超时",
        "notify": True  # 强制发送通知
    })

    # 因为发送日志行为采用异步发送
    # 这里只是为了保证请求能发送完成，实际场景下并不需要 wait
    lark_handler.flush_and_wait(timeout=5)
