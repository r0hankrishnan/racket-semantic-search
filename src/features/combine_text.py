import pandas as pd
from typing import List

def structured_combine_text(df:pd.DataFrame, object_cols:List[str]) -> pd.DataFrame:
    _df = df.copy()
    _df["combined_col"] = ""
    
    _replacements = str.maketrans({
        "!":".",
        "_":" ",
        "&":"and",
        "²":"",
        "\xa0":"",
        "\n":"",
        "\r":"",
        '"':"",
        '“':"",
        "+":"plus",
        "%":"percent"
    })
    
    _title_dict = {
        "racquet_brand":"Racquet Brand",
        "racquet_name":"Racquet Name",
        "racquet_desc":"Racquet Description",
        "racquet_composition":"Racquet Composition",
        "racquet_power":"Racquet Power Level",
        "racquet_stroke_style":"Racquet Stroke Style",
        "racquet_swing_speed":"Racquet Swing Speed",
        "racquet_colors":"Racquet Colors",
        "racquet_grip":"Racquet Grip Type"
    }
    
    for col in object_cols:        
        _content = _df[col].fillna("").astype(str).str.translate(_replacements)
        _content = _content.str.replace("in²", "inches squared", regex=False).str.replace("  ", " ", regex=False)
        _df["combined_col"] += _title_dict[col] + ": " + _content + "\n"
            
    return _df["combined_col"]


def create_natural_combined_text(row:pd.Series) -> str:
    def safe(val):
        return "unkown" if pd.isna(val) else str(val.strip())
    
    if row["racquet_balance_HH_HL"] < 0:
        hh_hl_tag = "head light"
    elif row["racquet_balance_HH_HL"]>0:
        hh_hl_tag = "head heavy"
    else:
        hh_hl_tag = "equally balanced"
    
    combined_text = (
        f"The {safe(row['racquet_name'])} is a {safe(row['racquet_power']).lower()} powered racquet designed for players with "
        f"{safe(row['racquet_stroke_style']).lower()} strokes and {safe(row['racquet_swing_speed']).lower()} swings. "
        f"It features a stiffness rating of {row['racquet_stiffness']} and a {str(row['racquet_composition']).lower()} "
        f"composition. The racquet has a {row['racquet_swingweight']} ounce swing weight, a {row['racquet_head_size_sq_in']} "
        f"square inch head size, a {row['racquet_strung_weight_oz']} ounce strung weight, "
        f"and has a {row['racquet_mains']} by {row['racquet_crosses']} string pattern. "
        f"The racquet has a tension range of {row['racquet_tension_lower']} pounds (lbs) to {row['racquet_tension_upper']} pounds (lbs). "
        f"The racquet has an average beam width of {row['racquet_avg_beam_width']}, with a {row['racquet_balance_in']} inch balance point, "
        f"and is {'' if row['racquet_balance_HH_HL'] == 0 else row['racquet_balance_HH_HL']} {hh_hl_tag}. The racquet has a "
        f"{row['racquet_colors']} colorway and has a price of {row['racquet_price']} dollars."
        )
    
    return " ".join(combined_text.split())


def create_natural_combined_text_v2(row:pd.Series) -> str:
    def safe(val):
        return "unkown" if pd.isna(val) else str(val.strip())
    
    if row["racquet_balance_HH_HL"] < 0:
        hh_hl_tag = "head light"
    elif row["racquet_balance_HH_HL"]>0:
        hh_hl_tag = "head heavy"
    else:
        hh_hl_tag = "equally balanced"
    
    combined_text = (
        f"The {safe(row['racquet_name'])} is a {safe(row['racquet_power']).lower()} powered racquet designed for players with "
        f"{safe(row['racquet_stroke_style']).lower()} strokes and {safe(row['racquet_swing_speed']).lower()} swings. "
        f"It features a stiffness rating of {row['racquet_stiffness']} and a {str(row['racquet_composition']).lower()} "
        f"composition. The racquet has a {row['racquet_swingweight']} ounce swing weight, a {row['racquet_head_size_sq_in']} "
        f"square inch head size, a {row['racquet_strung_weight_oz']} ounce strung weight, "
        f"and has a {row['racquet_mains']} by {row['racquet_crosses']} string pattern. "
        f"The racquet has a tension range of {row['racquet_tension_lower']} pounds (lbs) to {row['racquet_tension_upper']} pounds (lbs). "
        f"The racquet has an average beam width of {row['racquet_avg_beam_width']}, with a {row['racquet_balance_in']} inch balance point, "
        f"and is {'' if row['racquet_balance_HH_HL'] == 0 else row['racquet_balance_HH_HL']} {hh_hl_tag}. The racquet has a "
        f"{row['racquet_colors']} colorway and has a price of {row['racquet_price']} dollars."
        f"\n\nHere is the marketing blurb for the {safe(row['racquet_name'])}:\n{row['racquet_desc']}"
        )
    
    return " ".join(combined_text.split())