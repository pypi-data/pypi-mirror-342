"""
Module for statistical power analysis and related functions, aligned with
"Introduction to Statistics at DTU" textbook methodology.

This module uses statsmodels for core power calculations and scipy.stats
for hypothesis testing, providing functions for power analysis, sample size
calculations, and related statistical testing for two independent samples.
"""

import numpy as np
import scipy.stats as stats
# Use ttest_ind_from_stats for performing t-test directly from summary statistics
from scipy.stats import ttest_ind_from_stats
import statsmodels.stats.power as smp
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Union, Optional, Any, Callable

def ttest_power_analysis(effect_size: float, nobs: int = None, alpha: float = 0.05,
                         power: float = None, ratio: float = 1.0,
                         alternative: str = 'two-sided') -> float:
    """
    Perform power analysis for t-test using statsmodels TTestIndPower.

    This function acts as a wrapper for statsmodels.stats.power.TTestIndPower().solve_power,
    aligning with the textbook's methodology (e.g., Chapter 4, Examples 4.46, 4.49).
    It can solve for power, sample size (nobs1), effect size, or alpha.

    Parameters:
    -----------
    effect_size : float
        Effect size (Cohen's d) - the standardized mean difference.
        Calculated as (mean1 - mean2) / pooled_sd.
    nobs : int, optional
        Number of observations in the first sample (n1). If solving for sample size,
        this should be None.
    alpha : float, optional
        Significance level (Type I error rate). Default is 0.05. If solving for alpha,
        this should be None.
    power : float, optional
        Power of the test (1 - probability of Type II error). Default is None.
        If solving for power, this should be None.
    ratio : float, optional
        Ratio of sample sizes (nobs2 / nobs1). Default is 1.0 (equal sizes).
    alternative : str, optional
        Direction of the alternative hypothesis: 'two-sided' (default),
        'larger' (right-tailed), 'smaller' (left-tailed).

    Returns:
    --------
    float
        The calculated value for the parameter specified as None in the input
        (power, nobs1, effect_size, or alpha).
    """
    # Validate and map alternative hypothesis string if necessary (already matches statsmodels)
    valid_alternatives = ['two-sided', 'larger', 'smaller']
    if alternative not in valid_alternatives:
        # Map common alternatives if needed, otherwise raise error
        if alternative in ['two', '2-sided']:
             alternative = 'two-sided'
        elif alternative in ['right', 'greater']:
             alternative = 'larger'
        elif alternative in ['left', 'less']:
             alternative = 'smaller'
        else:
            raise ValueError(f"Invalid alternative: {alternative}. Choose from {valid_alternatives}")

    # Use statsmodels to solve for the missing parameter
    result = smp.TTestIndPower().solve_power(
        effect_size=effect_size,
        nobs1=nobs,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative=alternative
    )

    return result

# --- Functions assuming equal variance (using pooled SD) ---

def calculate_power(delta: float, sd: float, n: int, alpha: float = 0.05,
                    alternative: str = 'two-sided', ratio: float = 1.0) -> float:
    """
    Calculate statistical power for detecting a mean difference (assuming equal variance).

    Uses the textbook's approach based on statsmodels TTestIndPower.

    Parameters:
    -----------
    delta : float
        Mean difference to detect (mean_A - mean_B).
    sd : float
        Pooled standard deviation (assumed equal for both groups).
    n : int
        Sample size for the first group (n1).
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.
    ratio : float, optional
        Ratio of sample sizes (n2/n1). Default is 1.0 (equal sizes).

    Returns:
    --------
    float
        Statistical power (probability of rejecting H0 when H1 is true).
    """
    # Calculate Cohen's d effect size using the provided pooled SD
    effect_size = delta / sd

    # Calculate power using the core statsmodels wrapper
    power = ttest_power_analysis(
        effect_size=effect_size,
        nobs=n,
        alpha=alpha,
        power=None, # Solve for power
        alternative=alternative,
        ratio=ratio
    )

    return power

