import asyncio
import json
import logging
import signal
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Set

import jwt as pyjwt
import websockets
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import uvicorn

# Presets for tools
presets = {
    "translate_text": {
        "function_declarations": [{
            "name": "translate_text",
            "description": "Translate text to a target language",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to translate"},
                    "targetLanguage": {"type": "string", "description": "Target language code (e.g., 'es', 'fr')"},
                },
                "required": ["text", "targetLanguage"],
            },
        }],
    },
    "summarize_text": {
        "function_declarations": [{
            "name": "summarize_text",
            "description": "Summarize a given text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to summarize"},
                    "maxLength": {"type": "integer", "description": "Maximum summary length (words)"},
                },
                "required": ["text"],
            },
        }],
    },
    "generate_code": {
        "function_declarations": [{
            "name": "generate_code",
            "description": "Generate code in a specified language",
            "parameters": {
                "type": "object",
                "properties": {
                    "language": {"type": "string", "description": "Programming language (e.g., 'python', 'javascript')"},
                    "task": {"type": "string", "description": "Description of the coding task"},
                },
                "required": ["language", "task"],
            },
        }],
    },
}

class GeminiLiveWsServer:
    def __init__(
        self,
        port: int,
        google_api_key: str,
        jwt_secret: Optional[str] = None,
        auth_func: Optional[Callable] = None,
        cors_origins: List[str] = ["*"],
        google_ws_url: str = (
            "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent"
        ),
        system_instruction: str = "You are a helpful assistant.",
        tools: Optional[List[Any]] = None,
        enable_metrics: bool = False,
        metrics_interval: float = 5.0,
        debug: bool = False,
    ):
        # Configuration
        self.port = port
        self.google_api_key = google_api_key
        self.jwt_secret = jwt_secret
        self.auth_func = auth_func
        self.cors_origins = cors_origins
        self.google_ws_url = google_ws_url
        self.system_instruction = system_instruction
        self.tools = self._build_tools(tools)
        self.enable_metrics = enable_metrics
        self.metrics_interval = metrics_interval
        self.logger = self._setup_logger(debug)

        # Metrics
        self.metrics_data = {
            "active_connections": 0,
            "messages_processed": 0,
            "errors": 0,
        } if enable_metrics else None
        self.metrics_subscribers: Set[Callable] = set()

        # FastAPI + Socket.IO setup
        self.sio = socketio.AsyncServer(
            async_mode="asgi",
            cors_allowed_origins=cors_origins,
            ping_timeout=60,
            ping_interval=25,
            logger=self.logger,
            engineio_logger=debug,
        )
        self.app = FastAPI(lifespan=self.lifespan)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.asgi_app = socketio.ASGIApp(self.sio, self.app, socketio_path="/socket.io")

        # WebSocket connections
        self.google_ws_connections: Dict[str, websockets.WebSocketClientProtocol] = {}
        self.message_queues: Dict[str, asyncio.Queue] = {}

        # Register handlers
        self.sio.event(self.connect)
        self.sio.event(self.disconnect)
        self.sio.on("message")(self.on_message)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        await self._on_startup()
        yield
        await self._on_shutdown()

    def _setup_logger(self, debug: bool) -> logging.Logger:
        level = logging.DEBUG if debug else logging.INFO
        logger = logging.getLogger("GeminiLiveWsServer")
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def _build_tools(self, config_tools: Optional[List[Any]]) -> List[Any]:
        result = []
        if not config_tools:
            return result
        for tool in config_tools:
            if isinstance(tool, str) and tool in presets:
                result.append(presets[tool])
            elif isinstance(tool, dict):
                result.append(tool)
        return result

    async def _on_startup(self):
        self.logger.info("Server starting up")
        if self.enable_metrics:
            asyncio.create_task(self._broadcast_metrics())

    async def _on_shutdown(self):
        self.logger.info("Server shutting down")
        # Close Google WS connections
        for ws in self.google_ws_connections.values():
            await ws.close()

    async def _broadcast_metrics(self):
        while True:
            await asyncio.sleep(self.metrics_interval)
            for callback in list(self.metrics_subscribers):
                try:
                    callback(self.metrics_data.copy())
                except Exception as e:
                    self.logger.error(f"Metrics subscriber error: {e}")

    async def connect(self, sid, environ, auth):
        # Authentication
        if self.auth_func:
            try:
                await self.auth_func(sid, environ, auth)
            except Exception as e:
                self.logger.error(f"Auth middleware error: {e}")
                raise e
        elif self.jwt_secret:
            token = auth.get("token") if auth else None
            if not token:
                raise socketio.exceptions.ConnectionRefusedError("Authentication error")
            try:
                # user = pyjwt.decode(token, self.jwt_secret, algorithms=["HS256"])
                environ['user'] = token
            except Exception as e:
                self.logger.error(f"JWT auth failed: {e}")
                raise socketio.exceptions.ConnectionRefusedError("Authentication failed")

        self.logger.info(f"Client connected: {sid}")
        if self.metrics_data:
            self.metrics_data['active_connections'] += 1

        # Prepare message queue
        self.message_queues[sid] = asyncio.Queue()
        # Start Google WS connection
        asyncio.create_task(self._setup_google_connection(sid))

    async def disconnect(self, sid):
        self.logger.info(f"Client disconnected: {sid}")
        if self.metrics_data:
            self.metrics_data['active_connections'] -= 1
        ws = self.google_ws_connections.get(sid)
        if ws:
            await ws.close()
            del self.google_ws_connections[sid]
        if sid in self.message_queues:
            del self.message_queues[sid]

    async def on_message(self, sid, data):
        if data is None:
            await self.sio.emit('error', 'Empty message', to=sid)
            self.logger.error("Empty message received")
            if self.metrics_data:
                self.metrics_data['errors'] += 1
            return
        
        # Add binary data warning
        if isinstance(data, bytes) and len(data) > 1024:
            self.logger.warning(f"Large binary message received ({len(data)} bytes)")
        
        try:
            message_str = json.dumps(data)
        except TypeError:
            await self.sio.emit('error', 'Invalid message format', to=sid)
            self.logger.error("Invalid message format (non-serializable)")
            return

        ws = self.google_ws_connections.get(sid)
        if ws and ws.state == websockets.State.OPEN:
            try:
                await ws.send(message_str)
            except Exception as e:
                await self.sio.emit('error', f"Send failed: {str(e)}", to=sid)
                self.logger.error(f"Send failed: {str(e)}")
                if self.metrics_data:
                    self.metrics_data['errors'] += 1
        else:
            await self.message_queues[sid].put(message_str)
    async def _setup_google_connection(self, sid: str):
        attempts = 0
        max_attempts = 3
        delay_base = 2
        queue = self.message_queues[sid]

        while attempts < max_attempts:
            attempts += 1
            delay = delay_base * (2 ** (attempts - 1))
            url = f"{self.google_ws_url}?key={self.google_api_key}"
            try:
                async with websockets.connect(url) as ws:
                    self.google_ws_connections[sid] = ws
                    attempts = 0
                    setup = {
                        "setup": {
                            "model": "models/gemini-2.0-flash-exp",
                            "outputAudioTranscription": {},
                            "system_instruction": {"role": "user", "parts": [{"text": self.system_instruction}]},
                            "tools": self.tools,
                        }
                    }
                    await ws.send(json.dumps(setup))
                    await self.sio.emit('ready', {'status': 'connected', 'timestamp': datetime.utcnow().isoformat()}, to=sid)
                    
                    # Process queued messages
                    while not queue.empty():
                        msg = await queue.get()
                        await ws.send(msg)

                    # Handle incoming messages
                    async for msg in ws:
                        try:
                            parsed = json.loads(msg)
                        except json.JSONDecodeError:
                            parsed = msg
                            log_msg = "Non-JSON message received"
                            if isinstance(msg, bytes):
                                log_msg += f" ({len(msg)} bytes)"
                            self.logger.warning(log_msg)
                            if self.metrics_data:
                                self.metrics_data['errors'] += 1
                        
                        # Handle transcription
                        server_content = parsed.get('serverContent', {})
                        if server_content.get('outputTranscription'):
                            text = server_content['outputTranscription'].get('text')
                            await self.sio.emit('transcription', 
                                {'text': text, 'timestamp': datetime.utcnow().isoformat()}, 
                                to=sid
                            )
                        else:
                            await self.sio.emit('message', parsed, to=sid)
                            if tool_call := parsed.get('toolCall'):
                                for tc in tool_call.get('functionCalls', []):
                                    self.logger.debug(f"Tool call received: {tc}")
                        
                        if self.metrics_data:
                            self.metrics_data['messages_processed'] += 1
                    
            except Exception as e:
                self.logger.error(f"Google WS error: {e}")
                if self.metrics_data:
                    self.metrics_data['errors'] += 1
                await asyncio.sleep(delay)
        
        # Max attempts reached
        await self.sio.emit('error', 'Failed to connect to AI', to=sid)
        self.logger.error("Max Google WS attempts reached")

    def run(self):
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        config = uvicorn.Config(
            self.asgi_app,
            host="0.0.0.0",
            port=self.port,
            log_config=None,
            loop="asyncio"
        )
        server = uvicorn.Server(config)

        try:
            if sys.platform != 'win32':
                def handle_exit_signal(s, f):
                    server.should_exit = True

                for sig in (signal.SIGINT, signal.SIGTERM):
                    signal.signal(sig, handle_exit_signal)
            
            asyncio.run(server.serve())
        except KeyboardInterrupt:
            self.logger.info("Server stopped by user")
        finally:
            self.logger.info("Server shutdown complete")

# if __name__ == "__main__":
#     server = GeminiLiveWsServer(
#         port=8080,
#         google_api_key="<API_KEY>",
#         jwt_secret="YOUR_SECRET",
#         # debug=True,
#         cors_origins=["http://127.0.0.1:5500"],
#         system_instruction="You are a helpful named omiii.",
#     )
#     server.run()