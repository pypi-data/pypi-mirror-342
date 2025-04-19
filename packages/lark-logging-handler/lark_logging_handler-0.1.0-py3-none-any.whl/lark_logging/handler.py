import logging
import threading
import queue
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any
from .models import Subscriber
from .utils import _build_log_card_message, BuildResult

import lark_oapi as lark
from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody

class LarkHandler(logging.Handler):

    def __init__(self, app_id: str, app_secret: str, subscribers: List[Subscriber] = None,
                 level: int = logging.NOTSET,
                 notification_level: int = logging.WARNING,
                 queue_size: int = 100):
        """
        初始化飞书日志处理器
        :param app_id: 飞书应用的App ID
        :param app_secret: 飞书应用的App Secret
        :param subscribers: 订阅者列表
        :param level: 日志级别
        :param notification_level: 发送通知的日志级别
        :param queue_size: 队列大小
        """
        super().__init__(level=level)
        self.subscribers = subscribers or []
        self.app_id = app_id
        self.app_secret = app_secret
        self.notification_level = notification_level

        self.client = lark.Client.builder() \
            .app_id(app_id) \
            .app_secret(app_secret) \
            .log_level(lark.LogLevel(level)) \
            .build()

        # 创建消息队列和处理线程
        self.message_queue = queue.Queue(maxsize=queue_size)
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def flush_and_wait(self, timeout=None):
        """
        等待所有待处理的日志消息被发送完成。

        此方法主要用于短时运行的脚本或示例程序中，确保在程序退出前所有日志消息都被处理。
        在长期运行的应用程序或服务中通常不需要调用此方法。

        :param timeout: 最大等待时间(秒)，None表示无限等待
        :return: None
        """
        self.worker_thread.join(timeout)

    def emit(self, record: logging.LogRecord):
        """处理日志记录"""
        try:
            # 构造日志数据
            log_data = self._prepare_log_data(record)

            # 将日志放入队列
            try:
                self.message_queue.put(log_data, block=False)
            except queue.Full:
                self.handleError(record)
        except Exception:
            self.handleError(record)

    def _prepare_log_data(self, record: logging.LogRecord) -> Dict[str, Any]:
        extra_data = {}
        for key, value in record.__dict__.items():
            if key not in {
                'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
                'funcName', 'id', 'levelname', 'levelno', 'lineno', 'module',
                'msecs', 'message', 'msg', 'pathname', 'process',
                'processName', 'relativeCreated', 'stack_info', 'thread', 'threadName', 'taskName'
            }:
                extra_data[key] = value

        # 构造通用字段
        log_data: Dict[str, Any] = {
            "level": record.levelno,
            "time": datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S'),
            "message": self.format(record),
            **extra_data
        }

        # 默认只有警告以上级别才发送通知
        if "notify" not in log_data:
            log_data["notify"] = record.levelno >= logging.WARNING

        return log_data

    def _process_queue(self):
        """处理消息队列"""
        while True:
            try:

                log_data = self.message_queue.get(block=True)

                level = log_data.get("level", logging.NOTSET)

                should_send = True
                if level < self.notification_level:
                    should_send = log_data.get("notify", False)

                if not should_send:
                    self.message_queue.task_done()
                    continue

                content = _build_log_card_message(log_data)

                # 发送给所有订阅者
                for subscriber in self.subscribers:
                    try:
                        self._send_rich_message(subscriber, content)
                    except Exception as e:
                        print(f"发送消息失败: {e}")

                self.message_queue.task_done()
            except Exception as e:
                print(f"处理日志队列出错: {e}")

            # 避免CPU占用过高
            time.sleep(0.1)

    def _send_rich_message(self, subscriber: Subscriber, content: BuildResult):
        """发送富文本消息到飞书"""
        req = CreateMessageRequest.builder() \
            .request_body(CreateMessageRequestBody.builder()
                          .receive_id(subscriber.id_value)
                          .msg_type(content["msg_type"])
                          .content(content["content"])
                          .uuid(str(uuid.uuid4()))
                          .build()) \
            .receive_id_type(subscriber.id_type) \
            .build()

        resp = self.client.im.v1.message.create(req)
        if not resp.success():
            print(f"发送消息失败: {resp.code} {resp.msg}")
            return
