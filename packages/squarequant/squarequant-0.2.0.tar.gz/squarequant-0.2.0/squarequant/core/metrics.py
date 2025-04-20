"""
Risk metric implementations for the SquareQuant package
"""

import pandas as pd
import numpy as np
from numpy.linalg import LinAlgError
from scipy import stats
from scipy.optimize import minimize_scalar
from typing import List, Optional, Union

from squarequant.constants import (
    TRADING_DAYS_PER_YEAR,
    DEFAULT_SHARPE_WINDOW,
    DEFAULT_SORTINO_WINDOW,
    DEFAULT_VOLATILITY_WINDOW,
    DEFAULT_DRAWDOWN_WINDOW,
    DEFAULT_VAR_WINDOW,
    DEFAULT_CALMAR_WINDOW,
    DEFAULT_CVAR_WINDOW,
    DEFAULT_CONFIDENCE,
    DEFAULT_SEMIDEVIATION_WINDOW,
    DEFAULT_AVGDRAWDOWN_WINDOW,
    DEFAULT_ULCER_WINDOW,
    DEFAULT_MAD_WINDOW,
    DEFAULT_CDAR_WINDOW,
    DEFAULT_EDAR_WINDOW,
    DEFAULT_EVAR_WINDOW,
    DEFAULT_ERM_WINDOW,
    VALID_VAR_METHODS
)

from squarequant.core.base import RiskMetricBase, RiskFreeRateHelper


class SharpeRatio(RiskMetricBase):
    """
    Calculate rolling Sharpe ratios for specified assets
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 freerate: Optional[str] = None,
                 freerate_value: Optional[float] = None,
                 window: int = DEFAULT_SHARPE_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize Sharpe ratio calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate for
        freerate (str, optional): Column name for risk-free rate in data DataFrame
        freerate_value (float, optional): Constant risk-free rate to use if no column provided
        window (int): Rolling window size in trading days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True,
            freerate=freerate,
            freerate_value=freerate_value
        )

        # Get daily risk-free rate (without rolling average)
        self.daily_risk_free_rate = RiskFreeRateHelper.get_risk_free_rate(
            returns=self.data,
            freerate=freerate,
            freerate_value=freerate_value
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Sharpe ratio for all valid assets, with completely rewritten implementation
        to avoid any potential issues with the original code.

        Returns:
        DataFrame: Sharpe ratios for specified assets
        """
        if not self.valid_assets:
            return self.result

        # Create empty results DataFrame
        result_df = pd.DataFrame(index=self.data.index, columns=self.valid_assets)

        for asset in self.valid_assets:
            # Step 1: Calculate excess returns explicitly
            excess_returns = self.data[asset] - self.daily_risk_free_rate

            # Step 2: Calculate rolling mean of excess returns
            rolling_mean = excess_returns.rolling(window=self.window, min_periods=self.min_periods).mean()

            # Step 3: Calculate rolling standard deviation of excess returns
            rolling_std = excess_returns.rolling(window=self.window, min_periods=self.min_periods).std(ddof=1)

            # Step 4: Calculate annualized Sharpe ratio
            # Handle division by zero or very small numbers
            rolling_std_safe = rolling_std.replace(0, np.nan)

            sharpe = rolling_mean / rolling_std_safe * np.sqrt(TRADING_DAYS_PER_YEAR)
            # Store results
            result_df[asset] = sharpe

        # Copy results to the class result DataFrame
        self.result[self.valid_assets] = result_df[self.valid_assets]

        return self._finalize_result(self.result[self.valid_assets])

