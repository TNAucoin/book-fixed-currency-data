"""
Fixer.io Currency Exchange Rate Integration for Kognitos.

This integration provides access to real-time currency exchange rates via the Fixer.io API.
Supports 170+ world currencies with conversion, rate lookup, and currency information.
"""

import logging

import requests
from kognitos.bdk.decorators import book, procedure

FIXED_CURRENCY_DATA_BASE_URL = "https://data.fixer.io/api"
DEFAULT_TIMEOUT = 30

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@book(name="Fixer", icon="data/icon.svg")
class FixedCurrencyDataBook:
    """
    A book for accessing real-time currency exchange rates via Fixer.io API.

    This integration provides access to exchange rate data for 170+ world currencies,
    including conversion, rate lookup, and currency information. Compatible with
    free tier Fixer.io accounts.

    Author:
      Kognitos
    """

    def __init__(self):
        """
        Initializes an instance of the class.

        :param self: The instance of the class.
        """
        self._base_url = FIXED_CURRENCY_DATA_BASE_URL
        self._timeout = float(DEFAULT_TIMEOUT)

    @property
    def timeout(self) -> float:
        """
        Get the value of the timeout.

        Parameters:
            None

        Returns:
            The value of the timeout.
        """
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: float):
        """
        Sets the timeout value in seconds.

        Args:
            timeout (float): The timeout value to set. Must be a positive number.

        Raises:
            ValueError: If the timeout value is less than or equal to 0.
        """
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self._timeout = timeout

    @procedure("to say hello", connection_required=False)
    def say_hello(self) -> str:
        """
        Test if the book is loaded and responding.

        Output Concepts:
            the greeting: A hello message

        Example:
            >>> say hello
        """
        return "Hello from Fixer currency exchange book! Use other procedures with your Fixer.io API key."

    @procedure("to get rates with (api key)")
    def get_rates(self, api_key: str) -> str:
        """
        Get current exchange rates for all supported currencies.

        Input Concepts:
            the api key: Your Fixer.io API key

        Output Concepts:
            the rates: Current exchange rates

        Example:
            >>> get rates with "your_api_key"
        """
        try:
            url = f"{self._base_url}/latest?access_key={api_key}"
            response = requests.get(url, timeout=self._timeout)
            data = response.json()

            if not data.get("success", False):
                error = data.get("error", {})
                return f"Error: {error.get('info', 'API request failed')}"

            base = data.get("base", "EUR")
            date = data.get("date", "unknown")
            rates = data.get("rates", {})

            # Show first 10 rates
            rate_list = []
            for currency, rate in sorted(rates.items())[:10]:
                rate_list.append(f"{currency}: {rate}")

            return (
                f"Exchange rates for {base} on {date}: "
                + ", ".join(rate_list)
                + f" (and {len(rates)-10} more currencies available)"
            )

        except Exception as e:
            return f"Error: {str(e)}"

    @procedure("to get specific rates")
    def get_specific_rates(self, currencies: str, api_key: str) -> str:
        """
        Get rates for specific currencies only.

        Input Concepts:
            the currencies: Comma-separated currency codes (e.g. "USD,GBP,JPY")
            the api key: Your Fixer.io API key

        Output Concepts:
            the specific rates: Exchange rates for specified currencies

        Example:
            >>> get specific rates with
            ...     the currencies is "USD,GBP,JPY"
            ...     the api key is "your_api_key"
        """
        try:
            url = f"{self._base_url}/latest?access_key={api_key}&symbols={currencies.upper()}"
            response = requests.get(url, timeout=self._timeout)
            data = response.json()

            if not data.get("success", False):
                error = data.get("error", {})
                return f"Error: {error.get('info', 'API request failed')}"

            base = data.get("base", "EUR")
            date = data.get("date", "unknown")
            rates = data.get("rates", {})

            rate_list = []
            for currency, rate in rates.items():
                rate_list.append(f"{currency}: {rate}")

            return f"Exchange rates for {base} on {date}: " + ", ".join(rate_list)

        except Exception as e:
            return f"Error: {str(e)}"

    @procedure("to convert currency")
    def convert_currency(
        self, amount: str, source_currency: str, target_currency: str, api_key: str
    ) -> str:
        """
        Convert currency amount using latest rates (free tier compatible).

        Input Concepts:
            the amount: Amount to convert
            the source currency: Source currency (3-letter code)
            the target currency: Target currency (3-letter code)
            the api key: Your Fixer.io API key

        Output Concepts:
            the conversion: Conversion result

        Example:
            >>> convert currency with
            ...     the amount is "100"
            ...     the source currency is "USD"
            ...     the target currency is "EUR"
            ...     the api key is "your_api_key"
        """
        try:
            # Get latest rates for both currencies
            symbols = f"{source_currency.upper()},{target_currency.upper()}"
            url = f"{self._base_url}/latest?access_key={api_key}&symbols={symbols}"
            response = requests.get(url, timeout=self._timeout)
            data = response.json()

            if not data.get("success", False):
                error = data.get("error", {})
                return f"Error: {error.get('info', 'API request failed')}"

            rates = data.get("rates", {})
            date = data.get("date", "unknown")

            source_rate = rates.get(source_currency.upper())
            target_rate = rates.get(target_currency.upper())

            if not source_rate or not target_rate:
                return f"Error: Could not find rates for {source_currency} or {target_currency}"

            # Calculate conversion: amount * (target_rate / source_rate)
            amount_float = float(amount)
            conversion_rate = target_rate / source_rate
            result = amount_float * conversion_rate

            return f"Converted {amount} {source_currency.upper()} to {result:.4f} {target_currency.upper()} (rate: {conversion_rate:.6f}) on {date}"

        except ValueError:
            return f"Error: Invalid amount '{amount}'. Please provide a numeric value."
        except Exception as e:
            return f"Error: {str(e)}"

    @procedure("to check supported currencies")
    def check_supported_currencies(self, api_key: str) -> str:
        """
        Get list of supported currencies.

        Input Concepts:
            the api key: Your Fixer.io API key

        Output Concepts:
            the supported currencies: List of supported currency codes

        Example:
            >>> check supported currencies with "your_api_key"
        """
        try:
            url = f"{self._base_url}/symbols?access_key={api_key}"
            response = requests.get(url, timeout=self._timeout)
            data = response.json()

            if not data.get("success", False):
                error = data.get("error", {})
                return f"Error: {error.get('info', 'API request failed')}"

            symbols = data.get("symbols", {})

            # Show first 20 currencies
            currency_list = []
            for code, name in sorted(symbols.items())[:20]:
                currency_list.append(f"{code}: {name}")

            return (
                f"Supported currencies (first 20 of {len(symbols)} total): "
                + ", ".join(currency_list)
            )

        except Exception as e:
            return f"Error: {str(e)}"