def calculate_sample_size(delta: float, sd: float, power: float = 0.8,
                          alpha: float = 0.05, alternative: str = 'two-sided',
                          ratio: float = 1.0) -> int:
    """
    Calculate required sample size (per group if ratio=1) for a given power
    (assuming equal variance).

    Uses the textbook's approach based on statsmodels TTestIndPower.

    Parameters:
    -----------
    delta : float
        Mean difference to detect (mean_A - mean_B).
    sd : float
        Pooled standard deviation (assumed equal for both groups).
    power : float, optional
        Desired statistical power. Default is 0.8.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.
    ratio : float, optional
        Ratio of sample sizes (n2/n1). Default is 1.0 (equal sizes).

    Returns:
    --------
    int
        Required sample size for the first group (n1). If ratio=1, this is the
        size per group.
    """
    # Calculate Cohen's d effect size using the provided pooled SD
    effect_size = delta / sd

    # Calculate required sample size (nobs1) using the core statsmodels wrapper
    n = ttest_power_analysis(
        effect_size=effect_size,
        nobs=None, # Solve for nobs1
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )

    # Return sample size rounded up to the nearest integer
    return int(np.ceil(n))

def calculate_detectable_difference(sd: float, n: int, power: float = 0.8,
                                    alpha: float = 0.05, alternative: str = 'two-sided',
                                    ratio: float = 1.0) -> float:
    """
    Calculate the minimum detectable mean difference for a given power and sample size
    (assuming equal variance).

    Uses the textbook's approach based on statsmodels TTestIndPower.

    Parameters:
    -----------
    sd : float
        Pooled standard deviation (assumed equal for both groups).
    n : int
        Sample size for the first group (n1).
    power : float, optional
        Desired statistical power. Default is 0.8.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.
    ratio : float, optional
        Ratio of sample sizes (n2/n1). Default is 1.0 (equal sizes).

    Returns:
    --------
    float
        Minimum detectable mean difference (delta).
    """
    # Calculate the minimum detectable effect size (Cohen's d)
    effect_size = ttest_power_analysis(
        effect_size=None, # Solve for effect size
        nobs=n,
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )

    # Convert effect size back to the mean difference scale
    return effect_size * sd

# --- Functions handling potentially unequal variances (Welch's approach) ---
# Note: These functions use statsmodels power calculations which are based on
# Cohen's d (calculated using a form of pooled SD). They provide an approximation
# for the Welch scenario power using the textbook's recommended tool.
# The actual Welch's t-test (allowing unequal variances) is performed in the
# report function using scipy.stats.ttest_ind_from_stats(equal_var=False).

def cohen_d_unpooled(mean_diff: float, sd_A: float, sd_B: float) -> float:
    """
    Calculate Cohen's d effect size using the average of variances (unpooled).

    This is often used as input for power calculations when variances might differ.

    Parameters:
    -----------
    mean_diff : float
        Difference between means (mean_A - mean_B).
    sd_A, sd_B : float
        Standard deviations of the two groups.

    Returns:
    --------
    float
        Cohen's d effect size based on averaged variance.
    """
    # Calculate pooled standard deviation based on averaging variances
    # This is a common approach for Cohen's d when variances are unequal.
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    if pooled_sd == 0:
        return 0 # Avoid division by zero if both SDs are 0
    d = mean_diff / pooled_sd
    return d

def calculate_power_welch(mean_diff: float, sd_A: float, sd_B: float,
                          n_A: int, n_B: Optional[int] = None,
                          alpha: float = 0.05, alternative: str = "two-sided") -> float:
    """
    Calculate statistical power for Welch's t-test scenario (unequal variances).

    Approximates power by calculating Cohen's d using averaged variance and then
    using statsmodels TTestIndPower, consistent with textbook tools.

    Parameters:
    -----------
    mean_diff : float
        Mean difference to detect (μA - μB).
    sd_A, sd_B : float
        Standard deviations of groups A and B.
    n_A : int
        Sample size for group A.
    n_B : int, optional
        Sample size for group B. Default is equal to n_A.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.

    Returns:
    --------
    float
        Approximate statistical power for the Welch's test scenario.
    """
    if n_B is None:
        n_B = n_A

    # Calculate effect size using averaged variance
    effect_size = cohen_d_unpooled(mean_diff, sd_A, sd_B)

    # Calculate sample size ratio
    ratio = n_B / n_A

    # Calculate power using the core statsmodels wrapper
    power = ttest_power_analysis(
        effect_size=effect_size,
        nobs=n_A,
        alpha=alpha,
        power=None, # Solve for power
        alternative=alternative,
        ratio=ratio
    )
    return power

