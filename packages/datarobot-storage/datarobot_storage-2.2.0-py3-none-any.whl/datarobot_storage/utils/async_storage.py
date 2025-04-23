# -*- coding: utf-8 -*-
#
# Copyright 2024 DataRobot, Inc. and its affiliates.
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
from __future__ import absolute_import

import asyncio
import contextvars
import functools
from typing import Any

from datarobot_storage.base import AsyncStorage
from datarobot_storage.base import Storage

async_proxy_methods = [
    "client",
    "copy",
    "delete_all",
    "delete_batch",
    "delete",
    "exists",
    "exists_and_readable",
    "file_size",
    "get_generator",
    "move",
    "get",
    "get_seekable",
    "list",
    "put_generator",
    "put",
    "url",
]


def async_proxy_for(*attrs: str) -> Any:
    """Inject into wrapped class async proxy method for each of the attrs."""

    def cls_builder(cls: Any) -> Any:
        for attr_name in attrs:
            wrapper = _make_async_proxy(attr_name)
            functools.update_wrapper(wrapper, getattr(cls, attr_name))
            setattr(cls, attr_name, wrapper)
        return cls

    return cls_builder


def _make_async_proxy(attr_name: str) -> Any:
    """Return generated awaitable proxy method routing calls to the self._target."""

    async def async_proxy_method(self, *args, **kwargs):  # type: ignore[no-untyped-def]
        # asyncio.to_thread is only available in Python 3.9+, use low-level
        # in-place implementation here to make it compatible with Python 3.8
        ctx = contextvars.copy_context()
        loop = asyncio.events.get_running_loop()
        func = getattr(self._target, attr_name)
        runnable = functools.partial(ctx.run, func, *args, **kwargs)
        return await loop.run_in_executor(None, runnable)

    return async_proxy_method


@async_proxy_for(*async_proxy_methods)
class AsyncStorageWrapper(AsyncStorage):
    """Asynchronous wrapper for synchronous storage classes."""

    def __init__(self, target: Storage):
        self._target = target

    def __getattr__(self, item: Any) -> Any:
        """Call the target directly if the proxy method is not found.

        This method is executed only if __getattribute__ call fails to
        find the attribute in the proxy class. For the main use case
        (async method proxying), this won't be the case. These methods
        will be injected using the wrapper @async_proxy_for. However,
        for all other cases not injected into the proxy, the call will
        be forwarded using this method (i.e., properties, attributes,
        not proxied synchronous methods, etc.).
        """
        return getattr(self._target, item)
