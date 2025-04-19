class Subscriber:
    """飞书消息订阅者"""

    def __init__(self, id_type: str, id_value: str):
        """
        初始化订阅者
        :param id_type: 接收者类型，可以是 "open_id", "user_id", "union_id", "chat_id", "email"
        :param id_value: 接收者ID值
        """
        self.id_type = id_type
        self.id_value = id_value