def calculate_sample_size_welch(mean_diff: float, sd_A: float, sd_B: float,
                                power: float = 0.8, alpha: float = 0.05,
                                alternative: str = 'two-sided', ratio: float = 1.0) -> int:
    """
    Calculate required sample size (n1) for Welch's t-test scenario (unequal variances).

    Approximates required size by calculating Cohen's d using averaged variance
    and then using statsmodels TTestIndPower.

    Parameters:
    -----------
    mean_diff : float
        Mean difference to detect (μA - μB).
    sd_A, sd_B : float
        Standard deviations of groups A and B.
    power : float, optional
        Desired statistical power. Default is 0.8.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.
    ratio : float, optional
        Ratio of sample sizes (n2/n1). Default is 1.0 (equal sizes).

    Returns:
    --------
    int
        Required sample size for the first group (n1). If ratio=1, this is the
        approximate size per group needed.
    """
    # Calculate effect size using averaged variance
    effect_size = cohen_d_unpooled(mean_diff, sd_A, sd_B)

    # Calculate required sample size (nobs1) using the core statsmodels wrapper
    n = ttest_power_analysis(
        effect_size=effect_size,
        nobs=None, # Solve for nobs1
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )
    # Return sample size rounded up
    return int(np.ceil(n))

def calculate_detectable_difference_welch(sd_A: float, sd_B: float, n_A: int,
                                          n_B: Optional[int] = None, power: float = 0.8,
                                          alpha: float = 0.05, alternative: str = 'two-sided') -> float:
    """
    Calculate minimum detectable difference for Welch's t-test scenario (unequal variances).

    Approximates the difference by using statsmodels TTestIndPower to find the
    required Cohen's d (based on averaged variance) and converting it back.

    Parameters:
    -----------
    sd_A, sd_B : float
        Standard deviations of groups A and B.
    n_A : int
        Sample size for group A.
    n_B : int, optional
        Sample size for group B. Default is equal to n_A.
    power : float, optional
        Desired statistical power. Default is 0.8.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.

    Returns:
    --------
    float
        Approximate minimum detectable mean difference for the Welch's test scenario.
    """
    if n_B is None:
        n_B = n_A

    # Calculate sample size ratio
    ratio = n_B / n_A

    # Calculate the minimum detectable effect size (Cohen's d)
    effect_size = ttest_power_analysis(
        effect_size=None, # Solve for effect size
        nobs=n_A,
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )

    # Convert effect size back to mean difference using the averaged SD
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    return effect_size * pooled_sd

# --- Plotting Functions ---

