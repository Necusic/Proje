from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional
import uuid


class UserStatus(Enum):
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    DELETED = "Deleted"


class NotificationType(Enum):
    MESSAGE = "Message"
    INVITE = "Invite"
    SYSTEM = "System"


@dataclass
class Message:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    sent_at: datetime = field(default_factory=datetime.utcnow)
    edited_at: Optional[datetime] = None
    is_deleted: bool = False

    def edit(self, new_text: Optional[str] = None) -> None:
        self.edited_at = datetime.utcnow()
        if isinstance(self, TextMessage) and new_text is not None:
            self.text = new_text
        if isinstance(self, ImageMessage) and new_text is not None:
            self.caption = new_text

    def delete(self) -> None:
        self.is_deleted = True


@dataclass
class TextMessage(Message):
    text: str = ""


@dataclass
class ImageMessage(Message):
    image_id: uuid.UUID = field(default_factory=uuid.uuid4)
    caption: str = ""


@dataclass
class Attachment:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    file_type: str = ""


@dataclass
class MediaFile:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    url: str = ""
    thumbnail_url: str = ""
    mime_type: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    size_bytes: int = 0


@dataclass
class Chat:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_message_at: Optional[datetime] = None
    messages: List[Message] = field(default_factory=list)

    def send_message(self, message: Message) -> None:
        self.messages.append(message)
        self.last_message_at = message.sent_at


@dataclass
class PrivateChat(Chat):
    user1_id: uuid.UUID = field(default_factory=uuid.uuid4)
    user2_id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GroupChat(Chat):
    title: str = ""
    description: str = ""
    avatar_url: str = ""
    member_ids: List[uuid.UUID] = field(default_factory=list)

    def add_member(self, user_id: uuid.UUID) -> None:
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)

    def remove_member(self, user_id: uuid.UUID) -> None:
        if user_id in self.member_ids:
            self.member_ids.remove(user_id)


@dataclass
class User:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    last_active_at: datetime = field(default_factory=datetime.utcnow)
    username: str = ""
    password_hash: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: UserStatus = UserStatus.ACTIVE

    def set_status(self, status: UserStatus) -> None:
        self.status = status

    def touch(self) -> None:
        self.last_active_at = datetime.utcnow()


@dataclass
class Session:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = field(default_factory=uuid.uuid4)
    access_token: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=1))
    is_active: bool = True

    def validate(self) -> bool:
        if not self.is_active:
            return False
        if datetime.utcnow() >= self.expires_at:
            self.is_active = False
            return False
        return True

    def terminate(self) -> None:
        self.is_active = False


@dataclass
class Authentication:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    success: bool = False
    user_id: Optional[uuid.UUID] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Notification:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    notification_type: NotificationType = NotificationType.SYSTEM
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_read: bool = False

    def mark_read(self) -> None:
        self.is_read = True
