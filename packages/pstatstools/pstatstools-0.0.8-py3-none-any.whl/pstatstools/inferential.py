import numpy as np
import scipy.stats as stats
from scipy.stats import ttest_ind_from_stats
import statsmodels.stats.power as smp
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Union, Optional, Any, Callable

def ttest_power_analysis(effect_size: float, nobs: int = None, alpha: float = 0.05,
                         power: float = None, ratio: float = 1.0,
                         alternative: str = 'two-sided') -> float:
    valid_alternatives = ['two-sided', 'larger', 'smaller']
    if alternative not in valid_alternatives:
        if alternative in ['two', '2-sided']:
             alternative = 'two-sided'
        elif alternative in ['right', 'greater']:
             alternative = 'larger'
        elif alternative in ['left', 'less']:
             alternative = 'smaller'
        else:
            raise ValueError(f"Invalid alternative: {alternative}. Choose from {valid_alternatives}")

    result = smp.TTestIndPower().solve_power(
        effect_size=effect_size,
        nobs1=nobs,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative=alternative
    )

    return result

def calculate_power(delta: float, sd: float, n: int, alpha: float = 0.05,
                    alternative: str = 'two-sided', ratio: float = 1.0) -> float:
    effect_size = delta / sd
    power = ttest_power_analysis(
        effect_size=effect_size,
        nobs=n,
        alpha=alpha,
        power=None,
        alternative=alternative,
        ratio=ratio
    )
    return power

def calculate_sample_size(delta: float, sd: float, power: float = 0.8,
                          alpha: float = 0.05, alternative: str = 'two-sided',
                          ratio: float = 1.0) -> int:
    effect_size = delta / sd
    n = ttest_power_analysis(
        effect_size=effect_size,
        nobs=None,
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )
    return int(np.ceil(n))

def calculate_detectable_difference(sd: float, n: int, power: float = 0.8,
                                    alpha: float = 0.05, alternative: str = 'two-sided',
                                    ratio: float = 1.0) -> float:
    effect_size = ttest_power_analysis(
        effect_size=None,
        nobs=n,
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )
    return effect_size * sd

def cohen_d_unpooled(mean_diff: float, sd_A: float, sd_B: float) -> float:
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    if pooled_sd == 0:
        return 0
    d = mean_diff / pooled_sd
    return d

def calculate_power_welch(mean_diff: float, sd_A: float, sd_B: float,
                          n_A: int, n_B: Optional[int] = None,
                          alpha: float = 0.05, alternative: str = "two-sided") -> float:
    if n_B is None:
        n_B = n_A

    effect_size = cohen_d_unpooled(mean_diff, sd_A, sd_B)
    ratio = n_B / n_A
    power = ttest_power_analysis(
        effect_size=effect_size,
        nobs=n_A,
        alpha=alpha,
        power=None,
        alternative=alternative,
        ratio=ratio
    )
    return power

def calculate_sample_size_welch(mean_diff: float, sd_A: float, sd_B: float,
                                power: float = 0.8, alpha: float = 0.05,
                                alternative: str = 'two-sided', ratio: float = 1.0) -> int:
    effect_size = cohen_d_unpooled(mean_diff, sd_A, sd_B)
    n = ttest_power_analysis(
        effect_size=effect_size,
        nobs=None,
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )
    return int(np.ceil(n))

def calculate_detectable_difference_welch(sd_A: float, sd_B: float, n_A: int,
                                          n_B: Optional[int] = None, power: float = 0.8,
                                          alpha: float = 0.05, alternative: str = 'two-sided') -> float:
    if n_B is None:
        n_B = n_A

    ratio = n_B / n_A
    effect_size = ttest_power_analysis(
        effect_size=None,
        nobs=n_A,
        alpha=alpha,
        power=power,
        alternative=alternative,
        ratio=ratio
    )
    pooled_sd = np.sqrt((sd_A**2 + sd_B**2) / 2)
    return effect_size * pooled_sd