def power_curve(delta: float, sd: float, n_range: Tuple[int, int],
                alpha: float = 0.05, alternative: str = 'two-sided',
                n_points: int = 20, ratio: float = 1.0) -> plt.Figure:
    """
    Generate a power curve showing how power changes with sample size (n1).

    Assumes equal variance (uses pooled sd) consistent with `calculate_power`.

    Parameters:
    -----------
    delta : float
        Mean difference to detect (μA - μB).
    sd : float
        Pooled standard deviation.
    n_range : tuple
        (min_n1, max_n1) range of sample sizes for group 1 to consider.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.
    n_points : int, optional
        Number of points to plot on the curve. Default is 20.
    ratio : float, optional
        Ratio of sample sizes (n2/n1). Default is 1.0.

    Returns:
    --------
    matplotlib.figure.Figure
        Power curve figure.
    """
    min_n, max_n = n_range
    # Ensure minimum n is at least 2 for t-test calculations
    min_n = max(2, min_n)
    if max_n < min_n:
        max_n = min_n + n_points # Ensure range is valid

    # Generate sample sizes (n1)
    n_values = np.linspace(min_n, max_n, n_points)
    n_values = np.round(n_values).astype(int)
    # Ensure uniqueness and minimum value
    n_values = np.unique(n_values)
    n_values = n_values[n_values >= 2]
    if len(n_values) == 0:
         raise ValueError("n_range does not produce valid sample sizes >= 2.")


    # Calculate effect size once
    effect_size = delta / sd

    # Calculate power for each sample size
    power_values = [
        ttest_power_analysis(
            effect_size=effect_size,
            nobs=n,
            alpha=alpha,
            power=None, # Solve for power
            alternative=alternative,
            ratio=ratio
        )
        for n in n_values
    ]

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(n_values, power_values, 'o-', linewidth=2, markersize=6, label=f'Ratio (n2/n1) = {ratio}')

    # Add reference line for 80% power
    ax.axhline(y=0.8, linestyle='--', color='grey', alpha=0.7, label='Power = 0.8')

    # Labels and Title
    ax.set_xlabel('Sample Size (Group 1, n1)', fontsize=12)
    ax.set_ylabel('Statistical Power', fontsize=12)
    ax.set_title(f'Power Curve: Detecting Mean Difference = {delta}, SD = {sd}', fontsize=14)

    # Grid and Legend
    ax.grid(True, alpha=0.3)
    ax.legend()

    # Set plot limits
    ax.set_xlim(n_values.min(), n_values.max())
    ax.set_ylim(0, 1.05)

    plt.tight_layout()
    return fig

def effect_size_curve(sd: float, n: int, diff_range: Tuple[float, float],
                      alpha: float = 0.05, alternative: str = 'two-sided',
                      n_points: int = 20, ratio: float = 1.0) -> plt.Figure:
    """
    Generate a curve showing how power changes with effect size (mean difference).

    Assumes equal variance (uses pooled sd) consistent with `calculate_power`.

    Parameters:
    -----------
    sd : float
        Pooled standard deviation.
    n : int
        Sample size for the first group (n1).
    diff_range : tuple
        (min_diff, max_diff) range of mean differences to consider.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.
    n_points : int, optional
        Number of points to plot on the curve. Default is 20.
    ratio : float, optional
        Ratio of sample sizes (n2/n1). Default is 1.0.

    Returns:
    --------
    matplotlib.figure.Figure
        Power vs. effect size curve.
    """
    min_diff, max_diff = diff_range

    # Generate mean difference values
    diff_values = np.linspace(min_diff, max_diff, n_points)

    # Calculate power for each mean difference
    power_values = [
        calculate_power(
            delta=diff,
            sd=sd,
            n=n,
            alpha=alpha,
            alternative=alternative,
            ratio=ratio
        )
        for diff in diff_values
    ]

    # Calculate corresponding Cohen's d values for the second x-axis
    d_values = diff_values / sd

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot Power vs. Mean Difference
    line1 = ax1.plot(diff_values, power_values, 'o-', linewidth=2,
                     markersize=6, color='blue', label='Power')
    ax1.set_xlabel('Mean Difference (μA - μB)', fontsize=12)
    ax1.set_ylabel('Statistical Power', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Add reference line for 80% power
    ax1.axhline(y=0.8, linestyle='--', color='grey', alpha=0.7, label='Power = 0.8')

    # Create a second x-axis for Effect Size (Cohen's d)
    ax2 = ax1.twiny() # Share the same y-axis
    ax2.set_xlim(ax1.get_xlim()) # Match x-limits
    # Set ticks and labels for the second x-axis based on d_values
    # Show fewer ticks for clarity if many points
    tick_indices = np.linspace(0, len(diff_values) - 1, num=min(len(diff_values), 6), dtype=int)
    ax2.set_xticks(diff_values[tick_indices])
    ax2.set_xticklabels([f'{d:.2f}' for d in d_values[tick_indices]])
    ax2.set_xlabel("Effect Size (Cohen's d)", fontsize=12)

    # Title and Grid
    ax1.set_title(f'Power vs. Effect Size (n1={n}, Ratio={ratio}, SD={sd})', fontsize=14)
    ax1.grid(True, alpha=0.3)

    # Combine legends from both axes if needed (here only ax1 has labels)
    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc='best')

    # Set plot limits
    ax1.set_ylim(0, 1.05)

    plt.tight_layout()
    return fig


