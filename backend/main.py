import json
import hmac
import hashlib
from collections import defaultdict
from typing import Optional, Dict, Any, Union

import websockets
import asyncio
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn

# Load configuration
with open('data/rtms_credentials.json') as f:
    config = json.load(f)

ZOOM_SECRET_TOKEN = config['Zoom_Webhook_Secret_Token'][0]['token']
# Using the first set of credentials as default, but you might want to implement credential selection logic
CLIENT_SECRET = config['auth_credentials'][0]['client_secret']

# Track active connections
active_connections = defaultdict(dict)

app = FastAPI()

class URLValidationResponse(BaseModel):
    plainToken: str
    encryptedToken: str

class StandardResponse(BaseModel):
    status: str

class RTMSPayload(BaseModel):
    event: Optional[str]
    payload: Optional[Dict[str, Any]]

def generate_signature(client_id: str, meeting_uuid: str, stream_id: str, secret: str) -> str:
    """Generate HMAC signature for RTMS authentication."""
    message = f"{client_id},{meeting_uuid},{stream_id}"
    return hmac.new(
        secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

async def connect_to_media_websocket(
    endpoint: str,
    client_id: str,
    meeting_uuid: str,
    stream_id: str,
    media_type: str
) -> None:
    """Connect to the RTMS media WebSocket server."""
    connection_id = f"{meeting_uuid}_{stream_id}_{media_type}"
    
    # Close existing media connection if any
    if connection_id in active_connections:
        await active_connections[connection_id]['ws'].close()
        del active_connections[connection_id]

    try:
        async with websockets.connect(endpoint, ssl=None) as ws:
            active_connections[connection_id] = {'ws': ws}
            
            media_signature = generate_signature(client_id, meeting_uuid, stream_id, CLIENT_SECRET)
            handshake_message = {
                "msg_type": "DATA_HAND_SHAKE_REQ",
                "protocol_version": 1,
                "meeting_uuid": meeting_uuid,
                "rtms_stream_id": stream_id,
                "signature": media_signature,
                "payload_encryption": False
            }
            await ws.send(json.dumps(handshake_message))

            async for message in ws:
                data = json.loads(message)
                # Handle media data here
                print(f"Received {media_type} data:", data)

    except Exception as e:
        print(f"{media_type} WebSocket error: {e}")
    finally:
        if connection_id in active_connections:
            del active_connections[connection_id]

async def connect_to_rtms_websocket(
    client_id: str,
    meeting_uuid: str,
    stream_id: str,
    server_url: str
) -> None:
    """Connect to the RTMS signaling WebSocket server."""
    connection_id = f"{meeting_uuid}_{stream_id}"
    
    # Close existing connection if any
    if connection_id in active_connections:
        await active_connections[connection_id]['ws'].close()
        del active_connections[connection_id]

    try:
        async with websockets.connect(server_url, ssl=None) as ws:
            active_connections[connection_id] = {'ws': ws}
            
            signature = generate_signature(client_id, meeting_uuid, stream_id, CLIENT_SECRET)
            handshake_message = {
                "msg_type": "SIGNALING_HAND_SHAKE_REQ",
                "protocol_version": 1,
                "meeting_uuid": meeting_uuid,
                "rtms_stream_id": stream_id,
                "signature": signature
            }
            await ws.send(json.dumps(handshake_message))

            async for message in ws:
                data = json.loads(message)
                
                if data['msg_type'] == "SIGNALING_HAND_SHAKE_RESP":
                    if data['status_code'] == "STATUS_OK":
                        media_urls = data['media_server']['server_urls']
                        
                        # Connect to all available media endpoints
                        for media_type, url in media_urls.items():
                            asyncio.create_task(
                                connect_to_media_websocket(
                                    url,
                                    client_id,
                                    meeting_uuid,
                                    stream_id,
                                    media_type
                                )
                            )
                
                elif data['msg_type'] == "STREAM_STATE_UPDATE":
                    if data['state'] == "TERMINATED":
                        await ws.close()
                        if connection_id in active_connections:
                            del active_connections[connection_id]
                        break
                
                elif data['msg_type'] == "KEEP_ALIVE_REQ":
                    response = {
                        "msg_type": "KEEP_ALIVE_RESP",
                        "timestamp": int(asyncio.get_event_loop().time() * 1000)
                    }
                    await ws.send(json.dumps(response))

    except Exception as e:
        print(f"RTMS WebSocket error: {e}")
    finally:
        if connection_id in active_connections:
            del active_connections[connection_id]

@app.post("/", response_model=Union[URLValidationResponse, StandardResponse])
async def webhook_handler(request: Request):
    """Handle incoming Zoom webhooks."""
    data = await request.json()
    event = data.get('event')
    payload = data.get('payload', {})

    # Handle Zoom Webhook validation
    if event == 'endpoint.url_validation' and payload.get('plainToken'):
        print('Received URL validation request:', {
            'event': event,
            'plainToken': payload['plainToken']
        })

        hash_for_validate = hmac.new(
            ZOOM_SECRET_TOKEN.encode(),
            payload['plainToken'].encode(),
            hashlib.sha256
        ).hexdigest()

        response = URLValidationResponse(
            plainToken=payload['plainToken'],
            encryptedToken=hash_for_validate
        )
        
        print('Sending URL validation response:', response.dict())
        return response

    # Handle RTMS start event
    if (payload.get('event') == 'meeting.rtms.started' and 
        payload.get('payload', {}).get('object')):
        
        client_id = data.get('clientId')
        meeting_data = payload['payload']['object']
        meeting_uuid = meeting_data.get('meeting_uuid')
        rtms_stream_id = meeting_data.get('rtms_stream_id')
        server_urls = meeting_data.get('server_urls')

        if all([client_id, meeting_uuid, rtms_stream_id, server_urls]):
            asyncio.create_task(
                connect_to_rtms_websocket(
                    client_id,
                    meeting_uuid,
                    rtms_stream_id,
                    server_urls
                )
            )

    return StandardResponse(status="ok")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up connections on shutdown."""
    for connections in active_connections.values():
        if 'ws' in connections:
            await connections['ws'].close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)