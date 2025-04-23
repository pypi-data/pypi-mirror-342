#
# Copyright 2022 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc. Confidential.
#
# This is unpublished proprietary source code of DataRobot, Inc.
# and its affiliates.
#
# The copyright notice above does not evidence any actual or intended
# publication of such source code.
#
# This file and its contents are subject to DataRobot Tool and Utility Agreement.
# For details, see
# https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#
"""
This module provides client pool to manage long-live connections in multi-thread or coroutines
"""

import datetime
import logging
import threading
import time
import traceback
from collections import deque
from contextlib import contextmanager
from functools import wraps
from time import sleep

import dateutil.parser  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)

DRTIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class ClientPool:
    """
    ClientPool maintains clients pool with max size or unlimited size,
    and it ensures thread / coroutine safe, new client will be created on demand.

    Usage:

    pool = ClientPool(rabbitmq_transport_factory, (rabbitmq_url, ), None, 8)

    # use `with` statement
    with pool.get() as client:
        reply = client.request('test')

    # or manually `fetch` and `put`
    try:
        client = pool.fetch()
        reply = client.request('test')
    finally:
        pool.put(client)

    # call `discard` if the client encountered error and can not be used any more.
    pool.discard(client)
    """

    DEFAULT_MAXSIZE = 100

    def __init__(
        self,
        client_factory,
        init_args=(),
        init_kwargs=None,
        maxsize=DEFAULT_MAXSIZE,
        expiry=None,
        client_close=None,
    ):
        """
        @param client_factory - Function to create the client object.
        @param init_args - Tuple.
            Non-keyworded variables for client_factory function
        @param init_kwargs - Dict.
            Keyworded variables for client_factory function
        @param maxsize - Int.
            The maximum size of the pool.
        @param expiry - Int. (in seconds)
            Client is not used for more than this many seconds will be discarded.
            None means clients won't be discarded at all.
        @param client_close - optional function to be called when client discarded
        """
        if init_kwargs is None:
            init_kwargs = {}
        self._client_factory = client_factory
        self._client_close = client_close
        self._init_args = init_args
        self._init_kwargs = init_kwargs
        self._maxsize = maxsize
        if self._maxsize is None or self._maxsize <= 0:
            self._maxsize = self.DEFAULT_MAXSIZE
        self._expiry = expiry
        self._clients = {}
        self._queue = deque()
        self._lock = threading.Lock()
        self._not_empty_cv = threading.Condition(self._lock)

    @contextmanager
    def get(self):
        client = self.fetch()
        try:
            yield client
        finally:
            self.put(client)

    def fetch(self):
        self._lock.acquire()
        while len(self._queue) <= 0:
            if len(self._clients) < self._maxsize:
                self._lock.release()
                client = self._client_factory(*self._init_args, **self._init_kwargs)
                self._lock.acquire()
                if len(self._clients) < self._maxsize:
                    self._clients[client] = 0
                    self._lock.release()
                    return client
            else:
                self._not_empty_cv.wait()

        current_ts = time.time()
        client = self._queue.popleft()
        # slowly reduce the size of pool when the load is low
        # reduce once at a time
        if self._expiry and len(self._queue) > 0:
            if current_ts - self._clients[client] >= self._expiry:
                del self._clients[client]
                client = self._queue.popleft()
                self._not_empty_cv.notify_all()

        self._lock.release()
        return client

    def put(self, client):
        with self._lock:
            if client in self._clients:
                self._queue.append(client)
                self._clients[client] = time.time()
                if len(self._queue) <= 1:
                    self._not_empty_cv.notify_all()

    def discard(self, client):
        with self._lock:
            if client in self._clients:
                del self._clients[client]
                self._not_empty_cv.notify_all()

    def discard_all(self, force_close=False):
        to_discard = []
        with self._lock:
            to_discard = list(self._clients)  # make a copy
            self._clients.clear()
            self._not_empty_cv.notify_all()

        if force_close and self._client_close:
            for client in to_discard:
                self._client_close(client)