# --- Reporting Function ---

def power_analysis_report(mean_A: float, mean_B: float, sd_A: float, sd_B: float,
                          n_A: int, n_B: Optional[int] = None, alpha: float = 0.05,
                          alternative: str = 'two-sided', target_power: float = 0.8) -> Dict[str, Any]:
    """
    Generate a comprehensive power analysis report for two independent samples.

    Performs Welch's t-test (unequal variances assumed) using scipy.stats.ttest_ind_from_stats.
    Calculates power, required sample size, and minimum detectable difference using
    the Welch approximation functions based on statsmodels (consistent with textbook).

    Parameters:
    -----------
    mean_A, mean_B : float
        Sample means for group A and B.
    sd_A, sd_B : float
        Sample standard deviations for group A and B.
    n_A : int
        Sample size for group A.
    n_B : int, optional
        Sample size for group B. Default is equal to n_A.
    alpha : float, optional
        Significance level. Default is 0.05.
    alternative : str, optional
        Type of test: 'two-sided', 'larger', 'smaller'. Default is 'two-sided'.
    target_power : float, optional
        Target power level for sample size and minimum difference calculations. Default is 0.8.

    Returns:
    --------
    dict
        Comprehensive power analysis report including test results, power,
        sample size analysis, and minimum detectable difference.
    """
    if n_B is None:
        n_B = n_A

    if n_A < 2 or n_B < 2:
        raise ValueError("Sample sizes must be at least 2 for t-test.")
    if sd_A < 0 or sd_B < 0:
        raise ValueError("Standard deviations cannot be negative.")

    mean_diff = mean_A - mean_B
    ratio = n_B / n_A

    # --- 1. Perform Hypothesis Test (Welch's t-test from stats) ---
    # Use ttest_ind_from_stats for Welch's t-test (equal_var=False)
    # Map alternative string for scipy.stats
    if alternative == 'two-sided':
        scipy_alt = 'two-sided'
    elif alternative == 'larger':
        scipy_alt = 'greater'
    elif alternative == 'smaller':
        scipy_alt = 'less'
    else:
         # Should have been caught by ttest_power_analysis, but double-check
         raise ValueError(f"Invalid alternative: {alternative}")

    try:
        t_stat, p_value = ttest_ind_from_stats(
            mean1=mean_A, std1=sd_A, nobs1=n_A,
            mean2=mean_B, std2=sd_B, nobs2=n_B,
            equal_var=False, # Perform Welch's t-test
            alternative=scipy_alt
        )

        # Calculate Welch-Satterthwaite degrees of freedom
        var_A = sd_A**2 / n_A
        var_B = sd_B**2 / n_B
        df_num = (var_A + var_B)**2
        df_den = (var_A**2 / (n_A - 1)) + (var_B**2 / (n_B - 1))
        # Handle potential division by zero if n=1 (though prevented earlier)
        df = df_num / df_den if df_den > 0 else np.inf


        # Determine critical t-value(s)
        if alternative == 'two-sided':
            t_crit_upper = stats.t.ppf(1 - alpha / 2, df)
            t_crit_lower = stats.t.ppf(alpha / 2, df)
            critical_values = (t_crit_lower, t_crit_upper)
            reject = abs(t_stat) > t_crit_upper
        elif alternative == 'larger':
            t_crit = stats.t.ppf(1 - alpha, df)
            critical_values = (t_crit,)
            reject = t_stat > t_crit
        elif alternative == 'smaller':
            t_crit = stats.t.ppf(alpha, df)
            critical_values = (t_crit,)
            reject = t_stat < t_crit

        test_result = {
            'test': f"Welch's Independent Samples t-test ({alternative})",
            'null_hypothesis': "The two population means are equal (H0: μA = μB)",
            'alternative_hypothesis': f"Means are not equal ({alternative})" if alternative=='two-sided' \
                                     else f"Mean A > Mean B ({alternative})" if alternative=='larger' \
                                     else f"Mean A < Mean B ({alternative})",
            't_statistic': t_stat,
            'p_value': p_value,
            'degrees_of_freedom': df,
            'critical_t_values': critical_values,
            'alpha': alpha,
            'reject_null': reject,
            'conclusion': f"{'Reject' if reject else 'Fail to reject'} the null hypothesis at α = {alpha}."
        }

    except Exception as e:
        # Handle potential errors during t-test calculation (e.g., zero variance)
         test_result = {
            'test': f"Welch's Independent Samples t-test ({alternative})",
            'error': f"Could not perform t-test: {e}",
            't_statistic': np.nan, 'p_value': np.nan, 'degrees_of_freedom': np.nan,
            'critical_t_values': np.nan, 'alpha': alpha, 'reject_null': None, 'conclusion': "Test could not be performed."
        }


    # --- 2. Observed Effect and Power ---
    # Calculate Cohen's d using the unpooled SD method for power analysis consistency
    observed_effect_size = cohen_d_unpooled(mean_diff, sd_A, sd_B)
    # Calculate power for the observed difference and sample sizes
    observed_power = calculate_power_welch(
        mean_diff=mean_diff,
        sd_A=sd_A, sd_B=sd_B,
        n_A=n_A, n_B=n_B,
        alpha=alpha, alternative=alternative
    )

    # --- 3. Sample Size Analysis for Target Power ---
    # Calculate required n1 for target power *assuming the observed difference is the true difference*
    required_n1 = calculate_sample_size_welch(
        mean_diff=mean_diff, # Use observed difference as the target delta
        sd_A=sd_A, sd_B=sd_B,
        power=target_power,
        alpha=alpha, alternative=alternative,
        ratio=ratio # Use the current ratio
    )
    # Calculate power achieved with this required sample size (should be close to target_power)
    # Need n2 based on ratio
    required_n2 = int(np.ceil(required_n1 * ratio))
    actual_power_at_required_n = calculate_power_welch(
         mean_diff=mean_diff,
         sd_A=sd_A, sd_B=sd_B,
         n_A=required_n1, n_B=required_n2, # Use calculated required Ns
         alpha=alpha, alternative=alternative
    )


    # --- 4. Minimum Detectable Difference for Target Power ---
    # Calculate the minimum difference detectable with current sample sizes and target power
    min_diff = calculate_detectable_difference_welch(
        sd_A=sd_A, sd_B=sd_B,
        n_A=n_A, n_B=n_B, # Use current Ns
        power=target_power,
        alpha=alpha, alternative=alternative
    )
    # Calculate corresponding minimum effect size
    min_effect_size = cohen_d_unpooled(min_diff, sd_A, sd_B)

    # --- Assemble Report ---
    report = {
        'inputs': {
            'mean_A': mean_A, 'sd_A': sd_A, 'n_A': n_A,
            'mean_B': mean_B, 'sd_B': sd_B, 'n_B': n_B,
            'alpha': alpha, 'alternative': alternative, 'target_power': target_power
        },
        'test_results': test_result,
        'observed_effect': {
            'mean_difference': mean_diff,
            'effect_size_cohen_d': observed_effect_size,
            'power_for_observed_effect': observed_power
        },
        'sample_size_analysis': {
            'target_power': target_power,
            'required_n1_for_target_power': required_n1,
             # Also report n2 based on ratio
            'required_n2_for_target_power': required_n2,
            'power_at_required_n': actual_power_at_required_n,
            'assumed_delta': mean_diff, # Clarify assumption
            'assumed_sds': (sd_A, sd_B)
        },
        'minimum_detectable_difference': {
            'target_power': target_power,
            'min_detectable_diff': min_diff,
            'min_detectable_effect_size': min_effect_size,
            'current_n1': n_A,
            'current_n2': n_B
        }
    }

    return report

