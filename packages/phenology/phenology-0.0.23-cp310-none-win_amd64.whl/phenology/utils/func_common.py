import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures
from shapely.geometry import Point
from pyproj import CRS
from scipy import stats


def compare_two_groups(x, y, label, alpha=0.05, alternative='two-sided', extra_d_when_nonparam=True):
    """
    Compare two numeric datasets by checking normality (Shapiro-Wilk) and homogeneity 
    of variances (Levene), then automatically select either an independent t-test 
    (equal variances or Welch) or the Mann-Whitney U test. Returns a one-row DataFrame 
    with sample sizes, descriptive statistics, chosen test, p-values (raw and formatted), 
    and effect size (Cohen's d or rank-biserial correlation).
    
    If extra_d_when_nonparam is True, an additional Cohen's d is computed in the non-normal branch.
    
    Parameters
    ----------
    x, y : array-like
        Two arrays of numeric data (e.g. list, np.ndarray, pd.Series).
    label : str
        Identifier stored in the "#" column.
    alpha : float, optional
        Significance level for the normality and variance tests (default 0.05).
    alternative : {'two-sided', 'less', 'greater'}, optional
        Alternative hypothesis for the tests (default 'two-sided').
    extra_d_when_nonparam : bool, optional
        Whether to compute an extra Cohen's d when using the Mann-Whitney U test.
    
    Returns
    -------
    pd.DataFrame
        A single-row DataFrame with columns including sample sizes, means, medians,
        normality and variance test results, test used, test statistic, p-values (raw 
        and formatted), and effect size.
    """
    # ---------- Helper: Format very small p-values ----------
    def fp(p, th=1e-16):
        """If p < th, return '< 1.0e-16'; otherwise, return in scientific notation."""
        if np.isnan(p):
            return "nan"
        return f"< {th:.1e}" if p < th else f"{p:.3g}"
    
    # ---------- Helper: Compute Cohen's d ----------
    def cohen_d(a, b):
        va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
        pooled_std = np.sqrt(((len(a) - 1) * va + (len(b) - 1) * vb) / (len(a) + len(b) - 2))
        return (np.mean(a) - np.mean(b)) / pooled_std
    
    # ---------- Data cleaning: Convert to numpy arrays and remove NaNs ----------
    arr1 = np.array(x, dtype=float); arr1 = arr1[~np.isnan(arr1)]
    arr2 = np.array(y, dtype=float); arr2 = arr2[~np.isnan(arr2)]
    n1, n2 = len(arr1), len(arr2)
    
    if n1 < 2 or n2 < 2:
        return pd.DataFrame([{"#": label, 
                               "Error": "Insufficient sample size for statistical testing.", 
                               "Sample Sizes": (n1, n2)}])
    
    # ---------- Shapiro-Wilk Test for Normality ----------
    statn1, pn1 = stats.shapiro(arr1) if n1 >= 3 else (np.nan, np.nan)
    statn2, pn2 = stats.shapiro(arr2) if n2 >= 3 else (np.nan, np.nan)
    normality = (pn1 > alpha) and (pn2 > alpha) if not (np.isnan(pn1) or np.isnan(pn2)) else False
    
    # ---------- Levene's Test for Homogeneity of Variances ----------
    statv, pv = stats.levene(arr1, arr2)
    var_eq = (pv > alpha)
    
    # ---------- Initialize result dictionary ----------
    rd = {
        "#": label,
        "Sample Sizes": (n1, n2),
        "Mean (Group1)": arr1.mean(),
        "Mean (Group2)": arr2.mean(),
        "Median (Group1)": np.median(arr1),
        "Median (Group2)": np.median(arr2),
        "Var (Group1)": arr1.var(),
        "Var (Group2)": arr2.var(),
        # Shapiro-Wilk test results
        "Shapiro-Wilk p": (pn1, pn2),
        "Shapiro-Wilk p_str": (fp(pn1), fp(pn2)),

        # Levene test results
        "Levene p": pv,
        "Levene p_str": fp(pv),

        "Normality": normality,
        "VarEqual": var_eq,
        
    }
    
    # ---------- Choose test and compute effect size ----------
    if normality:
        # If data are normal -> use t-test (independent or Welch)
        if var_eq:
            t_stat, p_val = stats.ttest_ind(arr1, arr2, equal_var=True, alternative=alternative)
            test_used = "Independent t-test (equal var)"
        else:
            t_stat, p_val = stats.ttest_ind(arr1, arr2, equal_var=False, alternative=alternative)
            test_used = "Welch t-test (unequal var)"
        
        rd.update({
            "Test Used": test_used,
            "Test Statistic": t_stat,
            "p-value": p_val,
            "p-value_str": fp(p_val),
            "Cohen's d": cohen_d(arr1, arr2)
        })
    else:
        # If data are non-normal -> use Mann-Whitney U test
        u_stat, p_val = stats.mannwhitneyu(arr1, arr2, alternative=alternative)
        rb = 1 - 2 * min(u_stat, n1 * n2 - u_stat) / (n1 * n2)
        rd.update({
            "Test Used": "Mann-Whitney U",
            "Test Statistic": u_stat,
            "p-value": p_val,
            "p-value_str": fp(p_val),
            "Rank-biserial correlation": rb
        })
        if extra_d_when_nonparam:
            rd["Extra Cohen's d"] = cohen_d(arr1, arr2)
    
    return pd.DataFrame([rd]).T