def visualize_results(report: Dict[str, Any]) -> plt.Figure:
    """
    Create a comprehensive visualization of t-test results with confidence intervals.
    
    Parameters:
    -----------
    report : dict
        Power analysis report dictionary from power_analysis_report().
        
    Returns:
    --------
    matplotlib.figure.Figure
        Figure with visualized results.
    """
    inputs = report['inputs']
    test = report['test_results']
    obs = report['observed_effect']
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(12, 10))
    
    # Define a grid layout
    gs = plt.GridSpec(3, 2, figure=fig, height_ratios=[1, 1, 1.2])
    
    # 1. Mean difference with confidence interval
    ax1 = fig.add_subplot(gs[0, :])
    
    # Extract data
    mean_diff = obs['mean_difference']
    ci = test.get('confidence_interval', (np.nan, np.nan))
    
    # Plot means and CIs for each group
    group_means = [inputs['mean_A'], inputs['mean_B']]
    group_cis = [inputs['ci_A'], inputs['ci_B']]
    group_labels = ['Group A', 'Group B']
    
    # For the main mean comparison
    ax1.errorbar([0, 1], group_means, 
                yerr=[[m-ci[0] for m, ci in zip(group_means, group_cis)], 
                      [ci[1]-m for m, ci in zip(group_means, group_cis)]],
                fmt='o', capsize=10, markersize=10, 
                color=['#1f77b4', '#ff7f0e'], ecolor=['#1f77b4', '#ff7f0e'],
                label=['Group A', 'Group B'])
    
    # Add a horizontal line connecting the means
    ax1.plot([0, 1], group_means, 'k--', alpha=0.3)
    
    # Add mean values as text
    for i, (mean, ci_pair) in enumerate(zip(group_means, group_cis)):
        ax1.annotate(f"{mean:.2f}\n({ci_pair[0]:.2f}, {ci_pair[1]:.2f})", 
                    xy=(i, mean), xytext=(i, mean + 0.05 * (max(group_means) - min(group_means))),
                    ha='center', va='bottom')
    
    # Customize the plot
    ax1.set_title('Group Means with Confidence Intervals', fontsize=14)
    ax1.set_ylabel('Value', fontsize=12)
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels(group_labels)
    ax1.grid(True, alpha=0.3)
    
    # 2. Difference with CI and p-value indication
    ax2 = fig.add_subplot(gs[1, 0])
    
    # Draw zero line for reference
    ax2.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    
    # Plot mean difference with CI
    ax2.errorbar(0.5, mean_diff, 
                yerr=[[mean_diff - ci[0]], [ci[1] - mean_diff]],
                fmt='o', capsize=10, markersize=10, color='purple')
    
    # Annotate with values
    ax2.annotate(f"Difference: {mean_diff:.2f}\n{int(inputs['confidence_level']*100)}% CI: ({ci[0]:.2f}, {ci[1]:.2f})",
                xy=(0.5, mean_diff), xytext=(0.5, mean_diff + (ci[1] - ci[0])/2),
                ha='center', va='bottom')
    
    # Add p-value and significance information
    is_significant = test.get('reject_null', False)
    p_value = test.get('p_value', np.nan)
    
    if not np.isnan(p_value):
        sig_text = f"p = {p_value:.4f}\n({'Significant' if is_significant else 'Not significant'} at α = {inputs['alpha']})"
        ax2.annotate(sig_text, xy=(0.5, 0), xytext=(0.5, -0.2 * (ci[1] - ci[0])),
                    ha='center', va='top', color='red' if is_significant else 'black')
    
    # Customize the plot
    ax2.set_title('Mean Difference with Confidence Interval', fontsize=14)
    ax2.set_ylabel('Difference (A - B)', fontsize=12)
    ax2.set_xticks([])
    ax2.set_xlim(0, 1)
    ax2.grid(True, alpha=0.3)
    
    # 3. Effect size visualization
    ax3 = fig.add_subplot(gs[1, 1])
    
    effect_size = obs['effect_size_cohen_d']
    
    # Create a horizontal bar for the effect size
    ax3.barh(0, effect_size, height=0.4, color='purple', alpha=0.7)
    
    # Add reference lines and regions for Cohen's d interpretation
    ax3.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax3.axvline(x=0.2, color='k', linestyle='--', alpha=0.2)
    ax3.axvline(x=0.5, color='k', linestyle='--', alpha=0.2)
    ax3.axvline(x=0.8, color='k', linestyle='--', alpha=0.2)
    
    # Shade regions for different effect size interpretations
    ax3.axvspan(0, 0.2, alpha=0.1, color='green')
    ax3.axvspan(0.2, 0.5, alpha=0.1, color='blue')
    ax3.axvspan(0.5, 0.8, alpha=0.1, color='orange')
    ax3.axvspan(0.8, max(1.5, effect_size * 1.2), alpha=0.1, color='red')
    
    # Add annotations for effect size regions
    ax3.text(0.1, 0.5, 'Small', ha='center', va='center', transform=ax3.get_xaxis_transform())
    ax3.text(0.35, 0.5, 'Medium', ha='center', va='center', transform=ax3.get_xaxis_transform())
    ax3.text(0.65, 0.5, 'Large', ha='center', va='center', transform=ax3.get_xaxis_transform())
    ax3.text(min(1.2, max(1.0, effect_size)), 0.5, 'Very Large', ha='center', va='center', 
             transform=ax3.get_xaxis_transform())
    
    # Add the effect size value
    ax3.annotate(f"d = {effect_size:.2f}", xy=(effect_size, 0), 
                xytext=(effect_size, 0.2), ha='center', va='bottom')
    
    # Customize the plot
    ax3.set_title("Effect Size (Cohen's d)", fontsize=14)
    ax3.set_yticks([])
    ax3.set_xlim(-0.2, max(1.2, effect_size * 1.2))
    ax3.grid(True, alpha=0.3, axis='x')
    
    # 4. Power analysis visualization
    ax4 = fig.add_subplot(gs[2, :])
    
    # Calculate a power curve around the current sample size
    sample = report['sample_size_analysis']
    min_det = report['minimum_detectable_difference']
    n_A = inputs['n_A']
    n_values = np.linspace(max(2, n_A * 0.2), n_A * 2.5, 30)
    n_values = np.round(n_values).astype(int)
    
    # Calculate power for each sample size
    power_values = []
    for n in n_values:
        power = calculate_power_welch(
            mean_diff=mean_diff,
            sd_A=inputs['sd_A'], sd_B=inputs['sd_B'],
            n_A=n, n_B=int(n * inputs['n_B'] / inputs['n_A']),
            alpha=inputs['alpha'], alternative=inputs['alternative']
        )
        power_values.append(power)
    
    # Plot the power curve
    ax4.plot(n_values, power_values, 'o-', linewidth=2, markersize=6, color='blue', label='Power Curve')
    
    # Add reference line for target power
    target_power = sample['target_power']
    ax4.axhline(y=target_power, linestyle='--', color='r', alpha=0.7, label=f'Target Power ({target_power:.0%})')
    
    # Add reference line for current sample and power
    current_power = obs['power_for_observed_effect']
    ax4.axhline(y=current_power, linestyle=':', color='green', alpha=0.7, label=f'Current Power ({current_power:.2f})')
    ax4.axvline(x=n_A, linestyle=':', color='green', alpha=0.7)
    
    # Mark the required sample size for target power
    req_n1 = sample['required_n1_for_target_power']
    ax4.plot(req_n1, target_power, 'X', markersize=12, color='red', 
             label=f'Required N₁ = {req_n1} for {target_power:.0%} power')
    
    # Add annotations
    ax4.annotate(f"Current: N₁ = {n_A}, Power = {current_power:.2f}",
                xy=(n_A, current_power), xytext=(n_A * 1.1, current_power * 0.93),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))
    
    # Customize the plot
    ax4.set_title('Power Analysis: Sample Size vs. Power', fontsize=14)
    ax4.set_xlabel('Sample Size (Group 1, N₁)', fontsize=12)
    ax4.set_ylabel('Statistical Power', fontsize=12)
    ax4.grid(True, alpha=0.3)
    ax4.legend(loc='lower right')
    ax4.set_ylim(0, 1.05)
    
    # Add an explanation of the minimum detectable difference
    min_diff = min_det['min_detectable_diff']
    min_effect = min_det['min_detectable_effect_size']
    
    ax4.annotate(f"With current sample size (N₁={n_A}, N₂={inputs['n_B']}),\n"
                f"minimum detectable difference at {target_power:.0%} power: {min_diff:.2f} (d = {min_effect:.2f})",
                xy=(0.98, 0.02), xycoords='axes fraction', ha='right', va='bottom',
                bbox=dict(boxstyle="round,pad=0.3", fc="lightyellow", alpha=0.8))
    
    # Adjust layout
    plt.tight_layout()
    return fig

