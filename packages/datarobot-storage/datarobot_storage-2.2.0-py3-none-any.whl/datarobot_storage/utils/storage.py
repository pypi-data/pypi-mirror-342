# Copyright 2023 DataRobot, Inc. and its affiliates.
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

from __future__ import absolute_import
from __future__ import division

import errno
import logging
import os
import tempfile

logger = logging.getLogger(__name__)


def try_file_remove(local_filename):
    try:
        os.remove(local_filename)
    except OSError as e:
        if e.errno != errno.ENOENT:
            logger.error("Failed to remove local file", extra={'file_name': local_filename})
            return False
    return True


def safe_make_dir(path):
    if not path:
        logger.warning('Attempted to create invalid dir', extra={'file_path': path})
        return

    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError as error:
            if error.errno == errno.EEXIST:
                # Ignore race condition where another process may have created
                # this directory already
                pass
            else:
                logger.warning(
                    'Could not create directory', extra={'file_path': path}, exc_info=True
                )
                raise


def new_tempfile(path=None, file_path=False, suffix=''):
    """
    Get a local tempfile name

    Parameters
    ----------
    path : str, optional
        If specified, indicate where data should be stored on this system
    suffix : str, optional
        If specified, then the file name will end with that suffix
    file_path : bool, optional
        if True, then `path` is the filepath, and new file will be created in the parent directory:
        >>> new_tempfile('/tmp/path/to/some/file', file_path=True)  # doctest: +SKIP
        '/tmp/path/to/some/tmpGCQomM'
        otherwise, `path` will be treated as a directory path
        >>> new_tempfile('/tmp/path/to/some/file', file_path=False)  # doctest: +SKIP
        '/tmp/path/to/some/file/tmpMMSYYr'

    Returns
    -------
    filename : str
        A newly created path to a file in the data_dir
    """
    if path is None:
        path = tempfile.gettempdir()
    if file_path:
        path = os.path.dirname(path)

    safe_make_dir(path)
    tf = tempfile.NamedTemporaryFile(mode='w', delete=False, dir=path, suffix=suffix)
    tf.close()
    return tf.name


class StorageUtilsMixin(object):
    # Utility methods for Storage implementations.

    def removeprefix(self, string, prefix=None):
        prefix = prefix or getattr(self, 'prefix', '')
        index = 0
        if string.startswith(prefix):
            index = len(prefix)
        return string[index:]

    def name_list_chunks(self, name_iter, batch_size):
        sub_list = []
        for name in name_iter:
            sub_list.append(name)
            if len(sub_list) == batch_size:
                yield sub_list
                sub_list = []
        if sub_list:
            yield sub_list
