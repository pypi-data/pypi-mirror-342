"""
Module for statistical power analysis and related functions.
This module extends the pstatstools package with specialized functions
for power analysis, sample size calculations, and related statistical testing that are not necessarily sample or distribution locked.
"""

import numpy as np
import scipy.stats as stats
import statsmodels.stats.power as smp
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Union, Optional, Any, Callable


def welch_ttest(mean_A: float, mean_B: float, sd_A: float, sd_B: float, 
              n_A: int, n_B: Optional[int] = None, alpha: float = 0.05, 
              tail: str = "two") -> Dict[str, Any]:
    """
    Perform Welch's t-test for two samples with possibly unequal variances.
    
    Parameters:
    -----------
    mean_A, mean_B : float
        Sample means
    sd_A, sd_B : float
        Sample standard deviations
    n_A : int
        Sample size for group A
    n_B : int, optional
        Sample size for group B. Default is equal to n_A.
    alpha : float, optional
        Significance level. Default is 0.05.
    tail : str, optional
        Type of test: "two", "left", or "right". Default is "two".
        
    Returns:
    --------
    dict
        Dictionary with test results
    """
    if n_B is None:
        n_B = n_A
        
    mean_diff = mean_A - mean_B
    se_diff = np.sqrt((sd_A**2 / n_A) + (sd_B**2 / n_B))
    t_stat = mean_diff / se_diff
    
    df_numerator = ((sd_A**2 / n_A) + (sd_B**2 / n_B))**2
    df_denominator = ((sd_A**2 / n_A)**2 / (n_A-1)) + ((sd_B**2 / n_B)**2 / (n_B-1))
    df = df_numerator / df_denominator
    
    if tail == "two":
        p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df))
        t_crit = stats.t.ppf(1 - alpha/2, df)
        t_crits = (-t_crit, t_crit)
        reject = abs(t_stat) > t_crit
    elif tail == "right":
        p_value = 1 - stats.t.cdf(t_stat, df)
        t_crit = stats.t.ppf(1 - alpha, df)
        t_crits = (t_crit,)
        reject = t_stat > t_crit
    elif tail == "left":
        p_value = stats.t.cdf(t_stat, df)
        t_crit = stats.t.ppf(alpha, df)
        t_crits = (t_crit,)
        reject = t_stat < t_crit
    else:
        raise ValueError("Invalid tail type. Choose 'two', 'left', or 'right'.")
    
    ci_alpha = alpha
    if tail == "two":
        ci_alpha = alpha / 2
    
    margin = stats.t.ppf(1 - ci_alpha, df) * se_diff
    ci_lower = mean_diff - margin
    ci_upper = mean_diff + margin
    
    return {
        'test': f"{tail}-tailed Welch's t-test",
        'null_hypothesis': "The two population means are equal",
        'mean_difference': mean_diff,
        't_statistic': t_stat,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'standard_error': se_diff,
        'critical_values': t_crits,
        'confidence_interval': (ci_lower, ci_upper),
        'reject_null': reject,
        'conclusion': f"{'Reject' if reject else 'Fail to reject'} the null hypothesis at α = {alpha}."
    }


def calculate_power_welch(mean_diff: float, sd_A: float, sd_B: float, 
                        n_A: int, n_B: Optional[int] = None, 
                        alpha: float = 0.05, tail: str = "two") -> float:
    """
    Calculate statistical power for detecting a specified mean difference
    using Welch's t-test.
    
    Parameters:
    -----------
    mean_diff : float
        Mean difference to detect (μA - μB)
    sd_A, sd_B : float
        Sample standard deviations
    n_A : int
        Sample size for group A
    n_B : int, optional
        Sample size for group B. Default is equal to n_A.
    alpha : float, optional
        Significance level. Default is 0.05.
    tail : str, optional
        Type of test: "two", "left", or "right". Default is "two".
        
    Returns:
    --------
    float
        Statistical power (probability of rejecting H0 when H1 is true)
    """
    if n_B is None:
        n_B = n_A
    
    se_diff = np.sqrt((sd_A**2 / n_A) + (sd_B**2 / n_B))
    
    df_numerator = ((sd_A**2 / n_A) + (sd_B**2 / n_B))**2
    df_denominator = ((sd_A**2 / n_A)**2 / (n_A-1)) + ((sd_B**2 / n_B)**2 / (n_B-1))
    df = df_numerator / df_denominator
    
    ncp = mean_diff / se_diff
    
    if tail == "two":
        crit_value = stats.t.ppf(1 - alpha/2, df)
        power = 1 - stats.nct.cdf(crit_value, df, ncp) + stats.nct.cdf(-crit_value, df, ncp)
    elif tail == "right":
        crit_value = stats.t.ppf(1 - alpha, df)
        power = 1 - stats.nct.cdf(crit_value, df, ncp)
    elif tail == "left":
        crit_value = stats.t.ppf(alpha, df)
        power = stats.nct.cdf(crit_value, df, ncp)
    else:
        raise ValueError("Invalid tail type. Choose 'two', 'left', or 'right'.")
    
    return power


