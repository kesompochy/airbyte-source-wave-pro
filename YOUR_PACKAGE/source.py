#
# Copyright (c) 2024 Airbyte, Inc., all rights reserved.
#

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream


# Basic full refresh stream
class YOUR_PACKAGE_Stream(HttpStream, ABC):
    """
    Base stream class for your connector
    """

    @property
    def url_base(self) -> str:
        return self._url_base

    @abstractmethod
    def path(self, **kwargs) -> str:
        """
        Specify the path component of the API endpoint
        """
        pass

    def next_page_token(
        self, response: requests.Response
    ) -> Optional[Mapping[str, Any]]:
        """
        Override this method to define your pagination logic
        """
        return None

    def request_params(
        self,
        stream_state: Mapping[str, Any],
        stream_slice: Mapping[str, any] = None,
        next_page_token: Mapping[str, Any] = None,
    ) -> MutableMapping[str, Any]:
        """
        Override this method to define the query parameters
        """
        return {}

    def parse_response(
        self, response: requests.Response, **kwargs
    ) -> Iterable[Mapping]:
        """
        Override this method to define how to parse the response
        """
        yield {}


# Basic incremental stream
class IncrementalYOUR_PACKAGE_Stream(YOUR_PACKAGE_Stream, ABC):
    """
    Base class for incremental streams
    """

    state_checkpoint_interval = 500

    @property
    def cursor_field(self) -> str:
        """
        Override to return the cursor field for your stream
        """
        return "updated_at"  # example cursor field

    @property
    def supports_incremental(self) -> bool:
        return True

    def get_updated_state(
        self,
        current_stream_state: MutableMapping[str, Any],
        latest_record: Mapping[str, Any],
    ) -> Mapping[str, Any]:
        """
        Override to define how to update the stream state
        """
        latest_value = latest_record.get(self.cursor_field)
        current_value = current_stream_state.get(self.cursor_field)

        if current_value and latest_value:
            return {self.cursor_field: max(latest_value, current_value)}
        return {self.cursor_field: latest_value or current_value}


# Source
class SourceYOUR_PACKAGE(AbstractSource):
    def check_connection(self, logger, config) -> Tuple[bool, any]:
        """
        Override this method to implement connection checking
        """
        try:
            # Implement your connection check logic here
            return True, None
        except Exception as e:
            return False, str(e)

    def streams(self, config: Mapping[str, Any]) -> List[Stream]:
        """
        Override this method to return a list of stream instances
        """
        return []  # Return your stream instances here
