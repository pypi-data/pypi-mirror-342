"""
The module provides classes to subscribe to the Groww feed and get the feed data.
"""

import threading
import os
import nacl.signing
import nkeys
from typing import Callable, Optional, Final, Type
from google.protobuf.json_format import MessageToDict

from growwapi.groww.exceptions import GrowwFeedNotSubscribedException
from growwapi.groww.nats_client import NatsClient
from growwapi.groww.constants import SubscriptionTopic
from growwapi.groww.proto.stocks_socket_response_pb2 import (
    StocksSocketResponseProtoDto,
    StocksMarketInfoProto,
)
from growwapi.groww.proto.position_socket_pb2 import (
    PositionDetailProto,
)
from growwapi.groww.proto.stock_orders_socket_response_pb2 import (
    OrderDetailsBroadCastDto,
)
from growwapi.groww.client import GrowwAPI

import requests
import uuid

from growwapi.groww.exceptions import (
    GrowwAPIException,
    GrowwAPITimeoutException,
    GrowwAPIAuthenticationException,
    GrowwAPIAuthorisationException,
    GrowwAPIBadRequestException,
    GrowwAPINotFoundException,
    GrowwAPIRateLimitException,
)


class Feed:
    """
    Feed class to store data for a given topic.
    """

    def __init__(
        self,
        topic: str,
        on_update: Optional[Callable[[], None]] = None,
    ) -> None:
        """Initialize a Feed with a topic and no data.

        Args:
            topic (str): The topic of the feed.
            on_update (Optional[Callable[[], None]]): The callback function to call on data update.
        """
        self.topic: str = topic
        self.on_update: Optional[Callable[[], None]] = on_update
        self.data: Optional[any] = None
        self._data_event: threading.Event = threading.Event()

    def update(self, data: any) -> None:
        """Update the feed with new data.

        Args:
            data (any): The new data for the feed.
        """
        self.data = data
        self._data_event.set()
        self.on_update() if self.on_update else None

    def get_data(self, timeout: float) -> Optional[any]:
        """Retrieve the data from the feed, waiting up to the specified timeout.

        Args:
            timeout (float): The maximum time to wait for data, in seconds.

        Returns:
            Optional[any]: The data if available, else None.
        """
        data_available = self._data_event.wait(timeout)
        return self.data if data_available else None

    def get_topic(self) -> str:
        """Retrieve the topic of the feed.

        Returns:
            str: The topic of the feed.
        """
        return self.topic


class FeedStation:
    """
    FeedStation class to store feeds for various topics.
    """

    def __init__(self) -> None:
        """Initialize a FeedStation with an empty feed dictionary."""
        self.feed_dict: dict[str, Feed] = {}

    def add_feed(self, key: str, feed: Feed) -> None:
        """Add a feed to the feed dictionary.

        Args:
            key (str): The key for the feed.
            feed (Feed): The feed object to add.
        """
        self.feed_dict[key] = feed

    def get_feed(self, key: str) -> Optional[Feed]:
        """Retrieve a feed from the feed dictionary.

        Args:
            key (str): The key for the feed.

        Returns:
            Optional[Feed]: The feed object if found, else None.
        """
        return self.feed_dict.get(key)

    def remove_feed(self, key: str) -> None:
        """Remove a feed from the feed dictionary.

        Args:
            key (str): The key for the feed to remove.
        """
        self.feed_dict.pop(key, None)


