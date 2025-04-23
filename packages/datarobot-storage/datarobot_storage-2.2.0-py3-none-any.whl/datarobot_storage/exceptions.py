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

from botocore.exceptions import ClientError as BotoClientError


class ClientError(BotoClientError):
    """
    Indicates a problem with authentication or encryption settings.

    Use this to wrap `botocore.exceptions.ClientError` before re-raising them to calling code.
    """


def wrap_client_error(exc: BotoClientError) -> ClientError:
    """
    Construct `datarobot_storage.exception.ClientError` from `botocore.exceptions.ClientError`
    """
    return ClientError(operation_name=exc.operation_name, error_response=exc.response)