def calculate_sample_size_welch(mean_diff: float, sd_A: float, sd_B: float,
                             power: float = 0.8, alpha: float = 0.05,
                             tail: str = "two", max_n: int = 1000) -> Tuple[int, float]:
    """
    Calculate required sample size to detect a specified mean difference
    with desired power using Welch's t-test.
    
    Parameters:
    -----------
    mean_diff : float
        Mean difference to detect (μA - μB)
    sd_A, sd_B : float
        Sample standard deviations
    power : float, optional
        Desired statistical power. Default is 0.8.
    alpha : float, optional
        Significance level. Default is 0.05.
    tail : str, optional
        Type of test: "two", "left", or "right". Default is "two".
    max_n : int, optional
        Maximum sample size to check. Default is 1000.
        
    Returns:
    --------
    tuple
        (required sample size, actual power achieved)
    """
    for n in range(2, max_n + 1):
        achieved_power = calculate_power_welch(
            mean_diff=mean_diff,
            sd_A=sd_A,
            sd_B=sd_B,
            n_A=n,
            n_B=n,
            alpha=alpha,
            tail=tail
        )
        
        if achieved_power >= power:
            return n, achieved_power
    
    return max_n, calculate_power_welch(
        mean_diff=mean_diff,
        sd_A=sd_A,
        sd_B=sd_B,
        n_A=max_n,
        n_B=max_n,
        alpha=alpha,
        tail=tail
    )


def calculate_detectable_difference(sd_A: float, sd_B: float, n_A: int,
                                  n_B: Optional[int] = None, power: float = 0.8,
                                  alpha: float = 0.05, tail: str = "two") -> float:
    """
    Calculate the minimum detectable mean difference with specified power.
    
    Parameters:
    -----------
    sd_A, sd_B : float
        Sample standard deviations
    n_A : int
        Sample size for group A
    n_B : int, optional
        Sample size for group B. Default is equal to n_A.
    power : float, optional
        Desired statistical power. Default is 0.8.
    alpha : float, optional
        Significance level. Default is 0.05.
    tail : str, optional
        Type of test: "two", "left", or "right". Default is "two".
        
    Returns:
    --------
    float
        Minimum detectable mean difference
    """
    if n_B is None:
        n_B = n_A
    
    def get_power(diff):
        return calculate_power_welch(
            mean_diff=diff,
            sd_A=sd_A,
            sd_B=sd_B,
            n_A=n_A,
            n_B=n_B,
            alpha=alpha,
            tail=tail
        )
    
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    low = 0.001 * pooled_sd
    high = 5.0 * pooled_sd
    
    while high - low > 0.001 * pooled_sd:
        mid = (low + high) / 2
        if get_power(mid) < power:
            low = mid
        else:
            high = mid
    
    return (low + high) / 2


