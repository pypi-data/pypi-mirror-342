# @Coding: UTF-8
# @Time: 2025/3/28 23:50
# @Author: xieyang_ls
# @Filename: thread_holder.py

from threading import current_thread

from pyutils_spirit.annotation import singleton

from pyutils_spirit.util import Assemble, HashAssemble


@singleton(signature="ThreadHolder")
class ThreadHolder:
    __instances: Assemble[str | int, object] = None

    def __init__(self):
        self.__instances = HashAssemble()

    def setThreadHolder(self, instance: object) -> None:
        currentThreadId = current_thread().ident
        self.__instances.put(currentThreadId, instance)

    def getThreadHolder(self) -> object:
        currentThreadId = current_thread().ident
        return self.__instances.get(currentThreadId)

    def removeThreadHolder(self) -> object:
        currentThreadId = current_thread().ident
        return self.__instances.remove(currentThreadId)

    def setHolder(self, key: str | int, value: object) -> None:
        self.__instances.put(key, value)

    def getHolder(self, key: str | int) -> object:
        return self.__instances.get(key)

    def removeHolder(self, key: str | int) -> object:
        return self.__instances.remove(key)