class SortinoRatio(RiskMetricBase):
    """
    Calculate rolling Sortino ratios for specified assets
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 freerate: Optional[str] = None,
                 freerate_value: Optional[float] = None,
                 window: int = DEFAULT_SORTINO_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize Sortino ratio calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate for
        freerate (str, optional): Column name for risk-free rate in data DataFrame
        freerate_value (float, optional): Constant risk-free rate to use if no column provided
        window (int): Rolling window size in trading days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True,
            freerate=freerate,
            freerate_value=freerate_value
        )

        # Get daily risk-free rate (without rolling average)
        self.daily_risk_free_rate = RiskFreeRateHelper.get_risk_free_rate(
            returns=self.data,
            freerate=freerate,
            freerate_value=freerate_value
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Sortino ratio for all valid assets using vectorized operations.

        Returns:
        DataFrame: Sortino ratios for specified assets
        """
        if not self.valid_assets:
            return self.result

        # Use result DataFrame for intermediate calculations
        # Calculate daily excess returns directly into result
        self.result[self.valid_assets] = self.data[self.valid_assets].sub(self.daily_risk_free_rate, axis=0)

        # Store rolling mean
        rolling_mean = self.result[self.valid_assets].rolling(window=self.window, min_periods=self.min_periods).mean()

        # Create a custom function to calculate downside deviation for a pandas Series
        def downside_deviation(series):
            # Only consider negative returns for downside risk
            downside_returns = np.minimum(series, 0)
            # Compute root mean square of negative returns
            return np.sqrt(np.mean(np.square(downside_returns))) if len(series) > 0 else np.nan

        # Calculate downside deviation directly into result
        for asset in self.valid_assets:
            self.result[asset] = self.result[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(downside_deviation, raw=True)

        # Calculate Sortino ratio
        self.result[self.valid_assets] = rolling_mean.div(
            self.result[self.valid_assets].replace(0, np.nan)
        ) * np.sqrt(TRADING_DAYS_PER_YEAR)

        return self._finalize_result(self.result[self.valid_assets])


class Volatility(RiskMetricBase):
    """
    Calculate annualized rolling volatility for specified assets
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 window: int = DEFAULT_VOLATILITY_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize volatility calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate for
        window (int): Rolling window size in trading days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate annualized volatility for all valid assets.

        Returns:
        DataFrame: Volatility for specified assets
        """
        if not self.valid_assets:
            return self.result

        # Calculate rolling standard deviation and annualize for all valid assets at once
        vol_result = self.data[self.valid_assets].rolling(
            window=self.window,
            min_periods=self.min_periods
        ).std() * np.sqrt(TRADING_DAYS_PER_YEAR)

        return self._finalize_result(vol_result)


class MaximumDrawdown(RiskMetricBase):
    """
    Calculate the maximum drawdown for selected assets over a given time period
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 window: int = DEFAULT_DRAWDOWN_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize maximum drawdown calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate drawdown for
        window (int): Rolling window size in days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=False,
            min_periods=1
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate maximum drawdown for all valid assets.

        Returns:
        DataFrame: Maximum drawdown for specified assets
        """
        if not self.valid_assets:
            return self.result

        # No need for a separate asset_data DataFrame
        # Calculate rolling maximums directly using the original data
        rolling_max = self.data[self.valid_assets].rolling(
            window=self.window,
            min_periods=self.min_periods
        ).max()

        # Calculate drawdown directly into result
        self.result[self.valid_assets] = self.data[self.valid_assets].div(rolling_max) - 1

        # Calculate rolling minimum of drawdown into result
        self.result[self.valid_assets] = self.result[self.valid_assets].rolling(
            window=self.window,
            min_periods=self.min_periods
        ).min()

        return self._finalize_result(self.result[self.valid_assets])


class CalmarRatio(RiskMetricBase):
    """
    Calculate rolling Calmar ratios for specified assets
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 window: int = DEFAULT_CALMAR_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize Calmar ratio calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate for
        window (int): Rolling window size in trading days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Calmar ratio for all valid assets.

        Returns:
        DataFrame: Calmar ratios for specified assets
        """
        if not self.valid_assets:
            return self.result

        # Calculate annualized returns for the window
        rolling_returns = self.data[self.valid_assets].rolling(
            window=self.window,
            min_periods=self.min_periods
        ).mean() * TRADING_DAYS_PER_YEAR

        # For maximum drawdown calculation, convert returns to cumulative returns
        cum_returns = (1 + self.data[self.valid_assets]).cumprod()

        # Calculate rolling maximum values directly
        rolling_max = cum_returns.rolling(
            window=self.window,
            min_periods=self.min_periods
        ).max()

        # Calculate drawdown directly into result
        self.result[self.valid_assets] = cum_returns.div(rolling_max) - 1

        # Calculate max drawdown directly into result
        self.result[self.valid_assets] = self.result[self.valid_assets].rolling(
            window=self.window,
            min_periods=self.min_periods
        ).min()

        # Calculate Calmar ratio directly into result
        self.result[self.valid_assets] = rolling_returns.div(
            self.result[self.valid_assets].abs().replace(0, np.nan)
        )

        return self._finalize_result(self.result[self.valid_assets])


class ConditionalValueAtRisk(RiskMetricBase):
    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 confidence: float = DEFAULT_CONFIDENCE,
                 window: int = DEFAULT_CVAR_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None,
                 method: str = 'historical',
                 holding_period: int = 1,  # Add holding_period parameter
                 scaling_method: str = 'sqrt_time'):  # Add scaling_method parameter

        # Initialize with same parameters as ValueAtRisk
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True,
            confidence=confidence,
            method=method
        )

        self.confidence = confidence
        self.method = method
        self.holding_period = holding_period
        self.scaling_method = scaling_method

    def calculate(self) -> pd.DataFrame:
        if not self.valid_assets:
            return self.result

        # Calculate for each asset
        for asset in self.valid_assets:
            # Define calculation function based on method
            calc_func = self._calculate_historical_cvar if self.method == 'historical' else self._calculate_parametric_cvar

            # Apply to rolling windows
            self.result[asset] = self._optimized_rolling_apply(
                self.data[asset],
                self.window,
                calc_func
            )

        return self.result.dropna(how='all')

    def _calculate_historical_cvar(self, returns):
        # Filter NaN values
        valid_returns = returns[~np.isnan(returns)]
        if len(valid_returns) < self.min_periods:
            return np.nan

        # Sort returns (ascending)
        sorted_returns = np.sort(valid_returns)

        # Find tail size based on confidence
        tail_size = max(1, int(np.ceil(len(sorted_returns) * (1 - self.confidence))))

        # Calculate CVaR as mean of tail
        cvar = -np.mean(sorted_returns[:tail_size])

        # Apply holding period scaling
        if self.scaling_method == 'sqrt_time' and self.holding_period > 1:
            cvar *= np.sqrt(self.holding_period)

        return cvar

    def _calculate_parametric_cvar(self, returns):
        # Same implementation as before
        valid_returns = returns[~np.isnan(returns)]
        if len(valid_returns) < self.min_periods:
            return np.nan

        mean = np.mean(valid_returns)
        std = np.std(valid_returns, ddof=1)

        z_score = stats.norm.ppf(self.confidence)
        pdf_value = stats.norm.pdf(z_score)
        es_coeff = pdf_value / (1 - self.confidence)

        cvar = -(mean - std * es_coeff)

        # Apply holding period scaling
        if self.holding_period > 1:
            cvar *= np.sqrt(self.holding_period)

        return cvar

    def _optimized_rolling_apply(self, series, window, func):
        # Same as in ValueAtRisk
        result = pd.Series(index=series.index, dtype=float)
        values = series.values

        for i in range(window - 1, len(values)):
            window_data = values[i - window + 1:i + 1]
            result.iloc[i] = func(window_data)

        return result

