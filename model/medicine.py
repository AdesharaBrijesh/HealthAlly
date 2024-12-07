import pandas as pd
import faiss
import pickle
import numpy as np

def load_medicine_data():
    try:
        index = faiss.read_index('medicine_faiss_index.bin')
        df = pd.read_pickle('medicine_df.pkl')
        
        if df.empty:
            raise ValueError("Loaded DataFrame is empty")
        
        return index, df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None, None

# Load index and DataFrame
faiss_index, medicine_df = load_medicine_data()

def search_medicine(query):
    try:
        query = query.lower()  # Normalize the query

        # Dynamic column search for text columns
        search_columns = [col for col in medicine_df.columns if medicine_df[col].dtype == 'object']
        
        # Construct search mask: Ensure no NaN values are passed to str.contains
        mask = medicine_df[search_columns].apply(
            lambda col: col.str.lower().str.contains(query, na=False)  # Correct handling of NaN
        ).any(axis=1)
        
        results = medicine_df[mask].head(3)  # Limit to top 3 results
        
        if not results.empty:
            # Return formatted results for the primary and alternatives
            return {
                "primary": results.iloc[0].to_dict(),  # First result as primary
                "alternatives": results.iloc[1:].to_dict('records')  # Remaining as alternatives
            }
        else:
            return None
    
    except Exception as e:
        print(f"Error in search: {e}")
        return None

if __name__ == "__main__":
    query = "headache fever"
    result = search_medicine(query)
    print(result)
