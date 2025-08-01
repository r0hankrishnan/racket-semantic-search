import pandas as pd
import numpy as np
import re

def _add_brand_column(raw_df:pd.DataFrame) -> pd.DataFrame:
    """Create a brand column.

    Args:
        raw_df (pd.DataFrame): The raw, scraped data set.

    Returns:
        pd.DataFrame: Raw data set with racquet brand column.
    """
    
    mod_df = raw_df.copy()
    mod_df["racquet_brand"] = mod_df["racquet_name"].apply(lambda x: x.split(" ")[0])
    _new_col_order = ["racquet_brand"] + [col for col in mod_df.columns if col != "racquet_brand"]
    mod_df = mod_df[_new_col_order]
    
    return mod_df

def _remove_junior_racquets(mod_df:pd.DataFrame) -> pd.DataFrame:
    """Remove any racquets with "Junior" in there names.

    Args:
        mod_df (pd.DataFrame): The modified raw dataframe with the added racquet name column.

    Returns:
        pd.DataFrame: Dataframe with racquet brand column, junior racquets removed.
    """
    
    jr_df = mod_df[mod_df["racquet_name"].str.contains("Junior")]
    no_jr_df = mod_df.merge(jr_df, how = "outer", indicator=True)
    no_jr_df = no_jr_df[no_jr_df["_merge"]=="left_only"].drop(columns="_merge")
    
    return no_jr_df

def _drop_majority_NA_cols(no_jr_df:pd.DataFrame) -> pd.DataFrame:
    """Drop all columns with more than 95% NA values.

    Args:
        no_jr_df (pd.DataFrame): Dataframe with junior racquets removed.

    Returns:
        pd.DataFrame: Dataframe with racquet brand column, junior racquets removed, and majority NA columns dropped.
    """
    
    na_dropped_df = no_jr_df.copy()
    
    cols_to_drop = []
    for col in no_jr_df.columns:
        if no_jr_df[col].isna().sum() == 0:
            pass
        elif no_jr_df[col].isna().sum() / no_jr_df.shape[0] > 0.95:
            cols_to_drop.append(col)
        else:
            pass
        
    na_dropped_df = na_dropped_df.drop(columns = cols_to_drop)
    na_dropped_df = na_dropped_df.reset_index().drop(columns = "index")
    
    return na_dropped_df

