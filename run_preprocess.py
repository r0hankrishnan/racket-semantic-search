from src.data.preprocess import preprocess_raw_data
import datashelf.core as ds

if __name__ == "__main__":
    
    raw_df = ds.load(
        collection_name="racquets",
        hash_value="55dabe54d8b602a3c993460db0bf085737dc2c78a148e6d9fe5ea09f75b0e8ef"
    )
    
    intermediate_df = preprocess_raw_data(raw_df=raw_df)
    
    ds.save(
        df = intermediate_df,
        collection_name = "racquets",
        name="Basic Cleaned Data",
        tag="cleaned",
        message=("Removed all junior racquets. Removed duplicate columns. Used regex to extract"
                 "values for specially formatted columns. Standardized column naming. Dropped all"
                 "non-preprocessed columns.")
        )