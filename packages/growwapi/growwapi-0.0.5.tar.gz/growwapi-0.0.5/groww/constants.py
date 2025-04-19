"""
Constants for the Groww API and Feed
"""

from typing import Final


class SubscriptionTopic:
    """
    A class to generate subscription topics for various market data feeds.
    """

    DERIVATIVES_LIVE_PRICES: Final[str] = (
        "/topic/stocks_fo/tr_live_prices/proto.symbol."
    )
    DERIVATIVES_LIVE_PRICES_DETAIL: Final[str] = (
        "/topic/stocks_fo/tr_live_prices_detail/proto.symbol."
    )
    DERIVATIVES_MARKET_DEPTH: Final[str] = "/topic/stocks_fo/tr_live_book/proto.symbol."
    DERIVATIVES_ORDER_UPDATES: Final[str] = "stocks_fo/order/updates.apex."
    DERIVATIVES_POSITION_UPDATES: Final[str] = "stocks_fo/position/updates.apex."
    EQUITY_LIVE_PRICES: Final[str] = "/topic/stocks/tr_live_prices/proto.symbol."
    EQUITY_LIVE_PRICES_DETAILED: Final[str] = (
        "/topic/stocks/tr_live_prices_detail/proto.symbol."
    )
    EQUITY_MARKET_DEPTH: Final[str] = "/topic/stocks/tr_live_book/proto.symbol."
    EQUITY_ORDER_UPDATES: Final[str] = "stocks/order/updates.apex."
    LIVE_INDEX: Final[str] = "/topic/stocks/tr_live_indices/proto.symbol."
    MARKET_INFO: Final[str] = "/topic/proto/market_info"

    @staticmethod
    def get_derivatives_ltp_topic(subscription_key: str) -> str:
        """
        Get the derivatives live trading price topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The derivatives live trading price topic.
        """
        return f"{SubscriptionTopic.DERIVATIVES_LIVE_PRICES}{subscription_key}"

    @staticmethod
    def get_derivatives_ltp_detail_topic(subscription_key: str) -> str:
        """
        Get the derivatives live trading price detail topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The derivatives live trading price detail topic.
        """
        return f"{SubscriptionTopic.DERIVATIVES_LIVE_PRICES_DETAIL}{subscription_key}"

    @staticmethod
    def get_derivatives_market_depth_topic(subscription_key: str) -> str:
        """
        Get the derivatives market depth topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The derivatives market depth topic.
        """
        return f"{SubscriptionTopic.DERIVATIVES_MARKET_DEPTH}{subscription_key}"

    @staticmethod
    def get_derivatives_order_updates_topic(subscription_key: str) -> str:
        """
        Get the derivatives order updates topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The derivatives order updates topic.
        """
        return f"{SubscriptionTopic.DERIVATIVES_ORDER_UPDATES}{subscription_key}"
    
    @staticmethod
    def get_derivatives_position_updates_topic(subscription_key: str) -> str:
        """
        Get the derivatives position updates topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The derivatives position updates topic.
        """
        return f"{SubscriptionTopic.DERIVATIVES_POSITION_UPDATES}{subscription_key}"

    @staticmethod
    def get_equity_ltp_topic(subscription_key: str) -> str:
        """
        Get the equity live trading price topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The equity live trading price topic.
        """
        return f"{SubscriptionTopic.EQUITY_LIVE_PRICES}{subscription_key}"

    @staticmethod
    def get_equity_ltp_detailed_topic(subscription_key: str) -> str:
        """
        Get the equity live trading price detailed topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The equity live trading price detailed topic.
        """
        return f"{SubscriptionTopic.EQUITY_LIVE_PRICES_DETAILED}{subscription_key}"

    @staticmethod
    def get_equity_market_depth_topic(subscription_key: str) -> str:
        """
        Get the equity market depth topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The equity market depth topic.
        """
        return f"{SubscriptionTopic.EQUITY_MARKET_DEPTH}{subscription_key}"

    @staticmethod
    def get_equity_order_updates_topic(subscription_key: str) -> str:
        """
        Get the equity order updates topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The order updates topic.
        """
        return f"{SubscriptionTopic.EQUITY_ORDER_UPDATES}{subscription_key}"

    @staticmethod
    def get_index_ltp_topic(subscription_key: str) -> str:
        """
        Get the live index trading price topic.

        Args:
            subscription_key (str): The subscription key.

        Returns:
            str: The live index trading price topic.
        """
        return f"{SubscriptionTopic.LIVE_INDEX}{subscription_key}"

    @staticmethod
    def get_market_info_topic() -> str:
        """
        Get the market info topic.

        Returns:
            str: The market info topic.
        """
        return SubscriptionTopic.MARKET_INFO