class GrowwFeed:
    """
    Used to subscribe to the Groww feed and get the feed data.

    One instance of GrowwFeed can be used to subscribe to multiple topics and get the feed data.

    Note:
        Only one subscription can be created to each topic by a single instance of GrowwFeed.
    """

    _GROWW_SOCKET_URL: Final[str] = "wss://socket-api.groww.in"
    _GROWW_GENERATE_SOCKET_TOKEN_URL: Final[str] = "https://api.groww.in/v1/api/apex/v1/socket/token/create/"
    _nats_clients: dict[tuple[str, str], NatsClient] = {}

    def __init__(self, token: str) -> None:
        """
        Initialize the GrowwFeed class with socket token and key.

        Args:
            token (str): The token for Groww API.

        Raises:
            GrowwFeedConnectionException: If the socket connection fails.
        """
        self.token = token
        self._feed_station: FeedStation = FeedStation()
        self.seed_size_in_bytes: int = 32
        self.seed = os.urandom(self.seed_size_in_bytes)
        self.key_pair = self._generate_nkey_pair_from_seed()
        self.socket_token_response = self._generate_socket_token()
        self.socket_jwt_token = self.socket_token_response["token"]
        self.subscription_id = self.socket_token_response["subscriptionId"]
        self._client_key = (
            self.socket_jwt_token, 
            self.key_pair.seed.decode("utf-8")
        )
        if self._client_key not in GrowwFeed._nats_clients:
            GrowwFeed._nats_clients[self._client_key] = NatsClient(
                GrowwFeed._GROWW_SOCKET_URL,
                self._client_key[0],
                self._client_key[1],
                self._update_feed_data,
            )
        self._nats_client = GrowwFeed._nats_clients[self._client_key]

        self.segment_subscription_map = {
            GrowwAPI.SEGMENT_CASH: {
                "subscribe_live_data": self.__subscribe_stocks_live,
                "unsubscribe_live_data": self.__unsubscribe_stocks_live,
                "subscribe_market_depth": self.__subscribe_stocks_market_depth,
                "unsubscribe_market_depth": self.__unsubscribe_stocks_market_depth,
            },
            GrowwAPI.SEGMENT_FNO: {
                "subscribe_live_data": self.__subscribe_derivatives_live,
                "unsubscribe_live_data": self.__unsubscribe_derivatives_live,
                "subscribe_market_depth": self.__subscribe_derivatives_market_depth,
                "unsubscribe_market_depth": self.__unsubscribe_derivatives_market_depth,
            },
        }
    
    def _get_subscription_function(self, segment: str, action: str) -> Callable:
        if segment not in self.segment_subscription_map:
            raise ValueError(f"Invalid segment '{segment}'.")
        return self.segment_subscription_map[segment].get(action)

    def _generate_nkey_pair_from_seed(self) -> nkeys.KeyPair:
        signing_key = nacl.signing.SigningKey(self.seed)
        key_pair = nkeys.KeyPair(keys=signing_key, seed=nkeys.encode_seed(self.seed, nkeys.PREFIX_BYTE_USER))
        return key_pair

    def _generate_socket_token(self) -> str:
        headers = self._build_headers()
        request_body = {
            "socketKey" : self.key_pair.public_key.decode("utf-8"),
        }
        response = self._request_post(
            url=self._GROWW_GENERATE_SOCKET_TOKEN_URL,
            json=request_body,
            headers=headers,
        )
        return self._parse_response(response)
    
    def subscribe_live_data(
        self,
        segment: str,
        feed_keys: list[str],
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> dict[str, bool]:
        """
        Subscribe to the live data.

        Subscription can be created only once for a given feed key.

        Args:
            segment(str): The segment of the instrument corresponding to feed keys.
            feed_keys (list[str]): The list of feed keys.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            dict[str, bool] : True if a new subscription was created, False otherwise.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        subscribe_func = self._get_subscription_function(segment, "subscribe_live_data")        
        return {key: subscribe_func(key, on_data_received) for key in feed_keys}
    
    def unsubscribe_live_data(
        self, 
        segment: str,
        feed_keys: list[str],
    ) -> dict[str, bool]:
        """
        Unsubscribe from the live data.

        Args:
            segment(str): The segment of the instrument corresponding to feed keys.
            feed_keys (list[str]): The list of feed keys.

        Returns:
            dict[str, bool]: True if existing subscription was unsubscribed, False otherwise.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        unsubscribe_func = self._get_subscription_function(segment, "unsubscribe_live_data")
        return {key: unsubscribe_func(key) for key in feed_keys}
    
    def subscribe_indices_live(
        self,
        feed_keys: list[str],
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> dict[str, bool]:
        """
        Subscribe to the live data of indices.

        Subscription can be created only once for a given feed key.

        Args:
            feed_keys (list[str]): The list of feed keys.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            dict[str, bool]: True if a new subscription was created, False otherwise.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        return {key: self.__subscribe_indices_live(key, on_data_received) for key in feed_keys}
    
    def unsubscribe_indices_live(self, feed_keys: list[str]) -> dict[str, bool]:
        """
        Unsubscribe from the live data of indices.

        Args:
            feed_keys (list[str]): The list of feed keys.

        Returns:
            dict[str, bool]: True if existing subscription was unsubscribed, False otherwise.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        return {key: self.__unsubscribe_indices_live(key) for key in feed_keys}
    
    def subscribe_market_depth(
        self,
        segment: str,
        feed_keys: list[str],
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> dict[str, bool]:
        """
        Subscribe to the market depth.

        Subscription can be created only once for a given feed key.

        Args:
            segment(str): The segment of the instrument corresponding to feed keys.
            feed_keys (list[str]): The list of feed keys.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            dict[str, bool]: True if a new subscription was created, False otherwise.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")

        subscribe_func = self._get_subscription_function(segment, "subscribe_market_depth")
        return {key: subscribe_func(key, on_data_received) for key in feed_keys}

    def unsubscribe_market_depth(
        self,
        segment: str,
        feed_keys: list[str],
    ) -> dict[str, bool]:
        """
        Unsubscribe from the market depth.

        Args:
            segment(str): The segment of the instrument corresponding to feed keys.
            feed_keys (list[str]): The list of feed keys.

        Returns:
            dict[str, bool]: True if existing subscription was unsubscribed, False otherwise.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        unsubscribe_func = self._get_subscription_function(segment, "unsubscribe_market_depth")
        return {key: unsubscribe_func(key) for key in feed_keys}

    def subscribe_order_updates(
        self,
        segment: str,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the order updates.

        Subscription can be created only once for a given feed key.

        Args:
            segment (str): The segment of the stock.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        if (segment == GrowwAPI.SEGMENT_CASH):
            return self.__subscribe_stocks_order_updates(on_data_received)
        elif (segment == GrowwAPI.SEGMENT_FNO):
            return self.__subscribe_derivatives_order_updates(on_data_received)
        else:
            return False
    
    def unsubscribe_order_updates(self, segment: str) -> bool:
        """
        Unsubscribe from the order updates.

        Args:
            segment(str): The segment of the stock.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        if (segment == GrowwAPI.SEGMENT_CASH):
            return self.__unsubscribe_stocks_order_updates()
        elif (segment == GrowwAPI.SEGMENT_FNO):
            return self.__unsubscribe_derivatives_order_updates()
        else:
            return False
    
    def subscribe_derivatives_position_updates(
        self,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the position updates of a derivatives contract.

        Subscription can be created only once for a given feed key.

        Args:
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_derivatives_position_updates_topic(self.subscription_id),
            on_data_received,
        )

    def unsubscribe_derivatives_position_updates(
        self,
    ) -> bool:
        """
        Unsubscribe from the position updates of a derivatives contract.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_derivatives_position_updates_topic(self.subscription_id),
        )


    def __subscribe_derivatives_live(
        self,
        feed_key: str,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the live data of a derivatives contract.

        Subscription can be created only once for a given feed key.

        Args:
            feed_key (str): The feed key.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_derivatives_ltp_topic(feed_key),
            on_data_received,
        )


    def __unsubscribe_derivatives_live(self, feed_key: str) -> bool:
        """
        Unsubscribe from the live data of a derivatives contract.

        Args:
            feed_key (str): The feed key.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_derivatives_ltp_topic(feed_key)
        )

    def __subscribe_derivatives_market_depth(
        self,
        feed_key: str,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the market depth of a derivatives contract.

        Subscription can be created only once for a given feed key.

        Args:
            feed_key (str): The feed key.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_derivatives_market_depth_topic(feed_key),
            on_data_received,
        )

    def __unsubscribe_derivatives_market_depth(self, feed_key: str) -> bool:
        """
        Unsubscribe from the market depth of a derivatives contract.

        Args:
            feed_key (str): The feed key.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_derivatives_market_depth_topic(feed_key)
        )

    def __subscribe_derivatives_order_updates(
        self,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the order updates of a derivatives contract.

        Subscription can be created only once for a given feed key.

        Args:
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_derivatives_order_updates_topic(self.subscription_id),
            on_data_received,
        )

    def __unsubscribe_derivatives_order_updates(self) -> bool:
        """
        Unsubscribe from the order updates of a derivatives contract.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_derivatives_order_updates_topic(self.subscription_id),
        )
    
    def __subscribe_indices_live(
        self,
        feed_key: str,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the live data of an index.

        Args:
            feed_key (str): The feed key.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_index_ltp_topic(feed_key),
            on_data_received,
        )
    
    def __unsubscribe_indices_live(self, feed_key: str) -> bool:
        """
        Unsubscribe from the live data of an index.

        Args:
            feed_key (str): The feed key.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_index_ltp_topic(feed_key)
        )

    def subscribe_market_info(
        self,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the market information.

        Subscription can be created only once for a given feed key.

        Args:
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_market_info_topic(),
            on_data_received,
        )

    def unsubscribe_market_info(self) -> bool:
        """
        Unsubscribe from the market information.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(SubscriptionTopic.get_market_info_topic())

    def __subscribe_stocks_live(
        self,
        feed_key: str,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the live data of a stock.

        Subscription can be created only once for a given feed key.

        Args:
            feed_key (str): The feed key.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_equity_ltp_topic(feed_key),
            on_data_received,
        )

    def __unsubscribe_stocks_live(self, feed_key: str) -> bool:
        """
        Unsubscribe from the live data of a stock.

        Args:
            feed_key (str): The feed key.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_equity_ltp_topic(feed_key),
        )

    def __subscribe_stocks_market_depth(
        self,
        feed_key: str,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the market depth of a stock.

        Subscription can be created only once for a given feed key.

        Args:
            feed_key (str): The feed key.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_equity_market_depth_topic(feed_key),
            on_data_received,
        )

    def __unsubscribe_stocks_market_depth(self, feed_key: str) -> bool:
        """
        Unsubscribe from the market depth of a stock.

        Args:
            feed_key (str): The feed key.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_equity_market_depth_topic(feed_key)
        )

    def __subscribe_stocks_order_updates(
        self,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to the order updates of a stock.

        Subscription can be created only once for a given feed key.

        Args:
            feed_key (str): The feed key.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        return self._subscribe(
            SubscriptionTopic.get_equity_order_updates_topic(self.subscription_id),
            on_data_received,
        )

    def __unsubscribe_stocks_order_updates(self) -> bool:
        """
        Unsubscribe from the order updates of a stock.

        Returns:
            bool: True if existing subscription was unsubscribed, False otherwise.
        """
        return self._unsubscribe(
            SubscriptionTopic.get_equity_order_updates_topic(self.subscription_id),
        )

    def get_derivatives_live(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the live data of derivatives contracts.

        Args:
            feed_key (str): The feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The live price data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_derivatives_live(key, timeout) for key in feed_keys}
    
    def __get_derivatives_live(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the live data of a derivatives contract.

        Args:
            feed_key (str): The feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The live price data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_derivatives_ltp_topic(feed_key),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, StocksSocketResponseProtoDto)
        return self._transform_proto_data_to_dict(proto_data.stockLivePrice)
    
    def get_derivatives_ltp(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the last traded price (LTP) of derivatives contracts.

        Args:
            feed_key (str): The feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The live price data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_derivatives_ltp(key, timeout) for key in feed_keys}
    
    def __get_derivatives_ltp(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[float]:
        """
        Get the last traded price (LTP) of a derivatives contract.

        Args:
            feed_key (str): The feed key.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[float]: The last traded price, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data: Optional[dict[str, any]] = self.__get_derivatives_live(feed_key, timeout)
        return data.get("ltp") if data else None

    def get_derivatives_market_depth(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the market depth of derivatives contracts.

        Args:
            feed_keys (list[str]): The list of feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The market depth data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_derivatives_market_depth(key, timeout) for key in feed_keys}

    def __get_derivatives_market_depth(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the market depth of a derivatives contract.

        Args:
            feed_key (str): The feed key.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The market depth data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_derivatives_market_depth_topic(feed_key),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, StocksSocketResponseProtoDto)
        return self._transform_proto_data_to_dict(proto_data.stocksMarketDepth)

    def get_derivatives_order_update(
        self,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the order updates of a derivatives contract.

        Args:
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The order details, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_derivatives_order_updates_topic(self.subscription_id),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, OrderDetailsBroadCastDto)
        return self._transform_proto_data_to_dict(proto_data.orderDetailUpdateDto)

    def get_derivatives_position_update(
        self,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the position updates of a derivatives contract.

        Args:
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The exchange wise position, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_derivatives_position_updates_topic(self.subscription_id),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, PositionDetailProto)
        return {
            "symbolIsin": proto_data.positionInfo.symbolIsin,
            "exchangePosition": {
                'BSE': self._transform_proto_data_to_dict(
                    proto_data.positionInfo.BSE
                ),
                'NSE': self._transform_proto_data_to_dict(
                    proto_data.positionInfo.NSE
                ),
            },
        }

    def get_indices_live(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the live data of indices.

        Args:
            feed_keys (list[str]): The list of feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The live index data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_index_live(key, timeout) for key in feed_keys}

    def __get_index_live(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the live data of an index.

        Args:
            feed_key (str): The feed key.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The live index data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_index_ltp_topic(feed_key),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, StocksSocketResponseProtoDto)
        return self._transform_proto_data_to_dict(proto_data.stocksLiveIndices)
    
    def get_indices_value(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the last value of indices.

        Args:
            feed_keys (list[str]): The list of feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The last value of the indices, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_index_value(key, timeout) for key in feed_keys}

    def __get_index_value(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[float]:
        """
        Get the last value of an index.

        Args:
            feed_key (str): The feed key.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[float]: The last value of the index, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data: Optional[dict[str, any]] = self.__get_index_live(feed_key, timeout)
        return data.get("value") if data else None


    def get_market_info(self, timeout: float = 5) -> Optional[str]:
        """
        Get the market information.

        Args:
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[str]: The market information, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(SubscriptionTopic.get_market_info_topic(), timeout)
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, StocksMarketInfoProto)
        return proto_data.message

    def get_stocks_live(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the live data of stocks.

        Args:
            feed_keys (list[str]): The list of feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The live price data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_stock_live(key, timeout) for key in feed_keys}

    def __get_stock_live(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the live data of a stock.

        Args:
            feed_key (str): The feed key.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The live price data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_equity_ltp_topic(feed_key),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, StocksSocketResponseProtoDto)
        return self._transform_proto_data_to_dict(proto_data.stockLivePrice)

    def get_stocks_ltp(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the last traded price (LTP) of stocks.

        Args:
            feed_keys (list[str]): The list of feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The last traded price, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_stock_ltp(key, timeout) for key in feed_keys}

    def __get_stock_ltp(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[float]:
        """
        Get the last traded price (LTP) of a stock.

        Args:
            feed_key (str): The feed key.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[float]: The last traded price, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data: Optional[dict[str, any]] = self.__get_stock_live(feed_key, timeout)
        return data.get("ltp") if data else None

    def get_stocks_market_depth(
        self,
        feed_keys: list[str],
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the market depth of stocks.

        Args:
            feed_keys (list[str]): The list of feed keys.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The market depth data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        if not isinstance(feed_keys, list) or not all(isinstance(key, str) for key in feed_keys):
            raise TypeError("feed_keys must be a list of strings.")
        if not feed_keys:
            raise ValueError("At least one feed key must be provided")
        
        return {key: self.__get_stock_market_depth(key, timeout) for key in feed_keys}

    def __get_stock_market_depth(
        self,
        feed_key: str,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the market depth of a stock.

        Args:
            feed_key (str): The feed key.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The market depth data, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_equity_market_depth_topic(feed_key),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, StocksSocketResponseProtoDto)
        return self._transform_proto_data_to_dict(proto_data.stocksMarketDepth)

    def get_stocks_order_update(
        self,
        timeout: float = 5,
    ) -> Optional[dict[str, any]]:
        """
        Get the order updates of a stock.

        Args:
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[dict[str, any]]: The order details, or None if data is not available.

        Raises:
            GrowwFeedNotSubscribedException: If the feed was not subscribed before attempting to get.
        """
        data = self._get_feed(
            SubscriptionTopic.get_equity_order_updates_topic(self.subscription_id),
            timeout,
        )
        if data is None:
            return None

        proto_data = self._parse_data_to_proto_model(data, OrderDetailsBroadCastDto)
        return self._transform_proto_data_to_dict(proto_data.orderDetailUpdateDto)

    def _update_feed_data(self, topic: str, data: any) -> None:
        """
        Update the feed data for a given topic.

        Args:
            topic (str): The feed key.
            data (any): The data to update.
        """
        self._feed_station.get_feed(topic).update(data)

    def _subscribe(
        self,
        topic: str,
        on_data_received: Optional[Callable[[], None]] = None,
    ) -> bool:
        """
        Subscribe to a given topic.

        Subscription can be created only once for a given topic.

        Args:
            topic (str): The topic to subscribe to.
            on_data_received (Optional[Callable[[], None]]): The callback function to call on data update.

        Returns:
            bool: True if a new subscription was created, False otherwise.
        """
        if self._nats_client.is_subscribed(topic):
            return False

        self._feed_station.add_feed(topic, Feed(topic, on_data_received))
        return self._nats_client.subscribe_topic(topic)

    def _unsubscribe(self, topic: str) -> bool:
        """
        Unsubscribe from a given topic.

        Args:
            topic (str): The topic to unsubscribe from.

        Returns:
            bool: True if unsubscribed, else False.
        """
        if not self._nats_client.is_subscribed(topic):
            return False

        is_unsubed: bool = self._nats_client.unsubscribe_topic(topic)
        self._feed_station.remove_feed(topic)
        return is_unsubed

    def _get_feed(self, topic: str, timeout: float) -> Optional[any]:
        """
        Get the feed for a given subscription topic.

        Args:
            topic (str): The subscription topic.
            timeout (float): The timeout in seconds for getting the data.

        Returns:
            Optional[any]: The feed data if available, else None.

        Raises:
            GrowwFeedNotSubscribedException: If the feed is not subscribed.
        """
        feed: Feed = self._feed_station.get_feed(topic)
        if not feed:
            raise GrowwFeedNotSubscribedException(
                f"Feed not subscribed for topic! A subscription is required to get the data.",
                topic,
            )
        return feed.get_data(timeout)

    def _parse_data_to_proto_model(
        self,
        data: any,
        proto: Type[any],
    ) -> any:
        """
        Parse the proto object to the model object.

        Args:
            data (any): The data to parse.
            proto (Type): The proto class.
        """
        proto_object = proto()
        proto_object.ParseFromString(data)
        return proto_object

    def _transform_proto_data_to_dict(self, proto_data: any) -> dict[str, any]:
        """
        Parse the proto object to the model object.

        Args:
            proto_data (any): The data to parse.
            model (Type[BaseGrowwModel]): The model class.

        Returns:
            dict[str, any]: The model object.
        """
        return MessageToDict(proto_data, preserving_proto_field_name=True)
    
    def _build_headers(self) -> dict:
        return {
            "x-request-id": str(uuid.uuid4()),
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }

    def _request_post(
        self,
        url: str,
        json: dict = None,
        headers: dict = None,
        timeout: Optional[int] = None,
        **kwargs: any,
    ) -> requests.Response:
        try:
            return requests.post(
                url=url,
                json=json,
                headers=headers,
                timeout=timeout,
                **kwargs,
            )
        except requests.Timeout as e:
            raise GrowwAPITimeoutException() from e

    def _parse_response(self, response: requests.Response) -> dict:
        response_map = response.json()
        if response_map.get("status") == "FAILURE":
            error = response_map["error"]
            raise GrowwAPIException(code=error["code"], msg=error["message"])
        if response.status_code == 401:
            raise GrowwAPIAuthenticationException()
        if response.status_code == 404:
            raise GrowwAPINotFoundException()
        if response.status_code == 429:
            raise GrowwAPIRateLimitException()
        if response.status_code == 504:
            raise GrowwAPITimeoutException()
        if not response.ok:
            raise GrowwAPIException(
                code=str(response.status_code),
                msg="The request to the Groww API failed.",
            )
        return response_map
