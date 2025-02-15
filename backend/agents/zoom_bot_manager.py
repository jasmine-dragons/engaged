from typing import List, Dict
import asyncio
import aiohttp
from datetime import datetime
import json
import base64
import os
from dotenv import load_dotenv

load_dotenv()

class ZoomBotManager:
    def __init__(self, api_key: str, api_secret: str, account_id: str):
        self.client_id = os.getenv("ZOOM_CLIENT_ID")
        self.client_secret = os.getenv("ZOOM_CLIENT_SECRET")
        self.account_id = account_id
        self.base_url = "https://api.zoom.us/v2"
        self.bot_tokens: Dict[str, str] = {}  # student_name -> token
        self.access_token = None
        self.token_expiry = None

    async def _get_access_token(self) -> str:
        """Get OAuth access token for Zoom API authentication"""
        if self.access_token and self.token_expiry and datetime.utcnow().timestamp() < self.token_expiry:
            return self.access_token

        print("Getting new access token...")
        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')

        headers = {
            "Authorization": f"Basic {base64_auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://zoom.us/oauth/token",
                    headers=headers,
                    data={"grant_type": "account_credentials", "account_id": self.account_id},
                ) as response:
                    print(f"Token response status: {response.status}")
                    if response.status == 200:
                        token_data = await response.json()
                        print("Got token data:", token_data)
                        self.access_token = token_data["access_token"]
                        self.token_expiry = datetime.utcnow().timestamp() + token_data["expires_in"]
                        return self.access_token
                    else:
                        error_text = await response.text()
                        print(f"Error getting token: {error_text}")
                        raise Exception(f"Failed to get access token: {error_text}")
        except Exception as e:
            print(f"Exception in _get_access_token: {str(e)}")
            raise

    async def create_bot_participants(self, meeting_id: str, student_names: List[str]):
        """Create bot participants for each student"""
        print("[CREATE BOT PARTICIPANTS]")
        print(f"Meeting ID: {meeting_id}")
        print(f"Student Names: {student_names}")

        try:
            access_token = await self._get_access_token()
            print("Got access token:", access_token[:10] + "...")

            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }

            async with aiohttp.ClientSession() as session:
                for student_name in student_names:
                    try:
                        # Register bot with Zoom
                        register_url = f"{self.base_url}/meetings/{meeting_id}/registrants"
                        register_data = {
                            "email": f"{student_name.lower().replace(' ', '_')}@aibot.virtual",
                            "first_name": student_name,
                            "last_name": "AI Bot"
                        }
                        print(f"Registering {student_name} at {register_url}")
                        print(f"Data: {register_data}")

                        async with session.post(register_url, headers=headers, json=register_data) as response:
                            print(f"Response status for {student_name}: {response.status}")
                            response_text = await response.text()
                            print(f"Response body for {student_name}: {response_text}")
                            
                            if response.status in [201, 200]:
                                reg_data = json.loads(response_text)
                                self.bot_tokens[student_name] = reg_data.get('join_url', '')
                            else:
                                print(f"Failed to register {student_name}: {response_text}")
                    except Exception as e:
                        print(f"Error registering {student_name}: {str(e)}")

        except Exception as e:
            print(f"Error in create_bot_participants: {str(e)}")
            raise

    async def send_chat_message(self, meeting_id: str, student_name: str, message: str):
        """Send a chat message to the meeting on behalf of a student"""
        if student_name not in self.bot_tokens:
            raise ValueError(f"No bot token found for student {student_name}")

        access_token = await self._get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        chat_url = f"{self.base_url}/meetings/{meeting_id}/chat"
        chat_data = {
            "message": message,
            "to_contact": "everyone"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(chat_url, headers=headers, json=chat_data) as response:
                if response.status not in [201, 200]:
                    print(f"Failed to send message: {await response.text()}")

    async def join_meeting(self, meeting_id: str, student_name: str):
        """Join the meeting as a bot participant"""
        if student_name not in self.bot_tokens:
            raise ValueError(f"No join token found for student {student_name}")
        
        # In a real implementation, you would use the Zoom SDK to programmatically join
        # the meeting. For now, we'll just print the join URL
        print(f"Bot {student_name} would join using: {self.bot_tokens[student_name]}")
