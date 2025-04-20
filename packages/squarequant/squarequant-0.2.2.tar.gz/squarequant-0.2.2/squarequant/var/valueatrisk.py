"""
Value-at-Risk module implementations for the SquareQuant package
"""

import warnings
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.linear_model import LinearRegression
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
    - Parametric VaR: Based on the Delta-Gamma-Normal approach with proper gamma modeling
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
            weights: Optional[Union[List[float], dict]] = None,
            gamma_matrix: Optional[Union[pd.DataFrame, np.ndarray]] = None,
            market_regime_threshold: float = 1.5,
            vol_scaling_factor: float = 1.0
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
        gamma_matrix (Union[DataFrame, ndarray], optional): Matrix of second derivatives (gamma)
                                                          for assets in the portfolio
        market_regime_threshold (float): Volatility ratio threshold to detect high volatility regimes
        vol_scaling_factor (float): Factor to increase gamma effects in high volatility regimes
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

        # Validate confidence level
        if not (0 < confidence < 1):
            raise ValueError(f"Confidence level must be between 0 and 1, got {confidence}")

        # Define valid methods
        VALID_VAR_METHODS = ['historical', 'delta-normal', 'delta-gamma-normal', 'parametric']

        # Handle 'parametric' method for backward compatibility
        if method == 'parametric':
            method = 'delta-normal'

        # Validate method
        if method not in VALID_VAR_METHODS:
            valid_methods = ", ".join(VALID_VAR_METHODS)
            raise ValueError(f"Method must be one of {valid_methods}, got {method}")

        # Validate scaling method
        valid_scaling_methods = ['sqrt_time', 'linear', 'none']
        if scaling_method not in valid_scaling_methods:
            raise ValueError(f"Scaling method must be one of {valid_scaling_methods}, got {scaling_method}")

        self.confidence = confidence
        self.alpha = 1 - confidence  # Store alpha for calculations
        self.method = method
        self.holding_period = holding_period
        self.scaling_method = scaling_method
        self._original_weights = weights
        self.market_regime_threshold = market_regime_threshold
        self.vol_scaling_factor = vol_scaling_factor

        # Set weights (default: equal weighting)
        self._set_weights(weights)

        # Setup gamma matrix if provided, or initialize as zeros
        self._setup_gamma_matrix(gamma_matrix)

        # Store original price data for gamma calculations
        if hasattr(self, 'original_data'):
            self.price_data = self.original_data.copy()
        else:
            # If original_data is not available, we have to use whatever data is provided
            # This might be returns already, which would make gamma calculations less accurate
            self.price_data = data.copy()

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
        elif isinstance(weights, (list, np.ndarray)):
            # List/array of weights - check if lengths match
            if len(weights) == len(self.valid_assets):
                self.weights = np.array(weights)
                # Normalize weights to sum to 1
                if np.sum(self.weights) > 0:
                    self.weights = self.weights / np.sum(self.weights)
                else:
                    # If all weights are zero, use equal weighting
                    self.weights = np.ones(len(self.valid_assets)) / len(self.valid_assets)
            else:
                # If lengths don't match, warn user and use equal weighting
                warnings.warn(
                    f"Length of weights ({len(weights)}) doesn't match number of valid assets "
                    f"({len(self.valid_assets)}). Using equal weighting instead."
                )
                self.weights = np.ones(len(self.valid_assets)) / len(self.valid_assets)
        else:
            raise ValueError(f"Unsupported weights type: {type(weights)}")

    def _setup_gamma_matrix(self, gamma_matrix):
        """
        Set up the gamma matrix (second derivatives) for the delta-gamma-normal method.
        If gamma_matrix is None, will try to estimate gamma from price data.
        """
        n_assets = len(self.valid_assets)

        if gamma_matrix is None:
            # Initialize gamma matrix as zeros - will be estimated later if needed
            self.gamma_matrix = np.zeros((n_assets, n_assets))
            self.gamma_provided = False
        elif isinstance(gamma_matrix, pd.DataFrame):
            # Check if the dataframe has the correct asset labels
            if set(gamma_matrix.index) >= set(self.valid_assets) and set(gamma_matrix.columns) >= set(
                    self.valid_assets):
                # Extract the submatrix for valid assets
                self.gamma_matrix = gamma_matrix.loc[self.valid_assets, self.valid_assets].values
                self.gamma_provided = True
            else:
                raise ValueError("Gamma matrix DataFrame must have indices and columns matching valid assets")
        elif isinstance(gamma_matrix, np.ndarray):
            # Check if the array has the correct dimensions
            if gamma_matrix.shape == (n_assets, n_assets):
                self.gamma_matrix = gamma_matrix
                self.gamma_provided = True
            else:
                raise ValueError(f"Gamma matrix array must have shape ({n_assets}, {n_assets})")
        else:
            raise ValueError(f"Unsupported gamma_matrix type: {type(gamma_matrix)}")

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

    def _calculate_portfolio_return_series(self) -> pd.Series:
        """Calculate portfolio returns based on asset returns and weights"""
        portfolio_returns = pd.Series(0, index=self.data.index)

        for i, asset in enumerate(self.valid_assets):
            portfolio_returns += self.data[asset] * self.weights[i]

        return portfolio_returns

    def _detect_market_regime(self, return_series: pd.Series) -> pd.Series:
        """
        Detect high volatility market regimes.

        Returns a Series of 0/1 values where 1 indicates a high volatility regime
        """
        # Calculate long-term volatility (full window)
        long_term_vol = return_series.rolling(window=self.window, min_periods=self.min_periods).std()

        # Calculate short-term volatility (quarter of the window)
        short_term_window = max(5, self.window // 4)
        short_term_vol = return_series.rolling(window=short_term_window, min_periods=3).std()

        # Detect high volatility regimes where short-term vol is significantly higher than long-term
        high_vol_regime = (short_term_vol / long_term_vol) > self.market_regime_threshold

        # Fill NaN values with False (not high volatility)
        high_vol_regime = high_vol_regime.fillna(False).astype(int)

        return high_vol_regime

    def _estimate_gamma_from_returns(self) -> None:
        """
        Estimate gamma values from historical returns.
        This is a simplified approach - in practice, gamma would be calculated
        from option pricing models or provided directly.
        """
        if self.gamma_provided:
            return  # Skip if gamma was already provided

        n_assets = len(self.valid_assets)
        gamma = np.zeros((n_assets, n_assets))

        # Use price changes to approximate gamma
        # For each asset, regress squared returns against price changes
        try:
            # Calculate price changes
            price_changes = self.price_data[self.valid_assets].pct_change()

            # For each asset pair, estimate gamma using quadratic regression
            for i, asset_i in enumerate(self.valid_assets):
                for j, asset_j in enumerate(self.valid_assets):
                    if i == j:  # Diagonal elements (own-gamma)
                        # For own-gamma, we regress squared returns against squared price changes
                        X = price_changes[asset_i] ** 2
                        y = self.data[asset_i] ** 2

                        # Filter out NaN values
                        valid_idx = ~np.isnan(X) & ~np.isnan(y)
                        X_valid = X[valid_idx].values.reshape(-1, 1)
                        y_valid = y[valid_idx].values

                        if len(X_valid) > 10:  # Need sufficient data points
                            # Simple linear regression to estimate gamma (coefficient of squared term)
                            model = LinearRegression()
                            model.fit(X_valid, y_valid)
                            gamma[i, j] = model.coef_[0] / 2  # Divide by 2 for the proper gamma definition
                        else:
                            # Not enough data, use a conservative approximation based on volatility
                            vol = self.data[asset_i].std()
                            gamma[i, j] = vol * 0.5  # Simplified conservative estimate
                    else:
                        # Cross-gamma terms - correlation of squared returns
                        # This is a simplification; in practice, cross-gamma would be calculated
                        # using multivariate models or from option pricing
                        corr = self.data[asset_i].corr(self.data[asset_j])
                        vol_i = self.data[asset_i].std()
                        vol_j = self.data[asset_j].std()
                        gamma[i, j] = corr * vol_i * vol_j * 0.25  # Cross-gamma estimate

        except Exception as e:
            warnings.warn(f"Error estimating gamma matrix: {e}. Using conservative approximation.")
            # Use a simplified approach based on volatility
            for i, asset_i in enumerate(self.valid_assets):
                vol_i = self.data[asset_i].std()
                gamma[i, i] = vol_i * 0.5  # Diagonal elements

                for j in range(i + 1, n_assets):
                    asset_j = self.valid_assets[j]
                    corr = self.data[asset_i].corr(self.data[asset_j])
                    vol_j = self.data[asset_j].std()
                    gamma[i, j] = gamma[j, i] = corr * vol_i * vol_j * 0.25  # Off-diagonal elements

        # Ensure the gamma matrix is symmetric
        self.gamma_matrix = (gamma + gamma.T) / 2

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
            # Estimate gamma if not provided
            if not self.gamma_provided:
                self._estimate_gamma_from_returns()
            self._calculate_delta_gamma_normal_var()
        else:
            raise ValueError(f"Unknown method: {self.method}")

        # Skip the base class _finalize_result method entirely
        # and just clean up our result DataFrame
        return self.result.dropna(how='all')

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

        # Calculate portfolio returns for regime detection
        portfolio_returns = self._calculate_portfolio_return_series()

        # Detect market regimes (high volatility periods)
        high_vol_regime = self._detect_market_regime(portfolio_returns)

        # Calculate portfolio volatility using the rolling window
        portfolio_volatility = portfolio_returns.rolling(
            window=self.window,
            min_periods=self.min_periods
        ).std()

        # Calculate individual asset VaRs with gamma adjustments
        for i, asset in enumerate(self.valid_assets):
            # Standard deviation (first-order effect)
            volatility = self.data[asset].rolling(
                window=self.window,
                min_periods=self.min_periods
            ).std()

            # Calculate gamma adjustments based on own-gamma terms
            gamma_adj_series = pd.Series(0, index=self.data.index)

            for idx in range(len(self.data)):
                if idx >= self.window:
                    # Get a window of returns for covariance calculation
                    window_returns = self.data[self.valid_assets].iloc[idx - self.window:idx]

                    # Calculate covariance matrix for this window
                    if len(window_returns) >= self.min_periods:
                        try:
                            cov_matrix = window_returns.cov().values

                            # Calculate gamma adjustment using the gamma matrix
                            # For individual assets, only use own-gamma term
                            gamma_adjustment = 0.5 * self.gamma_matrix[i, i] * cov_matrix[i, i]

                            # Apply market regime scaling if in high volatility
                            if high_vol_regime.iloc[idx] == 1:
                                gamma_adjustment *= self.vol_scaling_factor

                            gamma_adj_series.iloc[idx] = gamma_adjustment
                        except Exception:
                            gamma_adj_series.iloc[idx] = np.nan
                    else:
                        gamma_adj_series.iloc[idx] = np.nan
                else:
                    gamma_adj_series.iloc[idx] = np.nan

            # Combine delta and gamma effects
            self.result[asset] = (volatility + gamma_adj_series) * z_score * scaling_factor

        # Calculate portfolio VaR with delta-gamma effects
        portfolio_gamma_adj = pd.Series(0, index=self.data.index)

        for idx in range(len(self.data)):
            if idx >= self.window:
                # Get a window of returns for covariance calculation
                window_returns = self.data[self.valid_assets].iloc[idx - self.window:idx]

                if len(window_returns) >= self.min_periods:
                    try:
                        # Calculate covariance matrix for this window
                        cov_matrix = window_returns.cov().values

                        # Calculate the weighted gamma term for portfolio
                        gamma_adjustment = 0

                        # Loop through all asset pairs to calculate gamma adjustment
                        for i in range(len(self.valid_assets)):
                            for j in range(len(self.valid_assets)):
                                # Apply weights and gamma matrix to covariance matrix
                                w_i = self.weights[i]
                                w_j = self.weights[j]
                                gamma_ij = self.gamma_matrix[i, j]
                                cov_ij = cov_matrix[i, j]

                                # Full gamma calculation for portfolio
                                gamma_adjustment += 0.5 * w_i * w_j * gamma_ij * cov_ij

                        # Apply market regime scaling if in high volatility
                        if high_vol_regime.iloc[idx] == 1:
                            gamma_adjustment *= self.vol_scaling_factor

                        portfolio_gamma_adj.iloc[idx] = gamma_adjustment
                    except Exception:
                        portfolio_gamma_adj.iloc[idx] = np.nan
                else:
                    portfolio_gamma_adj.iloc[idx] = np.nan
            else:
                portfolio_gamma_adj.iloc[idx] = np.nan

        # Combine delta and gamma effects for portfolio
        self.result['Portfolio'] = (portfolio_volatility + portfolio_gamma_adj) * z_score * scaling_factor