def df2shp(output_file, df, lat_name='lat', lon_name='lon', max_length=10):
    """
    Truncate DataFrame column names to a maximum length (default 10 characters) ensuring uniqueness,
    and convert the DataFrame to a shapefile.

    If the absolute longitude values exceed 190, adjust longitudes by subtracting 360 for those > 180.
    The function creates a GeoDataFrame using the specified longitude and latitude columns, sets the CRS
    to EPSG:4326, and writes the shapefile to the given output_file path.

    Parameters:
        output_file (str): Path where the shapefile will be saved.
        df (pd.DataFrame): Input DataFrame.
        lat_name (str): Name of the latitude column (default 'lat').
        lon_name (str): Name of the longitude column (default 'lon').
        max_length (int): Maximum length for truncated column names (default 10).

    Returns:
        None
    """
    # Truncate column names and ensure uniqueness
    new_columns = []
    for col in df.columns:
        truncated = col[:max_length]
        suffix = 1
        # Ensure the truncated name is unique among already processed columns.
        while truncated in new_columns:
            truncated = col[:max_length - len(str(suffix))] + str(suffix)
            suffix += 1
        new_columns.append(truncated)
    df.columns = new_columns

    # Adjust longitude values if necessary: if any absolute value exceeds 190, 
    # subtract 360 from values greater than 180.
    longs = df[lon_name].values
    if np.nanmax(np.abs(longs)) > 190:
        # Use boolean indexing for efficient adjustments.
        df.loc[df[lon_name] > 180, lon_name] -= 360

    # Create a geometry column using longitude and latitude
    df.loc[:, 'geometry'] = [Point(lon, lat) for lon, lat in zip(df[lon_name], df[lat_name])]
    
    # Create GeoDataFrame and set CRS to EPSG:4326
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = CRS.from_epsg(4326)
    
    # Save the GeoDataFrame as a shapefile
    gdf.to_file(output_file)



def get_summary(correlations, p_values):
    """
    Analyze statistically significant correlations across p-value thresholds.

    Processes input arrays through:
    1. Data validation: Filters non-NaN correlations with valid p-values (0-1)
    2. Threshold analysis: For each p-value cutoff (0.01, 0.05, 0.10, Total):
       a. Filters correlations meeting significance criteria
       b. Categorizes into positive/neutral/negative
       c. Calculates counts and percentages (relative to total and significant)
    3. Returns formatted comparison table

    Parameters:
        correlations (np.ndarray): Correlation coefficients array (-1 to 1)
        p_values (np.ndarray): Corresponding p-values array (0 to 1)

    Returns:
        pd.DataFrame: Summary table with columns:
            - Significance Level: Threshold (p < X) or 'Total'
            - Positive: Count (percentage of total)
            - Neutral: Count (percentage of total)
            - Negative: Count (percentage of total)
            - Pos/Neg Ratio: Ratio (significant positives vs negatives)

    Percentages show both:
    - Absolute %: Relative to all valid data points
    - Relative %: Within significant results (Pos/Neg ratio calculation)
    """
    # Validate and filter input data
    valid_mask = ~np.isnan(correlations) & (p_values >= 0) & (p_values <= 1)
    filtered_corrs = correlations[valid_mask]
    filtered_pvals = p_values[valid_mask]
    total_valid = len(filtered_corrs)

    results = []
    ANALYSIS_LEVELS = [
        ('0.01', 0.01), 
        ('0.05', 0.05), 
        ('0.10', 0.10), 
        ('1.01', 1.01)  # Special case for total
    ]

    for threshold_str, p_cutoff in ANALYSIS_LEVELS:
        # Apply p-value filter
        significant_corrs = filtered_corrs.copy()
        if p_cutoff <= 0.1:
            significant_corrs[filtered_pvals >= p_cutoff] = np.nan
        
        # Remove non-significant values (except for total case)
        analyzed_corrs = significant_corrs[~np.isnan(significant_corrs)]

        # Categorize correlations
        positive = np.sum(analyzed_corrs > 0)
        neutral = np.sum(analyzed_corrs == 0)
        negative = np.sum(analyzed_corrs < 0)
        total_significant = positive + negative

        # Calculate percentages relative to total valid
        positive_pct = positive / total_valid * 100
        neutral_pct = neutral / total_valid * 100
        negative_pct = negative / total_valid * 100

        # Calculate relative distribution (excluding neutral)
        denominator = total_significant if total_significant > 0 else 1
        positive_ratio_pct = positive / denominator * 100
        negative_ratio_pct = negative / denominator * 100

        # Safely format ratio
        if negative_ratio_pct == 0:
            ratio_str = "Inf" if positive_ratio_pct > 0 else "N/A"
        else:
            ratio_str = f"{positive_ratio_pct/negative_ratio_pct:.2f}"

        # Format output row
        level_label = 'Total' if threshold_str == '1.01' else f'p < {threshold_str}'
        results.append(pd.DataFrame({
            'Significance Level': [level_label],
            'Positive': [f"{positive} ({positive_pct:.2f}%)"],
            'Neutral': [f"{neutral} ({neutral_pct:.2f}%)"],
            'Negative': [f"{negative} ({negative_pct:.2f}%)"],
            'Pos/Neg Ratio': [f"{ratio_str} = {positive_ratio_pct:.2f}% : {negative_ratio_pct:.2f}%"]
        }))

    return pd.concat(results).reset_index(drop=True)



