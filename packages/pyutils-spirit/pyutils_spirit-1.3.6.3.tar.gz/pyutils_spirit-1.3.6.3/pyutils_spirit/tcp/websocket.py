# @Coding: UTF-8
# @Time: 2024/9/20 12:29
# @Author: xieyang_ls
# @Filename: websocket.py

import time

import socket

import base64

import hashlib

from abc import ABC

from pyutils_spirit.style import draw_websocket_banner

from logging import info, basicConfig, INFO, exception

from pyutils_spirit.util import Assemble, HashAssemble

from pyutils_spirit.concurrent_thread import ThreadExecutor

basicConfig(level=INFO)


class WebSocket(ABC):
    __socket_server: socket.socket = None

    __listener_count = None

    __buffer_size: int = None

    __websocket_server_class: type = None

    __executor: ThreadExecutor = None

    __instance_assemble: Assemble[int, object] = None

    __encoding: str = None

    __onopen_func: callable = None

    __onmessage_func: callable = None

    __close_signature = None

    __onclose_func: callable = None

    __onerror_func: callable = None

    @classmethod
    def __start_server(cls, host, port, other_cls):
        cls.__socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.__listener_count = 127
        cls.__buffer_size = 1024
        cls.__websocket_server_class = other_cls
        cls.__executor = ThreadExecutor(executor_count=1024)
        cls.__instance_assemble = HashAssemble()
        cls.__encoding = "utf-8"
        cls.__socket_server.bind((host, port))
        cls.__socket_server.listen(cls.__listener_count)
        cls.__executor.execute(cls.__listenerConnection)
        cls.__close_signature = ""
        info(f" WebSocket Server listening on ws://{host}:{port}")

    class Session:
        __socket: socket.socket = None

        __address: tuple[str, int] = None

        __buffer_size: int = None

        __is_connected: bool = None

        __headers: list[str] = None

        __start_connected_timer: float = None

        __close_connected_timer: float = None

        def __init__(self,
                     socket_client: socket.socket,
                     address: tuple[str, int] = None,
                     is_connected: bool = True,
                     buffer_size: int = None):
            self.__socket = socket_client
            self.__address = address
            self.__is_connected = is_connected
            self.__buffer_count = 1024 if buffer_size is None else buffer_size
            self.__start_connected_timer = time.time()

        def get_socket_client(self) -> socket.socket:
            return self.__socket

        def get_is_connected(self) -> bool:
            return self.__is_connected

        def get_address(self):
            if self.__address is None:
                self.__address = self.__socket.getpeername()
            return self.__address

        def get_headers(self) -> list[str]:
            if self.__headers is None:
                socket_headers = self.__socket.recv(self.__buffer_count).decode()
                self.__headers = socket_headers.splitlines()
            return self.__headers

        def get_params(self) -> dict | None:
            if self.__headers is None:
                return None
            header = self.__headers[0]
            arguments = header.split()[1].split("?")[1]
            params = dict(param.split('=') for param in arguments.split('&'))
            return params

        def sendMessage(self, message: str, encoding: str = "utf-8") -> None:
            message_bytes = message.encode(encoding)
            if len(message_bytes) <= 125:
                frame = bytearray([0x81, len(message_bytes)]) + message_bytes
            elif 126 <= len(message_bytes) <= 65535:
                frame = bytearray([0x81, 126]) + len(message_bytes).to_bytes(2, 'big') + message_bytes
            else:
                frame = bytearray([0x81, 127]) + len(message_bytes).to_bytes(8, 'big') + message_bytes
            self.__socket.send(frame)

        def close(self) -> None:
            self.__socket.close()
            self.__is_connected = False
            self.__close_connected_timer = time.time()

        def __str__(self) -> str:
            if self.__is_connected:
                connected_timer: str = f"current_connected_timer={time.time() - self.__start_connected_timer}"
            else:
                connected_timer = f"total_connected_timer={self.__close_connected_timer - self.__start_connected_timer}"
            return ("{" + f"socket={self.__socket}, " +
                    f"address={self.__address}, " +
                    f"{connected_timer}")

    @classmethod
    def __handshaking(cls, session: Session, header_item):
        # WebSocket 握手
        accept_key = base64.b64encode(
            hashlib.sha1(
                (header_item.split(": ")[1] + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()).decode()
        response = f"HTTP/1.1 101 Switching Protocols\r\n" \
                   f"Upgrade: websocket\r\n" \
                   f"Connection: Upgrade\r\n" \
                   f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
        session.get_socket_client().send(response.encode())

    @classmethod
    def __listenerConnection(cls) -> None:
        while True:
            try:
                socket_client, addr = cls.__socket_server.accept()
                session = cls.Session(socket_client=socket_client,
                                      address=addr,
                                      is_connected=True,
                                      buffer_size=cls.__buffer_size)
                for header_item in session.get_headers():
                    if "Sec-WebSocket-Key" in header_item:
                        cls.__handshaking(session, header_item)
                instance = cls.__websocket_server_class()
                cls.__instance_assemble.put(addr[1], instance)
                cls.__onopen_func(instance, session=session)
                cls.__executor.execute(cls.__listenerMessage, session=session)
            except Exception as e:
                exception(e)

    @classmethod
    def __receive_message(cls, session: Session):
        socket_client = session.get_socket_client()
        # 接收消息
        data = socket_client.recv(1024)
        if len(data) < 2:
            return None  # 处理接收的数据不足情况
        length = data[1] & 127
        if length == 126:
            if len(data) < 4:
                return None
            length = int.from_bytes(data[2:4], 'big')
        elif length == 127:
            if len(data) < 10:
                return None
            length = int.from_bytes(data[2:10], 'big')

        mask_start = 2 + (4 if length == 126 else (10 if length == 127 else 0))
        if len(data) < mask_start + 4:
            return None  # 确保掩码存在

        masks = data[mask_start:mask_start + 4]
        message = bytearray()

        for i in range(length):
            message.append(data[mask_start + 4 + i] ^ masks[i % 4])

        return message.decode(cls.__encoding, errors='ignore')

    @classmethod
    def __listenerMessage(cls, session: Session) -> None:
        address = session.get_address()[1]
        while session.get_is_connected():
            try:
                message: str = cls.__receive_message(session)
                if message is None or message is cls.__close_signature:
                    instance = cls.__instance_assemble.get(address)
                    session.close()
                    if cls.__onclose_func is not None:
                        cls.__onclose_func(instance, session=session)
                    break
                if cls.__onmessage_func is not None:
                    instance = cls.__instance_assemble.get(address)
                    cls.__onmessage_func(instance, message=message)
            except Exception as e:
                exception(e)
                if cls.__onerror_func is not None:
                    instance = cls.__instance_assemble.get(address)
                    try:
                        cls.__onerror_func(instance, session=session, exc=e)
                    except Exception as e:
                        exception(e)
        cls.__instance_assemble.remove(address)

    @classmethod
    def WebSocketServer(cls, host: str, port: int) -> callable:

        def decorator_handler(other_cls) -> type:
            draw_websocket_banner()
            cls.__start_server(host, port, other_cls)
            other_cls.__decorator__ = "WebSocketServer"
            other_cls.__decorator_params__ = {
                "host": host,
                "port": port
            }
            return other_cls

        return decorator_handler

    @classmethod
    def onopen(cls) -> callable:
        def decorator_handler(func) -> None:
            func.__decorator__ = "onopen"
            cls.__onopen_func = func
            return func

        return decorator_handler

    @classmethod
    def onmessage(cls) -> callable:
        def decorator_handler(func) -> None:
            func.__decorator__ = "onmessage"
            cls.__onmessage_func = func
            return func

        return decorator_handler

    @classmethod
    def onclose(cls) -> callable:
        def decorator_handler(func) -> None:
            func.__decorator__ = "onclose"
            cls.__onclose_func = func
            return func

        return decorator_handler

    @classmethod
    def onerror(cls) -> callable:
        def decorator_handler(func) -> None:
            func.__decorator__ = "onerror"
            cls.__onerror_func = func
            return func

        return decorator_handler


WebSocketServer = WebSocket.WebSocketServer
Session = WebSocket.Session
onopen = WebSocket.onopen
onmessage = WebSocket.onmessage
onclose = WebSocket.onclose
onerror = WebSocket.onerror