def power_curve(mean_diff: float, sd_A: float, sd_B: float,
              n_range: Tuple[int, int], alpha: float = 0.05,
              tail: str = "two", n_points: int = 20) -> plt.Figure:
    """
    Generate a power curve showing how power changes with sample size.
    
    Parameters:
    -----------
    mean_diff : float
        Mean difference to detect (μA - μB)
    sd_A, sd_B : float
        Sample standard deviations
    n_range : tuple
        (min_n, max_n) range of sample sizes to consider
    alpha : float, optional
        Significance level. Default is 0.05.
    tail : str, optional
        Type of test: "two", "left", or "right". Default is "two".
    n_points : int, optional
        Number of points to plot on the curve. Default is 20.
        
    Returns:
    --------
    matplotlib.figure.Figure
        Power curve figure
    """
    min_n, max_n = n_range
    
    n_values = np.linspace(min_n, max_n, n_points)
    n_values = np.round(n_values).astype(int)
    
    power_values = [
        calculate_power_welch(
            mean_diff=mean_diff,
            sd_A=sd_A,
            sd_B=sd_B,
            n_A=n,
            n_B=n,
            alpha=alpha,
            tail=tail
        )
        for n in n_values
    ]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(n_values, power_values, 'o-', linewidth=2, markersize=8)

    ax.axhline(y=0.8, linestyle='--', color='r', alpha=0.7, label='Power = 0.8')
    
    ax.set_xlabel('Sample Size (per group)', fontsize=12)
    ax.set_ylabel('Statistical Power', fontsize=12)
    ax.set_title(f'Power Curve for Detecting Mean Difference of {mean_diff}', fontsize=14)
    
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    ax.set_xlim(min_n, max_n)
    ax.set_ylim(0, 1.05)
    
    plt.tight_layout()
    return fig