def power_curve(delta: float, sd: float, n_range: Tuple[int, int],
                alpha: float = 0.05, alternative: str = 'two-sided',
                n_points: int = 20, ratio: float = 1.0) -> plt.Figure:
    min_n, max_n = n_range
    min_n = max(2, min_n)
    if max_n < min_n:
        max_n = min_n + n_points
    
    n_values = np.linspace(min_n, max_n, n_points)
    n_values = np.round(n_values).astype(int)
    n_values = np.unique(n_values)
    n_values = n_values[n_values >= 2]
    if len(n_values) == 0:
         raise ValueError("n_range does not produce valid sample sizes >= 2.")

    effect_size = delta / sd
    power_values = [
        ttest_power_analysis(
            effect_size=effect_size,
            nobs=n,
            alpha=alpha,
            power=None,
            alternative=alternative,
            ratio=ratio
        )
        for n in n_values
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(n_values, power_values, 'o-', linewidth=2, markersize=6, label=f'Ratio (n2/n1) = {ratio}')
    ax.axhline(y=0.8, linestyle='--', color='grey', alpha=0.7, label='Power = 0.8')
    ax.set_xlabel('Sample Size (Group 1, n1)', fontsize=12)
    ax.set_ylabel('Statistical Power', fontsize=12)
    ax.set_title(f'Power Curve: Detecting Mean Difference = {delta}, SD = {sd}', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend()
    ax.set_xlim(n_values.min(), n_values.max())
    ax.set_ylim(0, 1.05)
    plt.tight_layout()
    return fig

def effect_size_curve(sd: float, n: int, diff_range: Tuple[float, float],
                      alpha: float = 0.05, alternative: str = 'two-sided',
                      n_points: int = 20, ratio: float = 1.0) -> plt.Figure:
    min_diff, max_diff = diff_range
    diff_values = np.linspace(min_diff, max_diff, n_points)
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
    
    d_values = diff_values / sd
    fig, ax1 = plt.subplots(figsize=(10, 6))
    line1 = ax1.plot(diff_values, power_values, 'o-', linewidth=2,
                     markersize=6, color='blue', label='Power')
    ax1.set_xlabel('Mean Difference (μA - μB)', fontsize=12)
    ax1.set_ylabel('Statistical Power', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.axhline(y=0.8, linestyle='--', color='grey', alpha=0.7, label='Power = 0.8')
    
    ax2 = ax1.twiny()
    ax2.set_xlim(ax1.get_xlim())
    tick_indices = np.linspace(0, len(diff_values) - 1, num=min(len(diff_values), 6), dtype=int)
    ax2.set_xticks(diff_values[tick_indices])
    ax2.set_xticklabels([f'{d:.2f}' for d in d_values[tick_indices]])
    ax2.set_xlabel("Effect Size (Cohen's d)", fontsize=12)
    
    ax1.set_title(f'Power vs. Effect Size (n1={n}, Ratio={ratio}, SD={sd})', fontsize=14)
    ax1.grid(True, alpha=0.3)
    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc='best')
    ax1.set_ylim(0, 1.05)
    plt.tight_layout()
    return fig

def calculate_confidence_interval(mean: float, sd: float, n: int, 
                                 conf_level: float = 0.95) -> Tuple[float, float]:
    """
    Calculate confidence interval for a mean.
    
    Parameters:
    -----------
    mean : float
        Sample mean
    sd : float
        Sample standard deviation
    n : int
        Sample size
    conf_level : float, optional
        Confidence level (default: 0.95 for 95% CI)
        
    Returns:
    --------
    Tuple[float, float]
        Lower and upper bounds of the confidence interval
    """
    # Standard error of the mean
    sem = sd / np.sqrt(n)
    
    # Critical t-value
    alpha = 1 - conf_level
    df = n - 1
    t_crit = stats.t.ppf(1 - alpha/2, df)
    
    # Calculate margin of error
    margin_of_error = t_crit * sem
    
    # Calculate confidence interval
    lower = mean - margin_of_error
    upper = mean + margin_of_error
    
    return (lower, upper)

def power_analysis_report(mean_A: float, mean_B: float, sd_A: float, sd_B: float,
                          n_A: int, n_B: Optional[int] = None, alpha: float = 0.05,
                          alternative: str = 'two-sided', target_power: float = 0.8,
                          conf_level: float = 0.95) -> Dict[str, Any]:
    if n_B is None:
        n_B = n_A

    if n_A < 2 or n_B < 2:
        raise ValueError("Sample sizes must be at least 2 for t-test.")
    if sd_A < 0 or sd_B < 0:
        raise ValueError("Standard deviations cannot be negative.")

    mean_diff = mean_A - mean_B
    ratio = n_B / n_A

    # Map alternative string for scipy.stats
    if alternative == 'two-sided':
        scipy_alt = 'two-sided'
    elif alternative == 'larger':
        scipy_alt = 'greater'
    elif alternative == 'smaller':
        scipy_alt = 'less'
    else:
        raise ValueError(f"Invalid alternative: {alternative}")

    try:
        t_stat, p_value = ttest_ind_from_stats(
            mean1=mean_A, std1=sd_A, nobs1=n_A,
            mean2=mean_B, std2=sd_B, nobs2=n_B,
            equal_var=False,
            alternative=scipy_alt
        )

        # Calculate Welch-Satterthwaite degrees of freedom
        var_A = sd_A**2 / n_A
        var_B = sd_B**2 / n_B
        df_num = (var_A + var_B)**2
        df_den = (var_A**2 / (n_A - 1)) + (var_B**2 / (n_B - 1))
        df = df_num / df_den if df_den > 0 else np.inf

        # Calculate confidence interval for the difference in means
        # For Welch's t-test, we use the Welch-Satterthwaite df
        sem_diff = np.sqrt(var_A + var_B)
        alpha_ci = 1 - conf_level
        t_crit = stats.t.ppf(1 - alpha_ci/2, df)
        margin_of_error = t_crit * sem_diff
        ci_lower = mean_diff - margin_of_error
        ci_upper = mean_diff + margin_of_error

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
            'confidence_interval': (ci_lower, ci_upper),
            'confidence_level': conf_level,
            'conclusion': f"{'Reject' if reject else 'Fail to reject'} the null hypothesis at α = {alpha}."
        }

    except Exception as e:
        test_result = {
            'test': f"Welch's Independent Samples t-test ({alternative})",
            'error': f"Could not perform t-test: {e}",
            't_statistic': np.nan, 'p_value': np.nan, 'degrees_of_freedom': np.nan,
            'critical_t_values': np.nan, 'alpha': alpha, 'reject_null': None, 
            'confidence_interval': (np.nan, np.nan),
            'confidence_level': conf_level,
            'conclusion': "Test could not be performed."
        }

    # Calculate confidence intervals for each group mean
    ci_A = calculate_confidence_interval(mean_A, sd_A, n_A, conf_level)
    ci_B = calculate_confidence_interval(mean_B, sd_B, n_B, conf_level)

    # Calculate observed effect and power
    observed_effect_size = cohen_d_unpooled(mean_diff, sd_A, sd_B)
    observed_power = calculate_power_welch(
        mean_diff=mean_diff,
        sd_A=sd_A, sd_B=sd_B,
        n_A=n_A, n_B=n_B,
        alpha=alpha, alternative=alternative
    )

    # Sample size analysis for target power
    required_n1 = calculate_sample_size_welch(
        mean_diff=mean_diff,
        sd_A=sd_A, sd_B=sd_B,
        power=target_power,
        alpha=alpha, alternative=alternative,
        ratio=ratio
    )
    required_n2 = int(np.ceil(required_n1 * ratio))
    actual_power_at_required_n = calculate_power_welch(
         mean_diff=mean_diff,
         sd_A=sd_A, sd_B=sd_B,
         n_A=required_n1, n_B=required_n2,
         alpha=alpha, alternative=alternative
    )

    # Minimum detectable difference
    min_diff = calculate_detectable_difference_welch(
        sd_A=sd_A, sd_B=sd_B,
        n_A=n_A, n_B=n_B,
        power=target_power,
        alpha=alpha, alternative=alternative
    )
    min_effect_size = cohen_d_unpooled(min_diff, sd_A, sd_B)

    report = {
        'inputs': {
            'mean_A': mean_A, 'sd_A': sd_A, 'n_A': n_A, 'ci_A': ci_A,
            'mean_B': mean_B, 'sd_B': sd_B, 'n_B': n_B, 'ci_B': ci_B,
            'alpha': alpha, 'alternative': alternative, 
            'target_power': target_power, 'confidence_level': conf_level
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
            'required_n2_for_target_power': required_n2,
            'power_at_required_n': actual_power_at_required_n,
            'assumed_delta': mean_diff,
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

def print_power_report(report: Dict[str, Any], round_to: int = 4) -> None:
    """
    Print a formatted power analysis report generated by power_analysis_report().
    
    Parameters:
    -----------
    report : dict
        Power analysis report dictionary.
    round_to : int, optional
        Number of decimal places to round to. Default is 4.
    """
    # First, check if running in IPython/Jupyter environment
    in_notebook = False
    try:
        from IPython import get_ipython
        if get_ipython() is not None:
            # More robust check for notebook/qtconsole vs terminal ipython
            if 'zmqshell' in str(type(get_ipython())).lower():
                in_notebook = True
    except (ImportError, NameError):
        pass
        
    inputs = report['inputs']
    test = report['test_results']
    obs = report['observed_effect']
    sample = report['sample_size_analysis']
    min_det = report['minimum_detectable_difference']
    
    # Format for values
    float_formatter = f"{{:.{round_to}f}}".format
    
    if in_notebook:
        try:
            from IPython.display import display, HTML
            
            # Create a nicely formatted HTML report
            html = f"""
            <div style="max-width: 800px; margin: 0 auto;">
                <h2 style="text-align: center; margin-bottom: 30px;">T-Test Power Analysis Report</h2>
                
                <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 30px;">
                    <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <h3 style="margin-top: 0;">Group A</h3>
                        <p><strong>Mean:</strong> {float_formatter(inputs['mean_A'])}</p>
                        <p><strong>SD:</strong> {float_formatter(inputs['sd_A'])}</p>
                        <p><strong>N:</strong> {inputs['n_A']}</p>
                        <p><strong>{int(inputs['confidence_level']*100)}% CI:</strong> ({float_formatter(inputs['ci_A'][0])}, {float_formatter(inputs['ci_A'][1])})</p>
                    </div>
                    <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 15px; border-radius: 5px;">
                        <h3 style="margin-top: 0;">Group B</h3>
                        <p><strong>Mean:</strong> {float_formatter(inputs['mean_B'])}</p>
                        <p><strong>SD:</strong> {float_formatter(inputs['sd_B'])}</p>
                        <p><strong>N:</strong> {inputs['n_B']}</p>
                        <p><strong>{int(inputs['confidence_level']*100)}% CI:</strong> ({float_formatter(inputs['ci_B'][0])}, {float_formatter(inputs['ci_B'][1])})</p>
                    </div>
                </div>
                
                <h3>Test Results</h3>
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                    <p><strong>Test:</strong> {test.get('test', 'N/A')}</p>
            """
            
            if 'error' in test:
                html += f"<p><strong>Error:</strong> {test['error']}</p>"
            else:
                html += f"""
                    <p><strong>Null Hypothesis:</strong> {test.get('null_hypothesis', 'N/A')}</p>
                    <p><strong>Alternative:</strong> {test.get('alternative_hypothesis', 'N/A')}</p>
                    <p><strong>t-statistic:</strong> {float_formatter(test.get('t_statistic', np.nan))}</p>
                    <p><strong>Degrees of Freedom:</strong> {float_formatter(test.get('degrees_of_freedom', np.nan))}</p>
                    <p><strong>p-value:</strong> {float_formatter(test.get('p_value', np.nan))}</p>
                """
                
                # Format critical values nicely
                crits = test.get('critical_t_values', [])
                crit_str = ", ".join([f"{c:.{round_to}f}" for c in crits]) if isinstance(crits, tuple) or isinstance(crits, list) else f"{crits:.{round_to}f}"
                
                html += f"""
                    <p><strong>Critical t-value(s) at α={test.get('alpha', np.nan)}:</strong> {crit_str}</p>
                    <p><strong>Mean Difference (A-B):</strong> {float_formatter(obs.get('mean_difference', np.nan))}</p>
                    <p><strong>{int(inputs['confidence_level']*100)}% CI for Difference:</strong> ({float_formatter(test.get('confidence_interval', (np.nan, np.nan))[0])}, {float_formatter(test.get('confidence_interval', (np.nan, np.nan))[1])})</p>
                    <p><strong>Conclusion:</strong> {test.get('conclusion', 'N/A')}</p>
                """
            
            html += """
                </div>
                
                <div style="display: flex; flex-wrap: wrap; gap: 20px;">
            """
            
            # Effect and Power section
            html += f"""
                    <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                        <h3 style="margin-top: 0;">Observed Effect & Power</h3>
                        <p><strong>Mean Difference (A-B):</strong> {float_formatter(obs.get('mean_difference', np.nan))}</p>
                        <p><strong>Effect Size (Cohen's d):</strong> {float_formatter(obs.get('effect_size_cohen_d', np.nan))}</p>
                        <p><strong>Power:</strong> {float_formatter(obs.get('power_for_observed_effect', np.nan))}</p>
                    </div>
            """
            
            # Sample Size Analysis
            html += f"""
                    <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                        <h3 style="margin-top: 0;">Sample Size for {int(sample.get('target_power', 0.8)*100)}% Power</h3>
                        <p><small><em>(Assuming true difference = {float_formatter(sample.get('assumed_delta', np.nan))})</em></small></p>
                        <p><strong>Required N₁:</strong> {sample.get('required_n1_for_target_power', 'N/A')}</p>
                        <p><strong>Required N₂:</strong> {sample.get('required_n2_for_target_power', 'N/A')}</p>
                        <p><strong>Power with these sample sizes:</strong> {float_formatter(sample.get('power_at_required_n', np.nan))}</p>
                    </div>
                    
                    <div style="flex: 1; min-width: 300px; background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                        <h3 style="margin-top: 0;">Minimum Detectable Difference</h3>
                        <p><small><em>(At {int(min_det.get('target_power', 0.8)*100)}% power with current sample sizes)</em></small></p>
                        <p><strong>Min. Detectable Difference:</strong> {float_formatter(min_det.get('min_detectable_diff', np.nan))}</p>
                        <p><strong>Min. Effect Size (d):</strong> {float_formatter(min_det.get('min_detectable_effect_size', np.nan))}</p>
                    </div>
            """
            
            html += """
                </div>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px;">
                    <h3 style="margin-top: 0;">Interpretation Guidelines</h3>
                    <ul>
                        <li><strong>Effect Size (Cohen's d):</strong> Small ≈ 0.2 | Medium ≈ 0.5 | Large ≈ 0.8</li>
                        <li><strong>Power:</strong> Conventional target is ≥ 0.8 (80%). Lower values increase Type II error risk.</li>
                        <li><strong>p-value:</strong> If < α (typically 0.05), we reject the null hypothesis.</li>
                    </ul>
            """
            
            # Add summary interpretation
            es = obs.get('effect_size_cohen_d', np.nan)
            power = obs.get('power_for_observed_effect', np.nan)
            
            html += "<h3>Summary Interpretation</h3><ul>"
            
            if not np.isnan(es):
                size_interp = "small" if abs(es) < 0.35 else "medium" if abs(es) < 0.65 else "large"
                html += f"<li>The observed effect size ({float_formatter(es)}) is considered {size_interp}.</li>"
            
            if not np.isnan(power):
                power_interp = "very low (<50%)" if power < 0.5 else "low (50-79%)" if power < 0.8 else "adequate (≥80%)"
                html += f"<li>The statistical power ({float_formatter(power)}) is {power_interp}.</li>"
                
                if power < sample.get('target_power', 0.8) and not np.isnan(sample.get('required_n1_for_target_power', np.nan)):
                    html += f"<li>To achieve {int(sample.get('target_power', 0.8)*100)}% power, sample sizes of N₁≈{sample.get('required_n1_for_target_power', 'N/A')}, N₂≈{sample.get('required_n2_for_target_power', 'N/A')} would be needed.</li>"
                elif power >= sample.get('target_power', 0.8):
                    html += "<li>The current sample size provides adequate power.</li>"
            
            if not np.isnan(min_det.get('min_detectable_diff', np.nan)):
                html += f"<li>With the current sample size, the study has {int(min_det.get('target_power', 0.8)*100)}% power to detect a minimum difference of {float_formatter(min_det.get('min_detectable_diff', np.nan))}.</li>"
                
            html += """
                    </ul>
                </div>
            </div>
            """
            
            display(HTML(html))
            
        except Exception as e:
            print(f"Error generating HTML report: {e}. Falling back to text report.")
            _print_text_power_report(report, round_to)
    else:
        _print_text_power_report(report, round_to)

def _print_text_power_report(report: Dict[str, Any], round_to: int = 4) -> None:
    """Helper function to print a text-based power analysis report."""
    inputs = report['inputs']
    test = report['test_results']
    obs = report['observed_effect']
    sample = report['sample_size_analysis']
    min_det = report['minimum_detectable_difference']

    print("=======================================")
    print("    POWER ANALYSIS REPORT (T-TEST)     ")
    print("=======================================")

    print("\n--- INPUTS ---")
    print(f"Group A: Mean={inputs['mean_A']:.{round_to}f}, SD={inputs['sd_A']:.{round_to}f}, N={inputs['n_A']}")
    print(f"      {int(inputs['confidence_level']*100)}% CI: ({inputs['ci_A'][0]:.{round_to}f}, {inputs['ci_A'][1]:.{round_to}f})")
    print(f"Group B: Mean={inputs['mean_B']:.{round_to}f}, SD={inputs['sd_B']:.{round_to}f}, N={inputs['n_B']}")
    print(f"      {int(inputs['confidence_level']*100)}% CI: ({inputs['ci_B'][0]:.{round_to}f}, {inputs['ci_B'][1]:.{round_to}f})")
    print(f"Alpha: {inputs['alpha']}, Alternative: {inputs['alternative']}, Target Power: {inputs['target_power']}")

    print("\n--- HYPOTHESIS TEST RESULTS ---")
    print(f"Test Performed: {test.get('test', 'N/A')}")
    if 'error' in test:
        print(f"Error: {test['error']}")
    else:
        print(f"Null Hypothesis: {test.get('null_hypothesis', 'N/A')}")
        print(f"Alternative Hypothesis: {test.get('alternative_hypothesis', 'N/A')}")
        print(f"t-statistic: {test.get('t_statistic', np.nan):.{round_to}f}")
        print(f"Degrees of Freedom: {test.get('degrees_of_freedom', np.nan):.{round_to}f}")
        print(f"P-value: {test.get('p_value', np.nan):.{round_to}f}")
        
        # Format critical values nicely
        crits = test.get('critical_t_values', [])
        crit_str = ", ".join([f"{c:.{round_to}f}" for c in crits]) if isinstance(crits, tuple) or isinstance(crits, list) else f"{crits:.{round_to}f}"
        print(f"Critical t-value(s) at α={test.get('alpha', np.nan)}: {crit_str}")
        
        # Print confidence interval for the difference
        ci = test.get('confidence_interval', (np.nan, np.nan))
        print(f"{int(inputs['confidence_level']*100)}% CI for Mean Difference: ({ci[0]:.{round_to}f}, {ci[1]:.{round_to}f})")
        
        print(f"Conclusion: {test.get('conclusion', 'N/A')}")

    print("\n--- OBSERVED EFFECT & POWER ---")
    print(f"Observed Mean Difference (A - B): {obs.get('mean_difference', np.nan):.{round_to}f}")
    print(f"Observed Effect Size (Cohen's d): {obs.get('effect_size_cohen_d', np.nan):.{round_to}f}")
    print(f"Statistical Power for Observed Effect: {obs.get('power_for_observed_effect', np.nan):.{round_to}f}")

    print(f"\n--- SAMPLE SIZE FOR TARGET POWER ({sample.get('target_power', np.nan):.0%}) ---")
    print(f"  (Assuming true difference = {sample.get('assumed_delta', np.nan):.{round_to}f} and SDs = {sample.get('assumed_sds', (np.nan, np.nan))})")
    print(f"Required Sample Size (N1): {sample.get('required_n1_for_target_power', 'N/A')}")
    print(f"Required Sample Size (N2): {sample.get('required_n2_for_target_power', 'N/A')} (based on input ratio)")
    print(f"Actual Power with Required N: {sample.get('power_at_required_n', np.nan):.{round_to}f}")

    print(f"\n--- MINIMUM DETECTABLE DIFFERENCE (at {min_det.get('target_power', np.nan):.0%} Power) ---")
    print(f"  (With current sample sizes N1={min_det.get('current_n1', 'N/A')}, N2={min_det.get('current_n2', 'N/A')})")
    print(f"Minimum Detectable Mean Difference: {min_det.get('min_detectable_diff', np.nan):.{round_to}f}")
    print(f"Minimum Detectable Effect Size (d): {min_det.get('min_detectable_effect_size', np.nan):.{round_to}f}")

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
        print(f"With the current sample size, the study has {min_det.get('target_power', np.nan):.0%} power to detect a minimum difference of {min_det.get('min_detectable_diff', np.nan):.{round_to}f} (Effect Size d≈{min_det.get('min_detectable_effect_size', np.nan):.2f}).")
    else:
        print("Could not calculate minimum detectable difference.")

    print("=======================================")