def print_power_report(report: Dict[str, Any]) -> None:
    """
    Print a formatted power analysis report generated by power_analysis_report().

    Parameters:
    -----------
    report : dict
        Power analysis report dictionary.
    """
    inputs = report['inputs']
    test = report['test_results']
    obs = report['observed_effect']
    sample = report['sample_size_analysis']
    min_det = report['minimum_detectable_difference']

    print("=======================================")
    print("    POWER ANALYSIS REPORT (T-TEST)     ")
    print("=======================================")

    print("\n--- INPUTS ---")
    print(f"Group A: Mean={inputs['mean_A']}, SD={inputs['sd_A']}, N={inputs['n_A']}")
    print(f"Group B: Mean={inputs['mean_B']}, SD={inputs['sd_B']}, N={inputs['n_B']}")
    print(f"Alpha: {inputs['alpha']}, Alternative: {inputs['alternative']}, Target Power: {inputs['target_power']}")

    print("\n--- HYPOTHESIS TEST RESULTS ---")
    print(f"Test Performed: {test.get('test', 'N/A')}")
    if 'error' in test:
        print(f"Error: {test['error']}")
    else:
        print(f"Null Hypothesis: {test.get('null_hypothesis', 'N/A')}")
        print(f"Alternative Hypothesis: {test.get('alternative_hypothesis', 'N/A')}")
        print(f"t-statistic: {test.get('t_statistic', np.nan):.4f}")
        print(f"Degrees of Freedom: {test.get('degrees_of_freedom', np.nan):.4f}")
        print(f"P-value: {test.get('p_value', np.nan):.4f}")
        # Format critical values nicely
        crits = test.get('critical_t_values', [])
        crit_str = ", ".join([f"{c:.4f}" for c in crits]) if isinstance(crits, tuple) or isinstance(crits, list) else f"{crits:.4f}"
        print(f"Critical t-value(s) at α={test.get('alpha', np.nan)}: {crit_str}")
        print(f"Conclusion: {test.get('conclusion', 'N/A')}")

    print("\n--- OBSERVED EFFECT & POWER ---")
    print(f"Observed Mean Difference (A - B): {obs.get('mean_difference', np.nan):.4f}")
    print(f"Observed Effect Size (Cohen's d): {obs.get('effect_size_cohen_d', np.nan):.4f}")
    print(f"Statistical Power for Observed Effect: {obs.get('power_for_observed_effect', np.nan):.4f}")

    print(f"\n--- SAMPLE SIZE FOR TARGET POWER ({sample.get('target_power', np.nan):.0%}) ---")
    print(f"  (Assuming true difference = {sample.get('assumed_delta', np.nan):.4f} and SDs = {sample.get('assumed_sds', (np.nan, np.nan))})")
    print(f"Required Sample Size (N1): {sample.get('required_n1_for_target_power', 'N/A')}")
    print(f"Required Sample Size (N2): {sample.get('required_n2_for_target_power', 'N/A')} (based on input ratio)")
    print(f"Actual Power with Required N: {sample.get('power_at_required_n', np.nan):.4f}")

    print(f"\n--- MINIMUM DETECTABLE DIFFERENCE (at {min_det.get('target_power', np.nan):.0%} Power) ---")
    print(f"  (With current sample sizes N1={min_det.get('current_n1', 'N/A')}, N2={min_det.get('current_n2', 'N/A')})")
    print(f"Minimum Detectable Mean Difference: {min_det.get('min_detectable_diff', np.nan):.4f}")
    print(f"Minimum Detectable Effect Size (d): {min_det.get('min_detectable_effect_size', np.nan):.4f}")

    print("\n--- INTERPRETATION GUIDELINES ---")
    print("Effect Size (Cohen's d):  Small ≈ 0.2 | Medium ≈ 0.5 | Large ≈ 0.8")
    print("Power: Conventional target is ≥ 0.8 (80%). Lower power increases risk of Type II error (false negative).")

    # Add a summary interpretation
    print("\n--- SUMMARY INTERPRETATION ---")
    es = obs.get('effect_size_cohen_d', np.nan)
    power = obs.get('power_for_observed_effect', np.nan)

    if not np.isnan(es):
        size_interp = "small" if abs(es) < 0.35 else "medium" if abs(es) < 0.65 else "large" # Adjusted thresholds slightly
        print(f"The observed effect size ({es:.2f}) is considered {size_interp}.")
    else:
        print("Could not calculate observed effect size.")

    if not np.isnan(power):
        power_interp = "very low (<50%)" if power < 0.5 else "low (50-79%)" if power < 0.8 else "adequate (≥80%)"
        print(f"The statistical power for this effect size with the current sample ({power:.2f}) is {power_interp}.")
        if power < sample.get('target_power', 0.8) and not np.isnan(sample.get('required_n1_for_target_power', np.nan)):
             print(f"  -> To achieve {sample.get('target_power', 0.8):.0%} power for the observed effect,")
             print(f"     sample sizes of N1≈{sample.get('required_n1_for_target_power', 'N/A')}, N2≈{sample.get('required_n2_for_target_power', 'N/A')} would be needed.")
        elif power >= sample.get('target_power', 0.8):
             print("  -> The current sample size provides adequate power for the observed effect.")
    else:
         print("Could not calculate statistical power.")

    if not np.isnan(min_det.get('min_detectable_diff', np.nan)):
        print(f"With the current sample size, the study has {min_det.get('target_power', np.nan):.0%} power to detect a minimum difference of {min_det.get('min_detectable_diff', np.nan):.4f} (Effect Size d≈{min_det.get('min_detectable_effect_size', np.nan):.2f}).")
    else:
        print("Could not calculate minimum detectable difference.")

    print("=======================================")

