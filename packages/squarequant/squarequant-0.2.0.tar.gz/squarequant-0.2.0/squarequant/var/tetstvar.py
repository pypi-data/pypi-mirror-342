"""
Value-at-Risk module implementations for the SquareQuant package
"""

import pandas as pd
import numpy as np
from scipy import stats
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

from squarequant.core.base import RiskMetricBase

class ValueAtRisk(RiskMetricBase):
    """
    Calculate Value at Risk (VaR) using different methods.

    Implements:
    - Historical VaR: Based on historical returns
    - Parametric VaR: Based on the Delta-Normal approach
    - Parametric VaR: Based on the Delta-Gamma-Normal approach
    """

    def __init__(
            self,
            data: pd.DataFrame,
            assets: List[str],
            confidence: float = 0.95,
            window: int = 252,
            start: Optional[str] = None,
            end: Optional[str] = None,
            method: str = 'historical',
            holding_period: int = 1,
            scaling_method: str = 'sqrt_time',
            weights: Optional[Union[List[float], dict]] = None
    ):
        """
        Initialize VaR calculator.

        Parameters:
        data (DataFrame): DataFrame with asset price data
        assets (List[str]): List of asset columns to calculate VaR for
        confidence (float): Confidence level (0-1), default is 0.95 (95%)
        window (int): Rolling window size in trading days, default is 252 (1 year)
        start (str, optional): Start date in format 'YYYY-MM-DD'
        end (str, optional): End date in format 'YYYY-MM-DD'
        method (str): Method to calculate VaR - 'historical', 'delta-normal', 'delta-gamma-normal'
        holding_period (int): Holding period in days, default is 1 day
        scaling_method (str): Method to scale 1-day VaR: 'sqrt_time', 'linear', or 'none'
        weights (Union[List[float], dict], optional): Portfolio weights for assets
        """
        # Initialize with parent class parameters
        super().__init__(
            data=data,
            assets=assets,
            window=window,
            start=start,
            end=end,
            use_returns=True,
            min_periods=max(10, window // 5)  # Allow reasonable minimum periods
        )

        self.confidence = confidence
        self.alpha = 1 - confidence  # Store alpha for calculations
        self.method = method
        self.holding_period = holding_period
        self.scaling_method = scaling_method
        self._original_weights = weights

        # Set weights (default: equal weighting)
        self._set_weights(weights)

    def _set_weights(self, weights):
        """Set portfolio weights based on valid_assets"""
        if weights is None:
            # Equal weighting
            self.weights = np.ones(len(self.valid_assets)) / len(self.valid_assets)
        elif isinstance(weights, dict):
            # Dictionary of weights - extract only for valid assets
            self.weights = np.array([weights.get(asset, 0) for asset in self.valid_assets])
            # Normalize weights to sum to 1
            if np.sum(self.weights) > 0:
                self.weights = self.weights / np.sum(self.weights)
            else:
                # If all weights are zero, use equal weighting
                self.weights = np.ones(len(self.valid_assets)) / len(self.valid_assets)
        else:
            # List of weights - assumes ordering matches assets
            # Since we can't directly map list weights to valid_assets,
            # use equal weighting for simplicity
            self.weights = np.ones(len(self.valid_assets)) / len(self.valid_assets)

    def _get_scaling_factor(self) -> float:
        """Determine scaling factor based on holding period and scaling method"""
        if self.holding_period == 1 or self.scaling_method == 'none':
            return 1.0
        elif self.scaling_method == 'sqrt_time':
            return np.sqrt(self.holding_period)
        elif self.scaling_method == 'linear':
            return self.holding_period
        else:
            raise ValueError(f"Unknown scaling method: {self.scaling_method}")

    def calculate(self) -> pd.DataFrame:
        """
        Calculate Value at Risk based on the configured method

        Returns:
        DataFrame: Value at Risk for specified assets
        """
        if not self.valid_assets:
            return self.result

        if self.method == 'historical':
            self._calculate_historical_var()
        elif self.method == 'delta-normal':
            self._calculate_delta_normal_var()
        elif self.method == 'delta-gamma-normal':
            self._calculate_delta_gamma_normal_var()
        else:
            raise ValueError(f"Unknown method: {self.method}")

        # Skip the base class _finalize_result method entirely
        # and just clean up our result DataFrame
        return self.result.dropna(how='all')

    def _calculate_portfolio_return_series(self) -> pd.Series:
        """Calculate portfolio returns based on asset returns and weights"""
        portfolio_returns = pd.Series(0, index=self.data.index)

        for i, asset in enumerate(self.valid_assets):
            portfolio_returns += self.data[asset] * self.weights[i]

        return portfolio_returns

    def _calculate_historical_var(self) -> None:
        """Calculate historical Value at Risk for individual assets and portfolio"""
        # Get scaling factor for holding period
        scaling_factor = self._get_scaling_factor()

        # Calculate individual asset VaRs
        for asset in self.valid_assets:
            self.result[asset] = self.data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).apply(lambda x: -np.percentile(x, self.alpha * 100) * scaling_factor)

        # Calculate portfolio VaR
        portfolio_returns = self._calculate_portfolio_return_series()
        self.result["Portfolio"] = portfolio_returns.rolling(
            window=self.window,
            min_periods=self.min_periods
        ).apply(lambda x: -np.percentile(x, self.alpha * 100) * scaling_factor)

    def _calculate_delta_normal_var(self) -> None:
        """Calculate Delta-Normal Value at Risk for individual assets and portfolio"""
        # Get scaling factor for holding period
        scaling_factor = self._get_scaling_factor()

        # Get Z-score for the given confidence level
        z_score = stats.norm.ppf(self.confidence)

        # Calculate individual asset VaRs
        for asset in self.valid_assets:
            volatility = self.data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).std()
            self.result[asset] = volatility * z_score * scaling_factor

        # Calculate portfolio VaR using portfolio return series
        portfolio_returns = self._calculate_portfolio_return_series()

        # Calculate portfolio volatility using the rolling window
        portfolio_volatility = portfolio_returns.rolling(
            window=self.window,
            min_periods=self.min_periods
        ).std()

        # Calculate VaR
        self.result['Portfolio'] = portfolio_volatility * z_score * scaling_factor

    def _calculate_delta_gamma_normal_var(self) -> None:
        """
        Calculate Delta-Gamma-Normal Value at Risk for individual assets and portfolio.
        This accounts for both first-order (delta) and second-order (gamma) price sensitivities.
        """
        # Get scaling factor for holding period
        scaling_factor = self._get_scaling_factor()

        # Get Z-score for the given confidence level
        z_score = stats.norm.ppf(self.confidence)

        # Calculate individual asset VaRs first (similar to delta-normal but with gamma adjustment)
        for asset in self.valid_assets:
            # Standard deviation (first-order effect)
            volatility = self.data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).std()

            # Calculate simple gamma term (second-order effect)
            # This is a simplified approximation - in practice would use option greeks
            gamma_adjustment = 0.5 * (volatility ** 2) * 0.1  # 10% convexity factor

            # Combine delta and gamma effects
            self.result[asset] = (volatility + gamma_adjustment) * z_score * scaling_factor

        # Calculate portfolio VaR using portfolio return series
        portfolio_returns = self._calculate_portfolio_return_series()

        # Calculate portfolio volatility using the rolling window
        portfolio_volatility = portfolio_returns.rolling(
            window=self.window,
            min_periods=self.min_periods
        ).std()

        # Calculate gamma adjustment for portfolio (simplified)
        portfolio_gamma_adjustment = 0.5 * (portfolio_volatility ** 2) * 0.1  # 10% convexity factor

        # Combine delta and gamma effects for portfolio
        self.result['Portfolio'] = (portfolio_volatility + portfolio_gamma_adjustment) * z_score * scaling_factor