class SemiDeviation(RiskMetricBase):
    """
    Calculate semi-deviation (downside volatility) for specified assets.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 target_return: Optional[float] = None,
                 window: int = DEFAULT_SEMIDEVIATION_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize semi-deviation calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate for
        target_return (float, optional): Target return threshold. If None, the mean return is used
        window (int): Rolling window size in trading days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True,
            target_return=target_return
        )

        self.target_return = target_return

    def calculate(self) -> pd.DataFrame:
        """
        Calculate semi-deviation for all valid assets.

        Returns:
        DataFrame: Semi-deviation for specified assets
        """
        if not self.valid_assets:
            return self.result

        asset_returns = self.data[self.valid_assets]

        # Define a function to calculate semi-deviation for each window
        def semi_deviation(returns):
            if self.target_return is None:
                # If no target return is provided, use the mean return of the window
                threshold = np.mean(returns)
            else:
                threshold = self.target_return

            # Consider only returns below the threshold
            downside_returns = np.minimum(returns - threshold, 0)

            # Compute semi-deviation (square root of the mean of squared deviations)
            return np.sqrt(np.mean(np.square(downside_returns))) if len(returns) > 0 else np.nan

        # Apply the function to each asset
        for asset in self.valid_assets:
            self.result[asset] = asset_returns[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(semi_deviation, raw=True)

        # Annualize the semi-deviation
        self.result[self.valid_assets] = self.result[self.valid_assets] * np.sqrt(TRADING_DAYS_PER_YEAR)

        return self._finalize_result(self.result[self.valid_assets])


class AverageDrawdown(RiskMetricBase):
    """
    Calculate average drawdown for specified assets.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 window: int = DEFAULT_AVGDRAWDOWN_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize average drawdown calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate drawdown for
        window (int): Rolling window size in days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=False,
            min_periods=1
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate average drawdown for all valid assets.

        Returns:
        DataFrame: Average drawdown for specified assets
        """
        if not self.valid_assets:
            return self.result

        # Calculate rolling maximum directly
        rolling_max = self.data[self.valid_assets].rolling(
            window=self.window,
            min_periods=self.min_periods
        ).max()

        # Calculate drawdowns (not stored in self.result to avoid overwriting)
        drawdowns = self.data[self.valid_assets].div(rolling_max) - 1

        # Calculate mean of all drawdowns directly into result
        # We only include non-zero drawdowns in the calculation
        def avg_drawdown(drawdown_series):
            # Only consider actual drawdowns (negative values)
            actual_drawdowns = drawdown_series[drawdown_series < 0]

            # Calculate the mean of the drawdowns if there are any
            return actual_drawdowns.mean() if len(actual_drawdowns) > 0 else 0

        for asset in self.valid_assets:
            self.result[asset] = drawdowns[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(avg_drawdown)

        return self._finalize_result(self.result[self.valid_assets])


class UlcerIndex(RiskMetricBase):
    """
    Calculate Ulcer Index for specified assets.
    The Ulcer Index is the square root of the mean of the squared drawdowns.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 window: int = DEFAULT_ULCER_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize Ulcer Index calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate for
        window (int): Rolling window size in days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=False,
            min_periods=1
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Ulcer Index for all valid assets.

        Returns:
        DataFrame: Ulcer Index for specified assets
        """
        if not self.valid_assets:
            return self.result

        # Calculate rolling maximum directly
        rolling_max = self.data[self.valid_assets].rolling(
            window=self.window,
            min_periods=self.min_periods
        ).max()

        # Calculate percentage drawdowns (not stored in self.result to avoid overwriting)
        drawdowns = self.data[self.valid_assets].div(rolling_max) - 1

        # Calculate Ulcer Index directly into result
        def ulcer_index(drawdown_series):
            # Square all drawdowns (negative values become positive after squaring)
            squared_drawdowns = np.square(np.minimum(drawdown_series, 0))

            # Calculate the mean of squared drawdowns and take the square root
            return np.sqrt(np.mean(squared_drawdowns)) if len(drawdown_series) > 0 else 0

        for asset in self.valid_assets:
            self.result[asset] = drawdowns[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(ulcer_index)

        return self._finalize_result(self.result[self.valid_assets])


class MeanAbsoluteDeviation(RiskMetricBase):
    """
    Calculate Mean Absolute Deviation (MAD) for specified assets.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 window: int = DEFAULT_MAD_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize Mean Absolute Deviation calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate for
        window (int): Rolling window size in trading days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True
        )

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Mean Absolute Deviation for all valid assets.

        Returns:
        DataFrame: Mean Absolute Deviation for specified assets
        """
        if not self.valid_assets:
            return self.result

        # Define a function to calculate MAD for each window
        def mad(returns):
            # Calculate the mean return
            mean_return = np.mean(returns)

            # Calculate absolute deviations from the mean
            abs_deviations = np.abs(returns - mean_return)

            # Return the mean of absolute deviations
            return np.mean(abs_deviations) if len(returns) > 0 else np.nan

        # Apply the function to each asset
        for asset in self.valid_assets:
            self.result[asset] = self.data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(mad, raw=True)

        # Annualize the MAD
        self.result[self.valid_assets] = self.result[self.valid_assets] * np.sqrt(TRADING_DAYS_PER_YEAR)

        return self._finalize_result(self.result[self.valid_assets])


class EntropicRiskMeasure(RiskMetricBase):
    """
    Class for calculating the Entropic Risk Measure (ERM) using the historical method.

    The Entropic Risk Measure is calculated as:
    ERM(X) = z * ln(M_X(1/z) * (1/(1-confidence)))

    Where:
    - M_X(t) is the moment generating function of X at point t
    - z is the risk aversion parameter (must be positive)
    - confidence is the confidence level (typically 0.95 or 0.99)

    This implementation uses the historical method, which directly calculates
    the moment generating function from observed returns.
    """

    VALID_METHODS = ['historical']
    VALID_SCALING_METHODS = ['sqrt_time', 'linear', 'none']

    def __init__(
            self,
            data: pd.DataFrame,
            assets: List[str],
            z: float = 1.0,
            confidence: float = DEFAULT_CONFIDENCE,
            window: int = DEFAULT_ERM_WINDOW,
            start: Optional[str] = None,
            end: Optional[str] = None,
            holding_period: int = 1,
            scaling_method: str = 'sqrt_time'
    ):
        """
        Initialize the Entropic Risk Measure calculator.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing return series for assets
        assets : List[str]
            List of asset column names to calculate ERM for
        z : float, optional
            Risk aversion parameter, must be greater than zero. Default is 1.0
        confidence : float, optional
            Confidence level (typically 0.95 or 0.99). Default is from constants.DEFAULT_CONFIDENCE
        window : int, optional
            Size of rolling window for calculation. Default is from constants.DEFAULT_ERM_WINDOW
        start : str, optional
            Start date for calculations (YYYY-MM-DD format)
        end : str, optional
            End date for calculations (YYYY-MM-DD format)
        holding_period : int, optional
            Time horizon for risk projection. Default is 1
        scaling_method : str, optional
            Method to scale for holding period: 'sqrt_time', 'linear', or 'none'. Default is 'sqrt_time'
        """
        # Initialize with parent class parameters
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True,
            confidence=confidence,
            method='historical'  # Only historical method is supported now
        )

        # Validate parameters
        if z <= 0:
            raise ValueError("Risk aversion parameter z must be positive")

        if confidence <= 0 or confidence >= 1:
            raise ValueError("Confidence level must be between 0 and 1")

        if scaling_method not in self.VALID_SCALING_METHODS:
            raise ValueError(f"Scaling method must be one of {self.VALID_SCALING_METHODS}")

        if holding_period < 1:
            raise ValueError("Holding period must be at least 1")

        # Store additional parameters
        self.z = z
        self.confidence = confidence
        self.holding_period = holding_period
        self.scaling_method = scaling_method

    def calculate(self) -> pd.DataFrame:
        """
        Calculate the Entropic Risk Measure for all assets using the historical method.

        Returns
        -------
        pd.DataFrame
            DataFrame containing ERM values for each asset over time
        """
        if not self.valid_assets:
            return self.result

        # Calculate using historical method
        self._calculate_historical()

        return self._finalize_result(self.result[self.valid_assets])

    def _calculate_historical(self):
        """Calculate ERM using historical method for all assets"""
        for asset in self.valid_assets:
            # Define a lambda function for the rolling calculation
            calc_func = lambda x: self._historical_erm_for_window(x)

            # Apply the function to each window
            self.result[asset] = self.data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(calc_func, raw=True)

            # Apply holding period scaling
            if self.holding_period > 1 and self.scaling_method != 'none':
                self.result[asset] = self._apply_scaling(self.result[asset])

    def _historical_erm_for_window(self, returns):
        """Calculate historical ERM for a single window"""
        # Calculate moment generating function at 1/z
        mgf_value = np.mean(np.exp(-self.z * returns))

        # Calculate the historical erm
        return self.z * (np.log(mgf_value) + np.log(1 / (1 - self.confidence)))

    def _apply_scaling(self, values):
        """Apply scaling based on holding period"""
        if self.scaling_method == 'sqrt_time':
            return values * np.sqrt(self.holding_period)
        elif self.scaling_method == 'linear':
            return values * self.holding_period
        return values

    def get_erm_at_date(self, date):
        """Get ERM values for all assets at a specific date"""
        if date not in self.result.index:
            raise ValueError(f"Date {date} not found in results")

        return self.result.loc[date]

    def get_erm_for_asset(self, asset):
        """Get ERM time series for a specific asset"""
        if asset not in self.valid_assets:
            raise ValueError(f"Asset {asset} not found in results")

        return self.result[asset]

    @classmethod
    def batch_compute(cls, data, asset_groups, **kwargs):
        """Compute ERM for multiple groups of assets"""
        results = []

        for assets in asset_groups:
            erm = cls(data=data, assets=assets, **kwargs)
            results.append(erm.calculate())

        return results


class EntropicValueAtRisk(EntropicRiskMeasure):
    """
    Class for calculating the Entropic Value-at-Risk (EVaR).

    The Entropic Value-at-Risk is calculated as:
    EVaR(X) = inf_{z>0} { z * ln(M_X(1/z) * (1/(1-confidence))) }

    Where:
    - M_X(t) is the moment generating function of X at point t
    - confidence is the confidence level (typically 0.95 or 0.99)
    - The infimum is taken over all positive values of z

    Note that confidence = 1 - alpha, where alpha is the significance level
    typically used in mathematical formulations.
    """

    def __init__(
            self,
            data: pd.DataFrame,
            assets: List[str],
            confidence: float = 0.99,
            window: int = 252,
            start: Optional[str] = None,
            end: Optional[str] = None,
            holding_period: int = 1,
            scaling_method: str = 'sqrt_time',
            z_bounds: tuple = (0.1, 10.0),  # Bounds for optimization
            z_default: float = 1.0  # Default z value in case optimization fails
    ):
        """
        Initialize the Entropic Value-at-Risk calculator.

        Parameters
        ----------
        data : pd.DataFrame
            DataFrame containing return series for assets
        assets : List[str]
            List of asset column names to calculate EVaR for
        confidence : float, optional
            Confidence level (typically 0.95 or 0.99). Default is 0.99
        window : int, optional
            Size of rolling window for calculation. Default is 252
        start : str, optional
            Start date for calculations (YYYY-MM-DD format)
        end : str, optional
            End date for calculations (YYYY-MM-DD format)
        holding_period : int, optional
            Time horizon for risk projection. Default is 1
        scaling_method : str, optional
            Method to scale for holding period: 'sqrt_time', 'linear', or 'none'. Default is 'sqrt_time'
        z_bounds : tuple, optional
            Bounds for z parameter optimization (lower, upper). Default is (0.1, 10.0)
        z_default : float, optional
            Default z value to use if optimization fails. Default is 1.0
        """
        # Initialize with parent class (ERM) parameters
        # Use a default z value initially, will be optimized during calculation
        super().__init__(
            data=data,
            assets=assets,
            z=z_default,  # Temporary value, will be optimized per window
            confidence=confidence,
            window=window,
            start=start,
            end=end,
            holding_period=holding_period,
            scaling_method=scaling_method,
        )

        # Store additional parameters for EVaR
        self.z_bounds = z_bounds
        self.z_default = z_default

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Entropic Value-at-Risk for all valid assets.

        Returns
        -------
        pd.DataFrame
            DataFrame containing EVaR values for each asset over time
        """
        if not self.valid_assets:
            return self.result

        # Calculate using historical method with optimization
        self._calculate_historical()

        return self._finalize_result(self.result[self.valid_assets])

    def _calculate_historical(self):
        """Calculate EVaR using historical method for all assets"""
        for asset in self.valid_assets:
            # Define a lambda function for the rolling calculation
            calc_func = lambda x: self._optimize_z_historical(x)

            # Apply the function to each window
            self.result[asset] = self.data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(calc_func, raw=True)

            # Apply holding period scaling
            if self.holding_period > 1 and self.scaling_method != 'none':
                self.result[asset] = self._apply_scaling(self.result[asset])

    def _optimize_z_historical(self, returns):
        """
        Find optimal z value that minimizes ERM for a single window using historical method.
        This implements the infimum operation in the EVaR formula.
        """

        # Define objective function to minimize (the ERM formula)
        def objective(z):
            if z <= 0:
                return np.inf  # Invalid z

            # Calculate moment generating function at 1/z
            mgf_value = np.mean(np.exp(-1 / z * returns))

            # Calculate ERM with this z value
            return z * (np.log(mgf_value) + np.log(1 / (1 - self.confidence)))

        try:
            # Find z that minimizes the objective function
            result = minimize_scalar(
                objective,
                bounds=self.z_bounds,
                method='bounded'
            )

            if result.success:
                optimal_z = result.x
                return objective(optimal_z)
            else:
                # Fallback to default z if optimization fails
                return objective(self.z_default)
        except:
            # Handle any exceptions during optimization
            return objective(self.z_default)

    def get_evar_at_date(self, date):
        """Get EVaR values for all assets at a specific date"""
        return super().get_erm_at_date(date)

    def get_evar_for_asset(self, asset):
        """Get EVaR time series for a specific asset"""
        return super().get_erm_for_asset(asset)