def effect_size_curve(sd_A: float, sd_B: float, n: int, 
                     diff_range: Tuple[float, float], alpha: float = 0.05,
                     tail: str = "two", n_points: int = 20) -> plt.Figure:
    """
    Generate a curve showing how power changes with effect size.
    
    Parameters:
    -----------
    sd_A, sd_B : float
        Sample standard deviations
    n : int
        Sample size per group
    diff_range : tuple
        (min_diff, max_diff) range of mean differences to consider
    alpha : float, optional
        Significance level. Default is 0.05.
    tail : str, optional
        Type of test: "two", "left", or "right". Default is "two".
    n_points : int, optional
        Number of points to plot on the curve. Default is 20.
        
    Returns:
    --------
    matplotlib.figure.Figure
        Power vs. effect size curve
    """
    min_diff, max_diff = diff_range
    
    diff_values = np.linspace(min_diff, max_diff, n_points)
    
    power_values = [
        calculate_power_welch(
            mean_diff=diff,
            sd_A=sd_A,
            sd_B=sd_B,
            n_A=n,
            n_B=n,
            alpha=alpha,
            tail=tail
        )
        for diff in diff_values
    ]
    
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    d_values = diff_values / pooled_sd
    
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    line1 = ax1.plot(diff_values, power_values, 'o-', linewidth=2, 
                    markersize=8, color='blue', label='Power')
    ax1.set_xlabel('Mean Difference (μA - μB)', fontsize=12)
    ax1.set_ylabel('Statistical Power', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    ax1.axhline(y=0.8, linestyle='--', color='r', alpha=0.7, label='Power = 0.8')
    
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_xticks(diff_values[::4])  # Show fewer ticks
    ax2.set_xticklabels([f'{d:.2f}' for d in d_values[::4]])
    ax2.set_xlabel("Effect Size (Cohen's d)", fontsize=12)
    
    ax1.set_title(f'Power vs. Effect Size (n={n} per group)', fontsize=14)
    
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    ax1.set_ylim(0, 1.05)
    
    plt.tight_layout()
    return fig


def power_analysis_report(mean_A: float, mean_B: float, sd_A: float, sd_B: float, 
                        n: int, alpha: float = 0.05, 
                        tail: str = "two") -> Dict[str, Any]:
    """
    Generate a comprehensive power analysis report.
    
    Parameters:
    -----------
    mean_A, mean_B : float
        Sample means
    sd_A, sd_B : float
        Sample standard deviations
    n : int
        Sample size per group
    alpha : float, optional
        Significance level. Default is 0.05.
    tail : str, optional
        Type of test: "two", "left", or "right". Default is "two".
        
    Returns:
    --------
    dict
        Comprehensive power analysis report
    """
    mean_diff = mean_A - mean_B
    
    test_result = welch_ttest(
        mean_A=mean_A,
        mean_B=mean_B,
        sd_A=sd_A,
        sd_B=sd_B,
        n_A=n,
        n_B=n,
        alpha=alpha,
        tail=tail
    )
    
    observed_power = calculate_power_welch(
        mean_diff=mean_diff,
        sd_A=sd_A,
        sd_B=sd_B,
        n_A=n,
        n_B=n,
        alpha=alpha,
        tail=tail
    )
    
    required_n, actual_power = calculate_sample_size_welch(
        mean_diff=mean_diff,
        sd_A=sd_A,
        sd_B=sd_B,
        power=0.8,
        alpha=alpha,
        tail=tail
    )
    
    min_diff = calculate_detectable_difference(
        sd_A=sd_A,
        sd_B=sd_B,
        n_A=n,
        n_B=n,
        power=0.8,
        alpha=alpha,
        tail=tail
    )
    
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    observed_effect_size = mean_diff / pooled_sd
    min_effect_size = min_diff / pooled_sd
    
    report = {
        'test': test_result,
        'observed_difference': {
            'mean_diff': mean_diff,
            'effect_size': observed_effect_size,
            'power': observed_power
        },
        'sample_size_analysis': {
            'current_n': n,
            'required_n_for_80_power': required_n,
            'actual_power_at_required_n': actual_power
        },
        'minimum_detectable_difference': {
            'min_diff': min_diff,
            'min_effect_size': min_effect_size
        }
    }
    
    return report


def print_power_report(report: Dict[str, Any]) -> None:
    """
    Print a formatted power analysis report.
    
    Parameters:
    -----------
    report : dict
        Power analysis report from power_analysis_report()
    """
    test = report['test']
    obs = report['observed_difference']
    sample = report['sample_size_analysis']
    min_det = report['minimum_detectable_difference']
    
    print("===== POWER ANALYSIS REPORT =====")
    print("\n--- HYPOTHESIS TEST RESULTS ---")
    print(f"Test: {test['test']}")
    print(f"Null Hypothesis: {test['null_hypothesis']}")
    print(f"t-statistic: {test['t_statistic']:.4f}")
    print(f"Degrees of freedom: {test['degrees_of_freedom']:.4f}")
    print(f"p-value: {test['p_value']:.4f}")
    print(f"Conclusion: {test['conclusion']}")
    
    print("\n--- OBSERVED EFFECT ---")
    print(f"Mean difference: {obs['mean_diff']:.4f}")
    print(f"Effect size (Cohen's d): {obs['effect_size']:.4f}")
    print(f"Power: {obs['power']:.4f}")
    
    print("\n--- SAMPLE SIZE ANALYSIS ---")
    print(f"Current sample size: {sample['current_n']} per group")
    print(f"Required sample size for 80% power: {sample['required_n_for_80_power']} per group")
    print(f"Power with required sample size: {sample['actual_power_at_required_n']:.4f}")
    
    print("\n--- MINIMUM DETECTABLE DIFFERENCE ---")
    print(f"Minimum detectable difference (80% power): {min_det['min_diff']:.4f}")
    print(f"Minimum detectable effect size (80% power): {min_det['min_effect_size']:.4f}")
    
    print("\n--- INTERPRETATION GUIDE ---")
    print("Effect Size (Cohen's d):")
    print("  Small: d = 0.2")
    print("  Medium: d = 0.5")
    print("  Large: d = 0.8")
    
    print("\nPower:")
    print("  < 0.5: Very low, not recommended")
    print("  0.5-0.7: Low power, risk of Type II error")
    print("  0.8-0.9: Conventional acceptable power")
    print("  > 0.9: High power")
    
    es = obs['effect_size']
    size_interp = "small" if es < 0.5 else "medium" if es < 0.8 else "large"
    
    power = obs['power']
    power_interp = "very low" if power < 0.5 else "low" if power < 0.8 else "adequate" if power < 0.9 else "high"
    
    print("\nSummary Interpretation:")
    print(f"The observed effect size is {es:.2f}, which is considered {size_interp}.")
    print(f"The statistical power is {power:.2f}, which is {power_interp}.")
    
    if power < 0.8:
        print(f"To achieve 80% power, increase sample size to {sample['required_n_for_80_power']} per group.")
    else:
        print("The current sample size provides adequate power for the observed effect.")


def cohen_d(mean_diff: float, sd_A: float, sd_B: float) -> float:
    """
    Calculate Cohen's d effect size for two independent samples.
    
    Parameters:
    -----------
    mean_diff : float
        Difference between means (mean_A - mean_B)
    sd_A, sd_B : float
        Standard deviations of the two groups
        
    Returns:
    --------
    float
        Cohen's d effect size
    """
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    d = mean_diff / pooled_sd
    
    return d