class cached_property:
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    >>> class Frozen(object):
    ...     @cached_property
    ...     def random(self):
    ...         import random
    ...         return random.random()
    >>> frozen = Frozen()
    >>> assert frozen.random == frozen.random
    """

    def __init__(self, func):
        self.func = func
        self.__doc__ = getattr(func, "__doc__")
        self.name = func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = self.func(instance)
        instance.__dict__[self.name] = res
        return res


class retry:
    """Function decorator implementing retrying logic.

    delay: Sleep this many seconds * backoff * try number after failure
    backoff: Multiply delay by this factor after each failure
    exceptions: A tuple of exception classes; default (Exception,)
    hook: A function with the signature myhook(tries_remaining, exception);
          default None

    The decorator will call the function up to max_tries times if it raises
    an exception.

    By default, it catches instances of the Exception class and subclasses.
    This will recover after all but the most fatal errors. You may specify a
    custom tuple of exception classes with the 'exceptions' argument; the
    function will only be retried if it raises one of the specified
    exceptions.

    In certain cases, it makes sense to catch all exceptions except for certain
    exception classes and their subtypes. For example, a StopIteration exception
    may indicate the end of a generator rather than a truly exceptional case that
    ought to be retried. You may specify a custom tuple of exception classes that
    ought not be retried with the 'fatal_exceptions' argument.

    Additionally, you may specify a hook function which will be called prior
    to retrying with the number of remaining tries and the exception instance;
    see given example. This is primarily intended to give the opportunity to
    log the failure. Hook is not called after failure if no retries remain.
    """

    def __init__(
        self,
        max_tries=10,
        delay=5,
        backoff=1.3,
        max_delay=60,
        exceptions=(Exception,),
        fatal_exceptions=(StopIteration,),
        hook=None,
    ):
        self.max_delay = max_delay
        self.max_tries = max_tries
        self.delay = delay
        self.backoff = backoff
        self.exceptions = exceptions
        self.fatal_exceptions = fatal_exceptions
        self.hook = hook

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            mydelay = self.delay
            tries = list(range(self.max_tries - 1, -1, -1))
            for tries_remaining in tries:
                try:
                    return fn(*args, **kwargs)
                except self.fatal_exceptions:
                    raise
                except self.exceptions as e:
                    if tries_remaining > 0:
                        if self.hook is not None:
                            self.hook(tries_remaining, e, mydelay, fn.__name__)
                        sleep(min(mydelay, self.max_delay))
                        mydelay = mydelay * self.backoff
                    else:
                        raise

        return wrapper


def datetime_to_drtime_no_tz(dt):
    """Convert timestamp to common string representation that preserves lexicographical order
    with no timezone check

    >>> datetime_to_drtime_no_tz(datetime.datetime(2016, 12, 13, 11, 12, 13, 141516))
    '2016-12-13T11:12:13.141516Z'

    Parameters
    ----------
    dt : `datetime.datetime`

    Returns
    -------
    str
         String representation of timestamp
    """
    return "{:0>4}-{:0>2}-{:0>2}T{:0>2}:{:0>2}:{:0>2}.{:0>6}Z".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
    )


def drtime_to_datetime(drtime, ignore_warning=False):
    """Convert drtime-formatted strings into datetime objects

    Parameters
    ----------
    drtime : str
         String representation of datetime, e.g. '2016-12-13T11:12:13.141516Z'
    ignore_warning : bool
        Toggle logging when str input can be converted to datetime but is not a valid drtime string

    Returns
    -------
    datetime.datetime
    """
    try:
        return time.strptime(drtime, DRTIME_FORMAT)
    except ValueError:
        try:
            result = dateutil.parser.parse(drtime)
        except Exception:
            # We expect drtime objects to be produced by `datetime_to_drtime` and always be valid.
            # If you see this warning, drtime generation is probably broken and needs to be fixed.
            logger.warning(
                "drtime_to_datetime: couldn't read drtime",
                extra={"value": repr(drtime)},
                exc_info=True,
            )
            raise
        else:
            # We expect drtime objects to be produced by `datetime_to_drtime` and always be valid.
            # If you see this warning, we were able to parse drtime object, but the format wasn't
            # exactly the one we expected. This might be caused by:
            # * either a very old drtime object produced by a previous version of the application
            # * or the fact that drtime generation is broken and needs to be fixed
            if ignore_warning is False:
                extra = {"value": repr(drtime), "full_stack": traceback.format_stack()}
                logger.warning(
                    "drtime_to_datetime: dateutil.parser was used", extra=extra, exc_info=True
                )
            if result.tzinfo:
                return result.replace(tzinfo=None) - result.utcoffset()
            return result
