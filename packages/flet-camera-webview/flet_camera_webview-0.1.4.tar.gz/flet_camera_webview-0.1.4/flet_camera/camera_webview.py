import asyncio
import threading
import websockets
import base64
import socket
import os
from typing import Optional
import flet_webview as fwv
import shutil
from urllib.parse import urlparse
import flet as ft

# Глобальные переменные
_global_ws_server_started = False
_client_ids_by_session = {}

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # неважно куда, просто чтобы узнать интерфейс
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


class CameraWebView(fwv.WebView):
    latest_frame: Optional[str] = None

    def __init__(self, page: ft.Page, html_path="src"):
        parsed = urlparse(page.url)
        ip = get_local_ip()
        self.host = parsed.hostname or "127.0.0.1"
        # self.host = ip
        self.ws_port = 8765
        self.http_port = parsed.port or 8000

        self._frames_by_client = {}
        self._my_session_id = page.session_id
        self._watching_session_id = self._my_session_id

        # Регистрируем сессию заранее
        if self._my_session_id not in _client_ids_by_session:
            _client_ids_by_session[self._my_session_id] = None
            print(f"🕓 Зарегистрирована сессия: {self._my_session_id} (ожидание WebSocket)")

        # Копируем HTML, если нужно
        default_path = os.path.join(os.path.dirname(__file__), "assets", "camera.html")
        project_path = os.path.join(os.getcwd(), html_path, "assets", "camera.html")
        if not os.path.exists(project_path):
            os.makedirs(os.path.dirname(project_path), exist_ok=True)
            shutil.copy2(default_path, project_path)
            print(f"📄 Файл camera.html скопирован в {project_path}")

        # Запуск WebSocket сервера
        self._started = False
        self._start_services()

        # WebView 
        url = f"https://{self.host}:{self.http_port}/camera.html"
        print(f"🌐 URL WebView: {url}")
        # url = f"http://192.168.8.8:{self.http_port}/camera.html"
        super().__init__(url=url, expand=True)

    def _start_services(self):
        global _global_ws_server_started
        if self._started:
            return
        self._started = True

        if not _global_ws_server_started:
            _global_ws_server_started = True
            threading.Thread(target=lambda: asyncio.run(self._start_ws_server()), daemon=True).start()

    async def _start_ws_server(self):
        my_session_id = self._my_session_id

        async def handler(websocket):
            client_id = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
            print(f"📡 Новое подключение: {client_id}")

            if _client_ids_by_session.get(my_session_id) is None:
                _client_ids_by_session[my_session_id] = client_id
                print(f"✅ WebSocket зарегистрирован: {my_session_id} → {client_id}")

            try:
                async for message in websocket:
                    if message.startswith("data:image"):
                        self._frames_by_client[client_id] = message
            except Exception as e:
                print(f"❌ Ошибка WebSocket от {client_id}: {e}")

        await websockets.serve(handler, self.host, self.ws_port)
        print(f"🚀 WebSocket сервер: ws://{self.host}:{self.ws_port}")
        await asyncio.Future()

    def switch_to(self, session_id: str):
        if session_id in _client_ids_by_session:
            self._watching_session_id = session_id
            print(f"🔀 Переключено на сессию: {session_id}")
        else:
            print(f"⚠️ Невозможно переключиться: сессия {session_id} не найдена")

    def list_sessions(self):
        return list(_client_ids_by_session.keys())

    def get_image_bytes(self, session_id: Optional[str] = None) -> Optional[bytes]:
        target_session_id = session_id or self._watching_session_id
        client_id = _client_ids_by_session.get(target_session_id)

        if client_id is None:
            print(f"⏳ Ожидание WebSocket от session_id: {target_session_id}")
            return None

        latest = self._frames_by_client.get(client_id)
        if not latest:
            print(f"⏳ Нет кадров от клиента: {client_id} (session: {target_session_id})")
            return None

        print(f"📦 Кадр от client_id: {client_id} (для session_id: {target_session_id})")
        try:
            b64 = latest.split(",")[1]
            return base64.b64decode(b64)
        except Exception as e:
            print(f"❌ Ошибка декодирования от {client_id}: {e}")
            return None