# Example Usage (Optional - can be commented out)
if __name__ == '__main__':
    print("--- Example 1: Basic Power Calculation ---")
    # Parameters from a hypothetical study
    mean_treatment = 105
    mean_control = 100
    sd_pooled = 10 # Assume equal SD for this example
    n_per_group = 50
    delta_observed = mean_treatment - mean_control

    power = calculate_power(delta=delta_observed, sd=sd_pooled, n=n_per_group, alpha=0.05, alternative='two-sided')
    print(f"Calculated Power: {power:.4f}")

    print("\n--- Example 2: Sample Size Calculation ---")
    # Find N needed for 80% power to detect the same difference
    required_n = calculate_sample_size(delta=delta_observed, sd=sd_pooled, power=0.8, alpha=0.05, alternative='two-sided')
    print(f"Required N per group (for 80% power): {required_n}")

    print("\n--- Example 3: Welch's Power Calculation (Unequal SDs) ---")
    sd_treatment = 12
    sd_control = 8
    power_welch = calculate_power_welch(mean_diff=delta_observed, sd_A=sd_treatment, sd_B=sd_control, n_A=n_per_group, n_B=n_per_group)
    print(f"Calculated Power (Welch approx.): {power_welch:.4f}")

    print("\n--- Example 4: Full Power Analysis Report ---")
    report = power_analysis_report(
        mean_A=mean_treatment, mean_B=mean_control,
        sd_A=sd_treatment, sd_B=sd_control,
        n_A=n_per_group, n_B=n_per_group, # Use unequal SDs here
        alpha=0.05, alternative='two-sided', target_power=0.8
    )
    print_power_report(report)

    print("\n--- Example 5: Power Curve ---")
    try:
        fig_power = power_curve(delta=5, sd=10, n_range=(10, 150), alpha=0.05, alternative='two-sided')
        # In a real application, you might save or display the figure:
        # fig_power.savefig("power_curve.png")
        # plt.show() # Uncomment to display plot if running locally
        print("Power curve generated (figure object returned).")
        plt.close(fig_power) # Close the plot window automatically
    except Exception as e:
        print(f"Could not generate power curve: {e}")


    print("\n--- Example 6: Effect Size Curve ---")
    try:
        fig_effect = effect_size_curve(sd=10, n=50, diff_range=(1, 10), alpha=0.05, alternative='two-sided')
        # fig_effect.savefig("effect_size_curve.png")
        # plt.show()
        print("Effect size curve generated (figure object returned).")
        plt.close(fig_effect)
    except Exception as e:
        print(f"Could not generate effect size curve: {e}")
