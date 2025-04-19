import os
import json
import logging
from datetime import timedelta
from typing import Any, Dict, Optional, Union, cast
import aiohttp
import asyncio
from aiohttp_sse_client import client as sse_client
from .types import (
    ChatMessagePayload,
    CommandDataUnion,
    EventDataUnion,
    ChatbotClientOptions,
    CommandStartResult,
    CommandGetSelfResult,
    CommandGetContactsResult,
    CommandGetContactInfoResult, 
    CommandSendChatMessageResult,
    to_dict,
    ChatMessageEventData,
)
from .db import CommandDB

logger = logging.getLogger(__name__)

class ChatbotClient:
    """Main client for interacting with the chatbot platform.
    
    Handles connection, command execution, and event handling between
    the application and the messaging platform.
    """
    
    def __init__(self, options: ChatbotClientOptions):
        """Create a new instance of the ChatbotClient.
        
        Args:
            options: Configuration options for the client
        """
        self.baseURL = options["baseURL"]
        self.apiKey = options["apiKey"]
        self.messagePlatformType = options["messagePlatformType"]
        self.messagePlatformAccountID = options["messagePlatformAccountID"]
        self.commandRunner = options["commandRunner"]
        self.headers = {"Authorization": f"Bearer {self.apiKey}"}
        self.command_task = None
        self.command_db = CommandDB()

    async def start(self) -> None:
        """Start the client and establish a connection to the chatbot platform.
        
        Sets up an EventSource to listen for commands from the platform and
        handles them by delegating to the appropriate command runner methods.
        """
        url = f"{self.baseURL}/api/message-platforms/{self.messagePlatformType}/{self.messagePlatformAccountID}/commands"
        
        # Create a background task to handle the SSE connection
        self.command_task = asyncio.create_task(self._listen_for_commands(url))
        
    async def _listen_for_commands(self, url: str) -> None:
        """Listen for commands from the chatbot platform in the background.
        
        Args:
            url: The URL to connect to for SSE events
        """
        async with sse_client.EventSource(url, headers=self.headers, reconnection_time=timedelta(seconds=1)) as event_source:
            try:
                async for event in event_source:
                    if event.type is None:  # Normal messages have type=None
                        try:
                            command_data = json.loads(event.data)
                            logger.info("Received command: %s", command_data)
                            
                            command_id = command_data.get("id", "")
                            command_name = command_data.get("name", "")
                            command_payload = command_data.get("payload", {})
                            
                            # Check if command was already executed
                            existing_command = self.command_db.get_command(command_id)
                            if existing_command:
                                logger.info("Command %s already executed, returning cached result", command_id)
                                await self._send_command_result(
                                    command_data,
                                    result=existing_command["result"],
                                    error=existing_command["error"],
                                    skip_save=True  # Skip saving since command already exists
                                )
                                continue

                            # Execute command based on name
                            if command_name == "__start__":
                                try:
                                    self.headers['x-session-id'] = command_payload['sessionID']
                                    result: CommandStartResult = await self.commandRunner.on_start(command_payload)
                                    await self._send_command_result(command_data, result)
                                except Exception as e:
                                    await self._send_command_result(command_data, error=str(e))
                            elif command_name == "getSelf":
                                try:
                                    result: CommandGetSelfResult = await self.commandRunner.get_self(command_payload)
                                    await self._send_command_result(command_data, result)
                                except Exception as e:
                                    await self._send_command_result(command_data, error=str(e))
                            elif command_name == "getContacts":
                                try:
                                    result: CommandGetContactsResult = await self.commandRunner.get_contacts(command_payload)
                                    await self._send_command_result(command_data, result)
                                except Exception as e:
                                    await self._send_command_result(command_data, error=str(e))
                            elif command_name == "getContactInfo":
                                try:
                                    result: CommandGetContactInfoResult = await self.commandRunner.get_contact_info(command_payload)
                                    await self._send_command_result(command_data, result)
                                except Exception as e:
                                    await self._send_command_result(command_data, error=str(e))
                            elif command_name == "sendChatMessage":
                                try:
                                    result: CommandSendChatMessageResult = await self.commandRunner.send_chat_message(command_payload)
                                    await self._send_command_result(command_data, result)
                                except Exception as e:
                                    await self._send_command_result(command_data, error=str(e))
                            else:
                                logger.error("Unknown command: %s", command_data)
                                error_msg = "Unknown command"
                                await self._send_command_result(command_data, error=error_msg)
                        except Exception as e:
                            logger.error("Error processing command: %s", e)
                            if 'command_data' in locals():
                                await self._send_command_result(command_data, error=str(e))
                    elif event.type == "error":
                        logger.error("SSE error event: %s", event.data)
                        # Don't break the connection on error events
                        continue
                    else:
                        logger.info("Received event with type: %s, data: %s", event.type, event.data)
            except Exception as e:
                logger.error("SSE connection error: %s", e)
                # Connection error - client should attempt to reconnect
                await asyncio.sleep(5)  # Wait before reconnecting
                self.command_task = asyncio.create_task(self._listen_for_commands(url))  # Reconnect

    async def on_receive_chat_message(self, payload: ChatMessagePayload) -> EventDataUnion:
        """Handle the receipt of a chat message from the messaging platform.
        
        Forwards the message to the chatbot platform as an event.
        
        Args:
            payload: The chat message payload to send
            
        Returns:
            The response from the chatbot platform
        """
        logger.info("Received chat message: %s", payload)
        event_data: ChatMessageEventData = {
            "type": "chat-message",
            "payload": to_dict(payload)
        }
        return await self._send_event(event_data)

    async def _send_command_result(
        self,
        command: CommandDataUnion,
        result: Optional[Union[CommandStartResult, CommandGetSelfResult, CommandGetContactsResult, CommandGetContactInfoResult, CommandSendChatMessageResult]] = None,
        error: Optional[str] = None,
        skip_save: bool = False
    ) -> EventDataUnion:
        """Send a command result event to the chatbot platform.
        
        Used to report the success or failure of command execution.
        
        Args:
            command: The command that was executed
            result: The result of the command execution (if successful)
            error: The error message (if command execution failed)
            skip_save: Whether to skip saving the command result to database
            
        Returns:
            The response from the chatbot platform
        """
        # Save command execution record to database if not skipping
        if not skip_save:
            self.command_db.save_command(
                command_id=command["id"],
                command_name=command["name"],
                command_payload=command["payload"],
                result=result,
                error=error
            )
        
        # Create a payload without type annotation first
        payload = {
            "name": command["name"],
            "commandID": command["id"],
            "result": result,
            "error": error,
        }
        
        # Create the event data without type annotation
        event_data = {
            "type": "command-result",
            "payload": payload
        }
        
        logger.info("Sending command result: %s", event_data)
        
        # Convert to a serializable format and then back to ensure consistent field names
        event_data_json = json.dumps(event_data, default=lambda o: to_dict(o) if hasattr(o, "__dict__") else str(o))
        event_data_serialized = json.loads(event_data_json)
        
        return await self._send_event(event_data_serialized)
        
    async def _send_event(self, payload: EventDataUnion) -> EventDataUnion:
        """Send an event to the chatbot platform.
        
        Used for sending chat messages and command results.
        
        Args:
            payload: The event data to send
            
        Returns:
            The response from the chatbot platform
        """
        url = f"{self.baseURL}/api/message-platforms/{self.messagePlatformType}/{self.messagePlatformAccountID}/events"
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=self.headers, json=payload) as response:
                    # 201 Created is a success response for resource creation
                    if response.status not in [200, 201]:
                        error_text = await response.text()
                        logger.error("Error sending event: %s %s", response.status, error_text)
                        raise Exception(f"Error sending event: {response.status} {error_text}")
                    return await response.json()
            except Exception as e:
                logger.error("Error sending event: %s", e)
                raise

    async def upload(self, path):
        """Upload a file to the chatbot platform.
        Equivalent to curl -X POST https://chat.cwllll.com/api/upload -H "Authorization: Bearer API_KEY" -F "file=@test.jpg"
        
        NOTE: file name is required, in this example, it's test.jpg
        Args:
            path: The path to the file to upload
            
        Returns:
            { "url": "https://example.com/file.pdf" }
        """
        url = f"{self.baseURL}/api/upload"
        async with aiohttp.ClientSession() as session:
            # file name is required, get from basename of path
            file_name = os.path.basename(path)
            data = aiohttp.FormData()
            data.add_field('file', open(path, 'rb'), filename=file_name)
            async with session.post(url, headers=self.headers, data=data) as response:
                # Check for successful upload (e.g., status code 200 or 201)
                if response.status not in [200, 201]:
                    error_text = await response.text()
                    logger.error("Error uploading file: %s %s", response.status, error_text)
                    raise Exception(f"Error uploading file: {response.status} {error_text}")
                return await response.json()