class ConditionalDrawdownAtRisk(RiskMetricBase):
    """
    Calculate the Conditional Drawdown at Risk (CDaR) for specified assets.

    CDaR is an extension of drawdown analysis that measures the expected value
    of drawdowns exceeding a certain threshold, providing insights into tail risk
    of drawdown distributions.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 confidence: float = DEFAULT_CONFIDENCE,
                 window: int = DEFAULT_CDAR_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None):
        """
        Initialize Conditional Drawdown at Risk calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate CDaR for
        confidence (float): Confidence level (0-1)
        window (int): Rolling window size in days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        """
        # Validate confidence level
        if confidence <= 0 or confidence >= 1:
            raise ValueError("Confidence level must be between 0 and 1")

        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=False,  # Use price data directly
            min_periods=2,  # Need at least 2 periods to calculate a drawdown
            confidence=confidence
        )

        self.confidence = confidence

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Conditional Drawdown at Risk for all valid assets.

        Returns:
        DataFrame: Conditional Drawdown at Risk for specified assets
        """
        if not self.valid_assets:
            return self.result

        # We'll directly work with prices in this case
        asset_data = self.data[self.valid_assets]

        for asset in self.valid_assets:
            # Function to calculate CDaR for each rolling window
            def calculate_cdar(window_prices):
                if len(window_prices) < 2:
                    return np.nan

                # Calculate drawdowns
                prices = np.array(window_prices)
                peak = np.maximum.accumulate(prices)
                # Use relative drawdowns (percentage)
                drawdowns = (peak - prices) / peak

                # If all values are the same, drawdowns will be zero
                if np.all(drawdowns == 0):
                    return 0.0

                # Sort drawdowns to find the VaR threshold
                sorted_dd = np.sort(drawdowns)
                index = max(0, int(np.ceil(self.confidence * len(sorted_dd)) - 1))

                dar_value = sorted_dd[index]

                # Find drawdowns exceeding the DaR threshold
                excess_drawdowns = sorted_dd[:index + 1]

                # Calculate CDaR
                if len(excess_drawdowns) > 0:
                    cdar = np.mean(excess_drawdowns)
                else:
                    cdar = dar_value

                return cdar

            # Apply the function to rolling windows
            self.result[asset] = asset_data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(calculate_cdar, raw=True)

        # Finalize and return the result
        return self._finalize_result(self.result[self.valid_assets])


