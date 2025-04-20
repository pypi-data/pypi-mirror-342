# ------------------------------------------------------------------------------
# Copyright (c) 2022 Korawich Anuttra. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for
# license information.
# ------------------------------------------------------------------------------
from __future__ import annotations

import ctypes
import inspect
import os
import threading
import time
from datetime import datetime
from typing import Any

try:
    import psutil
except ImportError:  # pragma: no cove
    psutil = None

MAX_THREAD: int = int(os.getenv("PY_MAX_THREAD", "10"))


def _async_raise(tid, exc_type) -> None:  # pragma: no cove
    """Raises an exception in the threads with id tid"""
    if not inspect.isclass(exc_type):
        raise TypeError("Only core can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exc_type)
    )
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # NOTE: If it returns a number greater than one, you're in trouble,
        #   and you should call it again with exc=NULL to revert the effect.
        #
        #   >>> ctypes.pythonapi.PyThreadState_SetAsyncExc(
        #   ...     ctypes.c_long(tid), 0
        #   ... )
        #
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class ThreadWithControl(threading.Thread):  # pragma: no cove
    """Threading object that can control maximum background agent and result
    after complete.

        -   Get return output from threading function
        -   A thread class that supports raising an exception in the thread from
            another thread.

    Examples:
        >>> _thread = ThreadWithControl(target=lambda a: a * 2, args=(2, ))
        >>> _thread.daemon = True
        >>> _thread.start()
        >>> print(_thread.join())
        4
    """

    threadLimiter = threading.BoundedSemaphore(MAX_THREAD)

    def __init__(self, *args, **kwargs):
        # NOTE: Create existing attrs that will create from parent class.
        self._return = None
        self._target = None
        self._args = None
        self._kwargs = None
        super().__init__(*args, **kwargs)

        # NOTE: Create threading event.
        self._stop_event = threading.Event()
        self.check_count = 0

    def run(self):
        self.threadLimiter.acquire()
        try:
            if self._target:
                self._return = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs
            self.threadLimiter.release()

    def join(self, *args) -> Any:
        super().join(*args)
        return self._return

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def _get_my_tid(self):
        """Determines this (self's) thread id.

        CAREFUL: this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.is_alive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_ident"):
            return self._ident

        for thread in threading.enumerate():
            if thread is self:
                self._ident = thread.ident
                return thread.ident

        raise AssertionError("could not determine the thread's id")

    def raise_exc(self, exc_type):
        """
        Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc(...)
            ...
            t.raise_exc(SomeException)
            while t.isAlive():
                time.sleep(0.1)
                t.raise_exc(SomeException)

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL: this function is executed in the context of the
        caller thread, to raise an exception in the context of the
        thread represented by this instance.
        """
        _async_raise(self._get_my_tid(), exc_type)

    def terminate(self):
        """
        must raise the SystemExit type, instead of a SystemExit() instance
        due to a bug in PyThreadState_SetAsyncExc
        """
        self.raise_exc(SystemExit)


class MonitorThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(
        self,
        *args,
        prefix: str = None,
        waiting: int = 10,
        log=None,
        **kwargs,
    ):
        if psutil is None:
            raise NotImplementedError(
                "Monitoring thread need the ``psutil`` package, you should "
                "install it before running with: `pip install -U psutil`"
            )
        super().__init__(*args, **kwargs)
        self._log = log or print
        self._prefix: str = prefix or ""
        self._waiting: int = waiting
        self._stop = threading.Event()
        self.profiles: dict[str, list[float]] = {"cpu": [], "mem": []}

    def stop(self) -> None:
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self) -> None:
        """main control loop"""
        while not self.stopped():
            cpu: float = psutil.cpu_percent(interval=1)
            mem: float = psutil.virtual_memory().percent

            self.profiles["cpu"].append(cpu)
            self.profiles["mem"].append(mem)

            self._log(
                f"{self._prefix}{datetime.now():%Y-%m-%d %H:%M:%S} "
                f"CPU %: {cpu}, Mem %: {mem}, "
                f"Thread: {threading.active_count()}, "
                f"Process: {len([*psutil.process_iter()])}"
            )
            time.sleep(self._waiting)

    @property
    def summarize(self) -> tuple[float, float]:
        return (
            round(sum(self.profiles["cpu"]) / len(self.profiles["cpu"]), 3),
            round(sum(self.profiles["mem"]) / len(self.profiles["mem"]), 3),
        )
