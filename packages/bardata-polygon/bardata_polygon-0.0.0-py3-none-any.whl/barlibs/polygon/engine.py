# price engine

import logging
import pandas as pd

from functools import lru_cache, cached_property

from polygon.rest import RESTClient

from bardata import model

from . import utils


MAXBARS = 5000
MAXLIMIT = 50000

logger = logging.getLogger(__name__)


@lru_cache
def polygon_engine():
    """Polygon.io price engine factory function"""
    return PolygonPrices()


class PolygonPrices(model.PriceEngine):
    """Polygon.io price engine"""

    @cached_property
    def client(self):
        return RESTClient()

    def get_prices(self, ticker, freq="daily", start_date=None, end_date=None, max_bars=None, adjusted=True):
        """
        Get prices from Polygon.io
        
        Returns:
            Prices dataframe or None
        """

        if max_bars is None:
            max_bars = MAXBARS

        start_date, end_date = utils.fix_dates(start_date, end_date, freq=freq, periods=max_bars)

        multiplier, timespan = utils.map_frequency(freq)

        limit = MAXLIMIT
        sort = 'desc'

        kwds = {'ticker': ticker,
                'multiplier': multiplier,
                'timespan': timespan,
                'from_': start_date,
                'to': end_date,
                'adjusted': adjusted,
                'sort': sort,
                'limit': limit}
        
        logger.debug("kwds %s", kwds)

        # get_aggs has no pagination. use list_aggs for pagination ! 
        aggs = list(self.client.list_aggs(**kwds))

        if not aggs:
            logger.debug("No data found for %s", ticker)
            return None

        prices = pd.DataFrame.from_records(map(vars, aggs))

        prices['datetime'] = pd.to_datetime(prices.timestamp, unit="ms", utc=True)
        prices = prices.set_index('datetime').sort_index()
        prices = prices.filter(["open", "high", "low", "close", "volume", "vwap"])

        if max_bars:
            prices = prices.tail(max_bars)

        return prices

