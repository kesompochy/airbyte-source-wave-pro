#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch

from .source import SourceYOUR_PACKAGE


def run():
    source = SourceYOUR_PACKAGE()
    launch(source, sys.argv[1:])
