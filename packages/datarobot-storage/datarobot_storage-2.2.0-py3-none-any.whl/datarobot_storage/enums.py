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


class FileStorageBackend(object):
    LOCAL = "local"
    S3 = "s3"
    MEMORY = "memory"
    AZURE_BLOB = "azure_blob"
    GOOGLE = "google"

    @classmethod
    def all(cls):
        return {
            cls.LOCAL,
            cls.S3,
            cls.MEMORY,
            cls.AZURE_BLOB,
            cls.GOOGLE,
        }


class S3ServerSideEncryption(object):
    S3_SSE_AES = "AES256"
    S3_SSE_KMS = "aws:kms"
    DISABLED = "DISABLED"
