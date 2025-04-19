from typing import Dict, List, Optional, Union, Any, TypedDict as PyTypedDict, cast
from typing_extensions import TypedDict, Literal, NotRequired
from enum import Enum

def to_dict(obj):
    """Convert a TypedDict instance to a dictionary."""
    if isinstance(obj, (list, tuple)):
        return [to_dict(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: to_dict(v) for k, v in obj.items()}
    else:
        return obj

# Basic Types

class ContactType(str, Enum):
    """
    Represents the type of contact: either an individual user or a group chat.
    """
    PRIVATE = "private"
    GROUP = "group"

class EventType(str, Enum):
    """
    Represents types of events that can be received.
    """
    CHAT_MESSAGE = "chat-message"
    COMMAND_RESULT = "command-result"

class ContentType(str, Enum):
    """
    Represents types of content in messages.
    """
    TEXT = "text"
    LIST = "list"
    IMAGE = "image"
    AUDIO = "audio"
    CARD = "card"

# TypedDict definitions for structured data

class ImageData(TypedDict):
    """
    Image data structure.
    """
    url: str

class AudioData(TypedDict):
    """
    Audio data structure.
    """
    url: str
    duration: int

class ThumbData(TypedDict):
    """
    Thumbnail image data structure.
    """
    url: str

class CardData(TypedDict):
    """
    Card data structure.
    """
    title: str
    digest: str
    url: str
    thumb: ThumbData

# Content item definitions

class ChatMessageContentItemText(TypedDict):
    """
    Represents a text item in rich content.
    """
    type: Literal["text"]
    text: str

class ChatMessageContentItemImage(TypedDict):
    """
    Represents an image item in rich content.
    """
    type: Literal["image"]
    image: ImageData

class ChatMessageContentItemAudio(TypedDict):
    """
    Represents an audio item in rich content.
    """
    type: Literal["audio"]
    audio: AudioData

class ChatMessageContentItemCard(TypedDict):
    """
    Represents a card item in rich content.
    """
    type: Literal["card"]
    card: CardData

ChatMessageContentItemUnion = Union[
    ChatMessageContentItemText,
    ChatMessageContentItemImage,
    ChatMessageContentItemAudio,
    ChatMessageContentItemCard,
]

# Message content definitions

class ChatMessagePlainContent(TypedDict):
    """
    Represents plain text content in a chat message.
    """
    type: Literal["text"]
    text: str

class ChatMessageRichContent(TypedDict):
    """
    Represents rich content consisting of multiple content items in a chat message.
    """
    type: Literal["list"]
    list: List[ChatMessageContentItemUnion]

ChatMessageContentUnion = Union[ChatMessagePlainContent, ChatMessageRichContent]

# Event data definitions

class ChatMessagePayload(TypedDict):
    """
    Represents the payload for a chat message event.
    """
    contactType: ContactType
    contactID: str
    messageID: str
    senderID: str
    senderName: Optional[str]
    content: ChatMessageContentUnion
    mentioned: bool

class ChatMessageEventData(TypedDict):
    """
    Event data for chat message events.
    """
    type: Literal[EventType.CHAT_MESSAGE]
    payload: ChatMessagePayload


# Contact and command result definitions

class Contact(TypedDict):
    """
    Represents a contact in the system.
    """
    contactID: str
    name: str
    contactType: str
    alias: NotRequired[str]
    gender: NotRequired[str]

class CommandStartPayload(TypedDict):
    """
    Payload for the start command.
    """
    sessionID: str

class CommandStartResult(TypedDict):
    """
    Result of the start command.
    """
    self: Contact
    contacts: List[Contact]

class CommandGetSelfPayload(TypedDict):
    """
    Payload for the getSelf command.
    """
    pass

class CommandGetSelfResult(TypedDict):
    """
    Result of the getSelf command.
    """
    contactID: str
    name: str
    contactType: str

class CommandGetContactsPayload(TypedDict):
    """
    Payload for the getContacts command.
    """
    pass

class CommandGetContactsResult(TypedDict):
    """
    Result of the getContacts command.
    """
    contacts: List[Contact]

class CommandGetContactInfoPayload(TypedDict):
    """
    Payload for the getContactInfo command.
    """
    contactID: str

class CommandGetContactInfoResult(TypedDict):
    """
    Result of the getContactInfo command.
    """
    name: str
    members: List[Contact]

class CommandSendChatMessagePayload(TypedDict):
    """
    Payload for sending chat messages.
    """
    receiverID: str
    content: ChatMessageContentUnion
    mentions: List[str]

class CommandSendChatMessageResult(TypedDict):
    """
    Result of the sendChatMessage command.
    """
    messageID: str

class CommandInternalStartResultEventPayload(TypedDict):
    """
    Command result event payload for the internal start command.
    """
    name: Literal["__start__"]
    commandID: str
    result: CommandStartResult
    error: Optional[str]

class CommandSendChatMessageResultEventPayload(TypedDict):
    """
    Command result event payload for sending a chat message.
    """
    name: Literal["sendChatMessage"]
    commandID: str
    result: CommandSendChatMessageResult
    error: Optional[str]

class CommandGetSelfResultEventPayload(TypedDict):
    """
    Command result event payload for getting information about the current user.
    """
    name: Literal["getSelf"]
    commandID: str
    result: CommandGetSelfResult
    error: Optional[str]

class CommandGetContactsResultEventPayload(TypedDict):
    """
    Command result event payload for getting the list of contacts.
    """
    name: Literal["getContacts"]
    commandID: str
    result: CommandGetContactsResult
    error: Optional[str]

class CommandGetContactInfoResultEventPayload(TypedDict):
    """
    Command result event payload for getting information about a specific contact.
    """
    name: Literal["getContactInfo"]
    commandID: str
    result: CommandGetContactInfoResult
    error: Optional[str]

CommandResultEventPayloadUnion = Union[
    CommandInternalStartResultEventPayload,
    CommandSendChatMessageResultEventPayload,
    CommandGetSelfResultEventPayload,
    CommandGetContactsResultEventPayload,
    CommandGetContactInfoResultEventPayload,
]

class CommandResultEventData(TypedDict):
    """
    Event data for command result events.
    """
    type: Literal[EventType.COMMAND_RESULT]
    payload: CommandResultEventPayloadUnion

EventDataUnion = Union[ChatMessageEventData, CommandResultEventData]

# Command data definitions

class CommandData(TypedDict):
    """
    Base class for command data.
    """
    id: str

class CommandInternalStartData(CommandData):
    """
    Command data for the internal start command.
    """
    name: Literal["__start__"]
    payload: CommandStartPayload

class CommandSendChatMessageData(CommandData):
    """
    Command data for sending a chat message.
    """
    name: Literal["sendChatMessage"]
    payload: CommandSendChatMessagePayload

class CommandGetSelfData(CommandData):
    """
    Command data for getting information about the current user.
    """
    name: Literal["getSelf"]
    payload: CommandGetSelfPayload

class CommandGetContactsData(CommandData):
    """
    Command data for getting the list of contacts for the current user.
    """
    name: Literal["getContacts"]
    payload: CommandGetContactsPayload

class CommandGetContactInfoData(CommandData):
    """
    Command data for getting detailed information about a specific contact.
    """
    name: Literal["getContactInfo"]
    payload: CommandGetContactInfoPayload

CommandDataUnion = Union[
    CommandInternalStartData,
    CommandSendChatMessageData,
    CommandGetSelfData,
    CommandGetContactsData,
    CommandGetContactInfoData,
]

class CommandRunner:
    async def on_start(self, payload: CommandStartPayload) -> CommandStartResult:
        """
        Handle the start command to initialize the connection

        Args:
            payload: The start command payload

        Returns:
            Start command result containing session info, self info, and contacts
        """
        raise NotImplementedError

    async def get_self(self, payload: CommandGetSelfPayload) -> CommandGetSelfResult:
        """
        Get information about the current user

        Args:
            payload: The getSelf command payload

        Returns:
            Current user's contact information
        """
        raise NotImplementedError

    async def get_contacts(self, payload: CommandGetContactsPayload) -> CommandGetContactsResult:
        """
        Get the list of contacts for the current user

        Args:
            payload: The getContacts command payload

        Returns:
            List of contacts
        """
        raise NotImplementedError

    async def get_contact_info(self, payload: CommandGetContactInfoPayload) -> CommandGetContactInfoResult:
        """
        Get detailed information about a specific contact

        Args:
            payload: The getContactInfo command payload

        Returns:
            Contact's detailed information
        """
        raise NotImplementedError

    async def send_chat_message(self, payload: CommandSendChatMessagePayload) -> CommandSendChatMessageResult:
        """
        Send a chat message to a specific receiver

        Args:
            payload: The sendChatMessage command payload

        Returns:
            Result of sending the message
        """
        raise NotImplementedError

class ChatbotClientOptions(TypedDict):
    """
    Options for configuring the chatbot client.
    """
    baseURL: str
    apiKey: str
    messagePlatformType: str
    messagePlatformAccountID: str
    commandRunner: CommandRunner