class EntropicDrawdownAtRisk(RiskMetricBase):
    """
    Calculate the Entropic Drawdown at Risk (EDaR) for specified assets.

    EDaR uses the entropy concept to provide a coherent risk measure
    for drawdowns that captures tail risk better than traditional metrics.
    """

    def __init__(self,
                 data: pd.DataFrame,
                 assets: List[str],
                 confidence: float = DEFAULT_CONFIDENCE,
                 window: int = DEFAULT_EDAR_WINDOW,
                 start: Optional[str] = None,
                 end: Optional[str] = None,
                 solver: Optional[str] = None,
                 batch_size: int = 1,
                 fallback_z_min: float = 0.01,
                 fallback_z_max: float = 100.0,
                 fallback_steps: int = 20):
        """
        Initialize Entropic Drawdown at Risk calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate EDaR for
        confidence (float): Confidence level (0-1)
        window (int): Rolling window size in days
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        solver (str, optional): CVXPY solver name if available
        batch_size (int): Number of assets to process in one batch
        fallback_z_min (float): Minimum z value for grid search
        fallback_z_max (float): Maximum z value for grid search
        fallback_steps (int): Number of steps for grid search
        """
        # Validate confidence level
        if confidence <= 0 or confidence >= 1:
            raise ValueError("Confidence level must be between 0 and 1")

        # Import warnings here for error handling
        import warnings
        self.warnings = warnings

        # Check for CVXPY availability
        self.has_cvxpy = False
        self.cp = None
        try:
            import cvxpy as cp
            self.cp = cp
            self.has_cvxpy = True
        except ImportError:
            warnings.warn(
                "CVXPY not installed. Using grid search for EDaR calculation."
            )

        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=False,  # Use price data directly
            min_periods=2,  # Need at least 2 periods to calculate a drawdown
            confidence=confidence
        )

        self.confidence = confidence
        self.solver = solver
        self.batch_size = max(1, batch_size)
        self.fallback_z_min = fallback_z_min
        self.fallback_z_max = fallback_z_max
        self.fallback_steps = fallback_steps

        # Pre-compute logarithm for grid search
        self.log_inv_alpha = np.log(1 / confidence)

    def _calculate_edar_grid_search(self, drawdowns):
        """
        Calculate EDaR using grid search method.

        Parameters:
        drawdowns (ndarray): Array of drawdown values

        Returns:
        float: EDaR value
        """
        if len(drawdowns) < 2 or np.all(drawdowns == 0):
            return 0.0

        # Remove any NaN values
        drawdowns = drawdowns[~np.isnan(drawdowns)]
        if len(drawdowns) == 0:
            return np.nan

        # Generate z-values for grid search
        z_values = np.linspace(self.fallback_z_min, self.fallback_z_max, self.fallback_steps)

        min_edar = float('inf')
        for z in z_values:
            if z <= 0:
                continue

            try:
                # Calculate moment generating function
                # Use more numerically stable computation
                max_val = np.max(drawdowns / z)
                if max_val > 50:  # Avoid overflow
                    # Use log-sum-exp trick for numerical stability
                    shifted = drawdowns / z - max_val
                    mgf = np.exp(max_val) * np.mean(np.exp(shifted))
                else:
                    mgf = np.mean(np.exp(drawdowns / z))

                # Calculate EDaR
                edar = z * (np.log(mgf) + self.log_inv_alpha)

                # Update minimum
                if edar < min_edar:
                    min_edar = edar
            except:
                # Skip errors (e.g., overflow)
                continue

        # If we couldn't find a valid value, return NaN
        if min_edar == float('inf'):
            return np.nan

        return min_edar

    def _calculate_edar_cvxpy(self, drawdowns):
        """
        Calculate EDaR using CVXPY optimization.

        Parameters:
        drawdowns (ndarray): Array of drawdown values

        Returns:
        float: EDaR value
        """
        if not self.has_cvxpy:
            return self._calculate_edar_grid_search(drawdowns)

        if len(drawdowns) < 2 or np.all(drawdowns == 0):
            return 0.0

        # Remove any NaN values
        drawdowns = drawdowns[~np.isnan(drawdowns)]
        if len(drawdowns) == 0:
            return np.nan

        cp = self.cp
        T = len(drawdowns)

        try:
            # Set up the optimization problem
            t = cp.Variable()
            z = cp.Variable(pos=True)

            # We'll use the dual formulation which is more stable
            constraints = []
            objective_terms = []

            for dd in drawdowns:
                objective_terms.append(cp.exp(dd / z))

            objective = t + z * np.log(1 / self.confidence)
            constraints.append(cp.log(cp.sum(objective_terms) / T) <= t / z)

            # Solve the problem
            prob = cp.Problem(cp.Minimize(objective), constraints)

            try:
                if self.solver is not None:
                    prob.solve(solver=self.solver)
                else:
                    prob.solve()
            except:
                # If the primary solver fails, try SCS as a backup
                try:
                    prob.solve(solver='SCS')
                except:
                    # Fall back to grid search if optimization fails
                    return self._calculate_edar_grid_search(drawdowns)

            # Check if we got a valid solution
            if prob.status in ["optimal", "optimal_inaccurate"]:
                return objective.value
            else:
                return self._calculate_edar_grid_search(drawdowns)
        except:
            # Fall back to grid search if there's any error
            return self._calculate_edar_grid_search(drawdowns)

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Entropic Drawdown at Risk for all valid assets.

        Returns:
        DataFrame: Entropic Drawdown at Risk for specified assets
        """
        if not self.valid_assets:
            return self.result

        # We'll directly work with prices
        asset_data = self.data[self.valid_assets]

        # Process assets in batches
        for i in range(0, len(self.valid_assets), self.batch_size):
            batch_assets = self.valid_assets[i:i + self.batch_size]

            for asset in batch_assets:
                # Function to calculate EDaR for each rolling window
                def calculate_edar(window_prices):
                    if len(window_prices) < 2:
                        return np.nan

                    # Calculate drawdowns
                    prices = np.array(window_prices)
                    peak = np.maximum.accumulate(prices)
                    # Use relative drawdowns (percentage)
                    drawdowns = (peak - prices) / peak

                    # Calculate EDaR
                    if self.has_cvxpy:
                        return self._calculate_edar_cvxpy(drawdowns)
                    else:
                        return self._calculate_edar_grid_search(drawdowns)

                # Apply the function to rolling windows
                self.result[asset] = asset_data[asset].rolling(
                    window=self.window,
                    min_periods=self.min_periods
                ).apply(calculate_edar, raw=True)

                # Force garbage collection if processing multiple assets
                if len(self.valid_assets) > 1:
                    import gc
                    gc.collect()

        # Finalize and return the result
        return self._finalize_result(self.result[self.valid_assets])