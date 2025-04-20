"""
Function-based API for the SquareQuant package
"""

from typing import List, Optional, Union, Dict
import pandas as pd

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
    DEFAULT_ERM_WINDOW,
    DEFAULT_EVAR_WINDOW,
    DEFAULT_CDAR_WINDOW,
    DEFAULT_EDAR_WINDOW,
    DEFAULT_VAR_HOLDING_PERIOD,
    DEFAULT_VAR_CONFIDENCE
)

from squarequant.core.metrics import (
    SharpeRatio,
    SortinoRatio,
    Volatility,
    MaximumDrawdown,
    CalmarRatio,
    ConditionalValueAtRisk,
    SemiDeviation,
    AverageDrawdown,
    UlcerIndex,
    MeanAbsoluteDeviation,
    EntropicRiskMeasure,
    EntropicValueAtRisk,
    ConditionalDrawdownAtRisk,
    EntropicDrawdownAtRisk
)

from squarequant.var.valueatrisk import (
    ValueAtRisk
)


def sharpe(data: pd.DataFrame,
           assets: List[str],
           freerate: Optional[str] = None,
           freerate_value: Optional[float] = None,
           window: int = DEFAULT_SHARPE_WINDOW,
           start: Optional[str] = None,
           end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate rolling Sharpe ratios for specified assets

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    freerate (str, optional): Column name for risk-free rate in data DataFrame
    freerate_value (float, optional): Constant risk-free rate to use if no column provided
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Rolling Sharpe ratios for specified assets
    """
    calculator = SharpeRatio(
        data=data,
        assets=assets,
        freerate=freerate,
        freerate_value=freerate_value,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()


def sortino(data: pd.DataFrame,
            assets: List[str],
            freerate: Optional[str] = None,
            freerate_value: Optional[float] = None,
            window: int = DEFAULT_SORTINO_WINDOW,
            start: Optional[str] = None,
            end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate rolling Sortino ratios for specified assets

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    freerate (str, optional): Column name for risk-free rate in data DataFrame
    freerate_value (float, optional): Constant risk-free rate to use if no column provided
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Rolling Sortino ratios for specified assets
    """
    calculator = SortinoRatio(
        data=data,
        assets=assets,
        freerate=freerate,
        freerate_value=freerate_value,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()


def vol(data: pd.DataFrame,
        assets: List[str],
        window: int = DEFAULT_VOLATILITY_WINDOW,
        start: Optional[str] = None,
        end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate annualized rolling volatility for specified assets

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    window (int): Rolling window size in trading days, default is 10 days
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Rolling annualized volatility for specified assets
    """
    calculator = Volatility(
        data=data,
        assets=assets,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()


def mdd(data: pd.DataFrame,
        assets: List[str],
        window: int = DEFAULT_DRAWDOWN_WINDOW,
        start: Optional[str] = None,
        end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate the maximum drawdown for selected assets over a given time period

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate drawdown for
    window (int): Rolling window size in days, default is 181 days
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Rolling maximum drawdown for specified assets
    """
    calculator = MaximumDrawdown(
        data=data,
        assets=assets,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()

def calmar(data: pd.DataFrame,
           assets: List[str],
           window: int = DEFAULT_CALMAR_WINDOW,
           start: Optional[str] = None,
           end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate rolling Calmar ratios for specified assets

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Rolling Calmar ratios for specified assets
    """
    calculator = CalmarRatio(
        data=data,
        assets=assets,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()

def var(
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
        decay_factor: Optional[float] = None
) -> pd.DataFrame:
    # Initialize ValueAtRisk object
    var_calculator = ValueAtRisk(
        data=data,
        assets=assets,
        confidence=confidence,
        window=window,
        start=start,
        end=end,
        method=method,
        holding_period=holding_period,
        scaling_method=scaling_method,
        weights=weights
    )

    # Calculate VaR
    return var_calculator.calculate()

def cvar(data: pd.DataFrame,
         assets: List[str],
         confidence: float = DEFAULT_CONFIDENCE,
         window: int = DEFAULT_CVAR_WINDOW,
         start: Optional[str] = None,
         end: Optional[str] = None,
         method: str = 'historical',
         holding_period: int = DEFAULT_VAR_HOLDING_PERIOD,  # Add parameter
         scaling_method: str = 'sqrt_time') -> pd.DataFrame:  # Add parameter
    """
    Calculate rolling Conditional Value at Risk (CVaR) for specified assets

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate CVaR for
    confidence (float): Confidence level (0-1), default is 0.95 (95%)
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'
    method (str): Method to calculate CVaR - 'historical', 'parametric', default is 'historical'
    holding_period (int): Holding period in days, default is 10 days
    scaling_method (str): Method to scale 1-day CVaR, default is 'sqrt_time'

    Returns:
    DataFrame: Rolling CVaR for specified assets
    """
    calculator = ConditionalValueAtRisk(
        data=data,
        assets=assets,
        confidence=confidence,
        window=window,
        start=start,
        end=end,
        method=method,
        holding_period=holding_period,  # Pass parameter
        scaling_method=scaling_method  # Pass parameter
    )
    return calculator.calculate()

def semidev(data: pd.DataFrame,
            assets: List[str],
            target_return: Optional[float] = None,
            window: int = DEFAULT_SEMIDEVIATION_WINDOW,
            start: Optional[str] = None,
            end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate the semi-deviation (downside volatility) for specified assets.

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    target_return (float, optional): Target return threshold. If None, the mean return is used
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Semi-deviation for specified assets
    """
    calculator = SemiDeviation(
        data=data,
        assets=assets,
        target_return=target_return,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()


def avgdd(data: pd.DataFrame,
         assets: List[str],
         window: int = DEFAULT_AVGDRAWDOWN_WINDOW,
         start: Optional[str] = None,
         end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate the average drawdown for specified assets.

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate average drawdown for
    window (int): Rolling window size in days, default is 181 days
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Average drawdown for specified assets
    """
    calculator = AverageDrawdown(
        data=data,
        assets=assets,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()


def ulcer(data: pd.DataFrame,
         assets: List[str],
         window: int = DEFAULT_ULCER_WINDOW,
         start: Optional[str] = None,
         end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate the Ulcer Index for specified assets.
    The Ulcer Index is the square root of the mean of the squared drawdowns.

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate Ulcer Index for
    window (int): Rolling window size in days, default is 181 days
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Ulcer Index for specified assets
    """
    calculator = UlcerIndex(
        data=data,
        assets=assets,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()


def mad(data: pd.DataFrame,
       assets: List[str],
       window: int = DEFAULT_MAD_WINDOW,
       start: Optional[str] = None,
       end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate the Mean Absolute Deviation (MAD) for specified assets.

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate MAD for
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: Mean Absolute Deviation for specified assets
    """
    calculator = MeanAbsoluteDeviation(
        data=data,
        assets=assets,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()

def erm(data: pd.DataFrame,
        assets: List[str],
        z: float = 1.0,
        confidence: float = DEFAULT_CONFIDENCE,
        window: int = DEFAULT_ERM_WINDOW,
        start: Optional[str] = None,
        end: Optional[str] = None,
        method: str = 'historical',
        holding_period: int = 1,
        scaling_method: str = 'sqrt_time',
        decay_factor: float = 0.94) -> pd.DataFrame:
    """
    Calculate the Entropic Risk Measure (ERM) for specified assets.

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    z (float): Risk aversion parameter, must be greater than zero. Default is 1.0
    confidence (float): Significance level (0-1), default is 0.95 (95%)
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'
    method (str, optional): Method to use for calculation: 'historical', 'parametric', or 'weighted'.
                           Default is 'historical'
    holding_period (int, optional): Time horizon for risk projection. Default is 1
    scaling_method (str, optional): Method to scale for holding period: 'sqrt_time', 'linear', or 'none'.
                                   Default is 'sqrt_time'
    decay_factor (float, optional): Decay factor for weighted method (between 0 and 1). Default is 0.94

    Returns:
    DataFrame: Entropic Risk Measure for specified assets
    """
    calculator = EntropicRiskMeasure(
        data=data,
        assets=assets,
        z=z,
        confidence=confidence,
        window=window,
        start=start,
        end=end,
        holding_period=holding_period,
        scaling_method=scaling_method
    )
    return calculator.calculate()

def evar(
        data: pd.DataFrame,
        assets: List[str],
        confidence: float = DEFAULT_CONFIDENCE,  # Changed from alpha to confidence
        window: int = DEFAULT_EVAR_WINDOW,
        start: Optional[str] = None,
        end: Optional[str] = None,
        holding_period: int = 1,
        scaling_method: str = 'sqrt_time',
        z_bounds: tuple = (0.1, 10.0),  # Added z_bounds parameter
        z_default: float = 1.0  # Changed from initial_z to z_default
) -> pd.DataFrame:
    """
    Calculate Entropic Value at Risk for specified assets.

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    confidence (float): Confidence level (0-1), default is 0.95 (95%)
    window (int): Rolling window size in trading days, default is 252 (1 year)
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'
    method (str, optional): Method to use - 'historical', 'parametric', or 'weighted'. Default is 'parametric'
    holding_period (int): Time horizon for risk projection, default is 1
    scaling_method (str): Method to scale 1-day EVaR, default is 'sqrt_time'
    z_bounds (tuple): Bounds for z parameter optimization (lower, upper). Default is (0.1, 10.0)
    z_default (float): Default z value to use if optimization fails. Default is 1.0

    Returns:
    DataFrame: Entropic Value at Risk for specified assets
    """
    calculator = EntropicValueAtRisk(
        data=data,
        assets=assets,
        confidence=confidence,  # Match the parameter name with the class
        window=window,
        start=start,
        end=end,
        holding_period=holding_period,
        scaling_method=scaling_method,
        z_bounds=z_bounds,
        z_default=z_default
    )
    return calculator.calculate()


def cdar(data: pd.DataFrame,
         assets: List[str],
         confidence: float = DEFAULT_CONFIDENCE,
         window: int = DEFAULT_CDAR_WINDOW,
         start: Optional[str] = None,
         end: Optional[str] = None) -> pd.DataFrame:
    """
    Calculate the Conditional Drawdown at Risk (CDaR) for specified assets

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate CDaR for
    confidence (float): Confidence level (0-1), default is 0.95 (95%)
    window (int): Rolling window size in days, default is 181 days
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'

    Returns:
    DataFrame: CDaR for specified assets
    """
    calculator = ConditionalDrawdownAtRisk(
        data=data,
        assets=assets,
        confidence=confidence,
        window=window,
        start=start,
        end=end
    )
    return calculator.calculate()


def edar(data: pd.DataFrame,
         assets: List[str],
         confidence: float = DEFAULT_CONFIDENCE,
         window: int = DEFAULT_EDAR_WINDOW,
         start: Optional[str] = None,
         end: Optional[str] = None,
         solver: Optional[str] = None,
         batch_size: int = 1,
         fallback_z_min: float = 0.01,
         fallback_z_max: float = 100.0,
         fallback_steps: int = 20) -> pd.DataFrame:
    """
    Calculate the Entropic Drawdown at Risk (EDaR) for specified assets.
    This implementation uses convex optimization via CVXPY when available,
    with fallback to grid search if needed.

    Parameters:
    data (DataFrame): DataFrame with asset price data
    assets (List[str]): List of asset columns to calculate for
    confidence (float): Confidence level (0-1), default is 0.95 (95%)
    window (int): Rolling window size in days, default is 181 days
    start (str, optional): Start date in format 'YYYY-MM-DD'
    end (str, optional): End date in format 'YYYY-MM-DD'
    solver (str, optional): CVXPY solver to use (e.g., 'MOSEK', 'ECOS', 'SCS')
                           If None, CVXPY will choose automatically.
    batch_size (int): Number of assets to process in one batch for memory efficiency
    fallback_z_min (float): Minimum value of z for fallback grid search
    fallback_z_max (float): Maximum value of z for fallback grid search
    fallback_steps (int): Number of steps for fallback grid search

    Returns:
    DataFrame: Entropic Drawdown at Risk for specified assets
    """
    calculator = EntropicDrawdownAtRisk(
        data=data,
        assets=assets,
        confidence=confidence,
        window=window,
        start=start,
        end=end,
        solver=solver,
        batch_size=batch_size,
        fallback_z_min=fallback_z_min,
        fallback_z_max=fallback_z_max,
        fallback_steps=fallback_steps
    )
    return calculator.calculate()