class Parameters:
    # AMO Status constants
    AMO_STATUS_NA = "NA"
    AMO_STATUS_PENDING = "PENDING"
    AMO_STATUS_DISPATCHED = "DISPATCHED"
    AMO_STATUS_PARKED = "PARKED"
    AMO_STATUS_PLACED = "PLACED"
    AMO_STATUS_FAILED = "FAILED"
    AMO_STATUS_MARKET = "MARKET"

    # Validity constants
    VALIDITY_DAY = "DAY"
    VALIDITY_EOS = "EOS"
    VALIDITY_IOC = "IOC"
    VALIDITY_GTC = "GTC"
    VALIDITY_GTD = "GTD"

    # EquityType constants
    EQUITY_TYPE_STOCKS = "STOCKS"
    EQUITY_TYPE_FUTURE = "FUTURE"
    EQUITY_TYPE_OPTION = "OPTION"
    EQUITY_TYPE_ETF = "ETF"
    EQUITY_TYPE_INDEX = "INDEX"
    EQUITY_TYPE_BONDS = "BONDS"

    # Exchange constants
    EXCHANGE_BSE = "BSE"
    EXCHANGE_MCX = "MCX"
    EXCHANGE_MCXSX = "MCXSX"
    EXCHANGE_NCDEX = "NCDEX"
    EXCHANGE_NSE = "NSE"
    EXCHANGE_US = "US"

    # OrderStatus constants
    ORDER_STATUS_ACKED = "ACKED"
    ORDER_STATUS_APPROVED = "APPROVED"
    ORDER_STATUS_CANCELLATION_REQUESTED = "CANCELLATION_REQUESTED"
    ORDER_STATUS_CANCELLED = "CANCELLED"
    ORDER_STATUS_COMPLETED = "COMPLETED"
    ORDER_STATUS_DELIVERY_AWAITED = "DELIVERY_AWAITED"
    ORDER_STATUS_EXECUTED = "EXECUTED"
    ORDER_STATUS_FAILED = "FAILED"
    ORDER_STATUS_MODIFICATION_REQUESTED = "MODIFICATION_REQUESTED"
    ORDER_STATUS_NEW = "NEW"
    ORDER_STATUS_REJECTED = "REJECTED"
    ORDER_STATUS_TRIGGER_PENDING = "TRIGGER_PENDING"

    # OrderType constants
    ORDER_TYPE_LIMIT = "LIMIT"
    ORDER_TYPE_MARKET = "MARKET"
    ORDER_TYPE_STOP_LOSS = "SL"
    ORDER_TYPE_STOP_LOSS_MARKET = "SL-M"

    # Product constants
    PRODUCT_ARBITRAGE = "ARB"
    PRODUCT_BO = "BO"
    PRODUCT_CNC = "CNC"
    PRODUCT_CO = "CO"
    PRODUCT_NORMAL_MARGIN = "NRML"
    PRODUCT_MIS = "MIS"
    PRODUCT_MTF = "MTF"

    # Segment constants
    SEGMENT_CASH = "CASH"
    SEGMENT_CURRENCY = "CURRENCY"
    SEGMENT_COMMODITY = "COMMODITY"
    SEGMENT_DERIVATIVE = "FNO"

    # TransactionType constants
    TRANSACTION_TYPE_BUY = "BUY"
    TRANSACTION_TYPE_SELL = "SELL"