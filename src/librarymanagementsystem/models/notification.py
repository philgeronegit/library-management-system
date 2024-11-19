import uuid
from datetime import datetime


class Notification:
    def __init__(
        self,
        type: str,
        content: str,
        date_notification: datetime,
        user_id: int,
        id: int = None,
    ):
        self.id = id or int(uuid.uuid4())
        self.type = type
        self.content = content
        self.date_notification = date_notification
        self.user_id = user_id

    def __str__(self):
        return f"Notification(type={self.type}, contenu={self.content}, date={self.date_notification} user_id={self.user_id})"