def _regex_transform_cols(na_dropped_df:pd.DataFrame) -> pd.DataFrame:
    """Use regex functions to convert string columns with non-standard formatting to float values.

    Args:
        na_dropped_df (pd.DataFrame): DataFrame with majority NA columns dropped.

    Returns:
        pd.DataFrame: DataFrame with racquet brand column, junior racquets removed, majority NA columns dropped, and string columns transformed.
    """
    
    regex_df = na_dropped_df.copy()
    
    # Get columns to change (might not need this)
    str_cols = [] 
    for col in regex_df.columns:
        if regex_df[col].dtype == "object" and "racquet_" not in col:
            str_cols.append(col)
        else:
            pass
    
    # Extract racquet head size in sq. inches
    regex_df["racquet_head_size_sq_in"] = (
        regex_df["Head Size"]\
            .str.extract(r"(\d+\.?\d*)\s*(?:in²|in|sq\s*in)")\
                .astype(float)
                )
    
    # Extract racquet length in inches
    regex_df["racquet_length_in"] = (
        regex_df["Length"]\
            .str.extract(r"(\d+\.?\d*)\s*(?:in²|in|sq\s*in)")\
                .astype(float)
                )
    
    # Extract strung weight in ounces 
    regex_df["racquet_strung_weight_oz"] = (
        regex_df["Strung Weight"]\
            .str.extract(r"(\d+\.?\d*)\s*")\
                .astype(float)
                )
    
    # Extract racquet balance inches value
    regex_df["racquet_balance_in"] = (
        regex_df["Balance"]\
            .str.extract(r"(\d+(?:\.\d+)?)\s*in\b")\
                .astype(float)
                )
    
    # Extract Balance number and label separately
    extracted = regex_df["Balance"].str.extract(
        r"(\d+(?:\.\d+)?)\s*(?:pts\s*)?(HL|HH|EB)\b"
    )

    extracted.columns = ["value", "label"]

    extracted["value"] = extracted["value"].astype(float)

    def apply_balance_sign(row):
        if row["label"] == "HL":
            return row['value']
        elif row["label"] == "HH":
            return -row["value"]
        elif row["label"] == "EB":
            return 0.0
        return None

    # Extract and apply discrete headlight indicator
    regex_df["racquet_balance_HH_HL"] = extracted.apply(apply_balance_sign, axis = 1)
    
    # Extract racquet stiffness
    regex_df["racquet_stiffness"] = regex_df["Stiffness"]
    regex_df['racquet_stiffness'] = regex_df['racquet_stiffness'].replace('N/A (very low)', np.nan)
    regex_df["racquet_stiffness"] = regex_df["racquet_stiffness"].astype(float)
    
    # Get average beam width as proxy for 3-value beam width field
    def average_beam_width(value):
        if isinstance(value, str):
            parts = value.split("/")
            numbers = []
            for part in parts:
                cleaned = part.strip().replace("mm", "")
                if cleaned:
                    try:
                        numbers.append(float(cleaned))
                    except ValueError:
                        pass
            if numbers:
                return sum(numbers) / len(numbers)
            else:
                return float("nan")
        else:
            return float("nan")
    
    # Extract and apply average beam width function
    regex_df["racquet_avg_beam_width"] = regex_df["Beam Width"].apply(average_beam_width)
    
    # Extract main and cross values, assign to relevant column in series, and pass series to df
    def extract_mains_crosses(value):
        mains = np.nan
        crosses = np.nan
        
        if isinstance(value, str) and value.strip():
            
            mains_regex = re.search(r'(\d+)\s*Mains', value, re.IGNORECASE)
            crosses_regex = re.search(r'(\d+)\s*Crosses', value, re.IGNORECASE)
            
            if mains_regex:
                mains = float(mains_regex.group(1))
                
            if crosses_regex:
                crosses = float(crosses_regex.group(1))
                
        return pd.Series([mains, crosses])

    # Extract main and cross values and apply to respective columns
    regex_df[["racquet_mains", "racquet_crosses"]] = regex_df["String Pattern"].apply(extract_mains_crosses)
    
    # Define function to get tension upper and lower bounds
    def extract_tension_bounds(value):
        lower = np.nan
        upper = np.nan
        
        if isinstance(value, str) and value.strip():
            tension_regex = re.search(r'(\d+)\s*-\s*(\d+)', value)
            if tension_regex:
                lower = float(tension_regex.group(1))
                upper = float(tension_regex.group(2))
            
        return pd.Series([lower, upper])

    # Extract and apply tension bounds to new columns
    regex_df[["racquet_tension_lower", "racquet_tension_upper"]] = regex_df["String Tension"].apply(extract_tension_bounds)
    
    return regex_df

def _final_touch_ups(regex_df:pd.DataFrame) -> pd.DataFrame:
    """Drop non-regexed columns, standardized naming conventions of columns

    Args:
        regex_df (pd.DataFrame): DataFrame with regexed columns.

    Returns:
        pd.DataFrame: DataFrame with racquet brand column, junior racquets removed, majority NA columns dropped, 
        string columns transformed, old columns dropped, and column names standardized.
    """
    
    intermediate_df = regex_df.copy()
    drop_cols = ["Head Size", "Length", "Strung Weight", "Balance", "Beam Width", "String Pattern", "String Tension", "Stiffness"]
    
    intermediate_df.drop(columns = drop_cols, inplace = True)
    intermediate_df.rename(columns = {"Swingweight":"racquet_swingweight",
                                    "Composition":"racquet_composition",
                                    "Power Level":"racquet_power",
                                    "Stroke Style":"racquet_stroke_style",
                                    "Swing Speed":"racquet_swing_speed",
                                    "Racquet Colors":"racquet_colors",
                                    "Grip Type":"racquet_grip"},
                        inplace = True)
    
    return intermediate_df

def preprocess_raw_data(raw_df:pd.DataFrame) -> pd.DataFrame:
    
    mod_df = _add_brand_column(raw_df=raw_df)
    
    no_jr_df = _remove_junior_racquets(mod_df=mod_df)
    
    na_dropped_df = _drop_majority_NA_cols(no_jr_df=no_jr_df)
    
    regex_df = _regex_transform_cols(na_dropped_df=na_dropped_df)
    
    intermediate_df = _final_touch_ups(regex_df=regex_df)
    
    return intermediate_df