def fit_ols_model(x, y, degree):
    """
    Fit a polynomial Ordinary Least Squares (OLS) regression model to the data.
    
    This function creates polynomial features of a specified degree from the input predictor x,
    fits an OLS regression model to predict the response variable y, and computes various model statistics.
    It returns a range of x values for plotting the fitted curve, predicted y values over that range,
    along with key statistics including the coefficient, p-value, intercept, R-squared value, the fitted model,
    and the confidence interval bounds for the predictions.
    
    Parameters:
        x (np.ndarray): 1D array of predictor values.
        y (np.ndarray): 1D array of response values.
        degree (int): Degree of the polynomial to fit.
        
    Returns:
        tuple: A tuple containing:
            - x_range (np.ndarray): A linearly spaced array covering the range of x values.
            - y_range (np.ndarray): Predicted y values corresponding to x_range.
            - coef (float): Coefficient of the first polynomial feature (slope component).
            - p_val (float): p-value for the first predictor coefficient.
            - intercept (float): Intercept of the fitted model.
            - r2 (float): R-squared value of the model fit.
            - model: The fitted OLS model object.
            - ci_low (np.ndarray): Lower bounds of the confidence intervals for predictions.
            - ci_high (np.ndarray): Upper bounds of the confidence intervals for predictions.
    
    Example:
        >>> import numpy as np
        >>> x = np.linspace(0, 10, 50)
        >>> y = 3 * x + np.random.randn(50)
        >>> x_range, y_range, coef, p_val, intercept, r2, model, ci_low, ci_high = fit_ols_model(x, y, degree=1)
    """
    # Fit the polynomial transformation of x
    poly = PolynomialFeatures(degree=degree)
    x_poly = poly.fit_transform(x.reshape(-1, 1))
    
    # Add a constant term and fit the OLS model
    X = sm.add_constant(x_poly)
    model = sm.OLS(y, X).fit()
    
    # Extract key statistics from the model
    r2 = model.rsquared
    p_val = model.pvalues[1]
    coef = model.params[1]
    intercept = model.params[0]
    
    # Generate a range of x values for plotting predictions
    x_range = np.linspace(x.min(), x.max(), 100)
    x_poly_range = poly.fit_transform(x_range.reshape(-1, 1))
    
    # Get predicted y values and confidence intervals
    y_range = model.predict(sm.add_constant(x_poly_range))
    predictions = model.get_prediction(sm.add_constant(x_poly_range))
    ci_low, ci_high = predictions.conf_int().T  # confidence intervals
    
    return x_range, y_range, coef, p_val, intercept, r2, model, ci_low, ci_high



def remove_outliers(data, threshold=3):
    """
    Function to remove outliers from a given data array.

    Parameters:
    - data: One-dimensional or multi-dimensional data array, can be a pandas Series, NumPy array, or xarray.DataArray.
    - threshold: Threshold for outliers in terms of the data standard deviation. Default is 3.

    Returns:
    - Processed data array with outliers beyond the threshold replaced with NaN.

    Note:
    - For NumPy arrays, the function directly modifies the input array, replacing outliers with NaN.
    - For xarray.DataArray, a new array is generated where outliers are replaced with NaN, and the original array remains unaffected.
    - If the input is a pandas Series, a new Series is generated with outliers replaced with NaN, and the original Series remains unaffected.

    """
    
    # Calculate the standard deviation, mean, and center the data
    data_std = np.nanstd(data)
    data_mean = np.nanmean(data)
    data_centered = np.abs(data - data_mean)
    
    # Remove outliers based on the threshold and data type
    if isinstance(data, xr.DataArray):
        data = xr.where(data_centered > threshold*data_std, np.nan, data)
    else:
        data[data_centered > threshold*data_std] = np.nan

    return data


