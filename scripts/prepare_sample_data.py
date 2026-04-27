import pandas as pd
import os

def prepare_samples():
    """Creates a small slice of data for cloud deployment."""
    countries = ["ethiopia", "kenya", "sudan", "tanzania", "nigeria"]
    target_dir = "app/sample_data"
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"Created {target_dir}")

    for country in countries:
        source = f"data/{country}_clean.csv"
        dest = f"{target_dir}/{country}_clean.csv"
        
        if os.path.exists(source):
            # Take only the first 500 rows to keep it lightweight for GitHub
            df = pd.read_csv(source)
            df.head(500).to_csv(dest, index=False)
            print(f"DONE: Created sample for {country} ({dest})")
        else:
            print(f"SKIP: Source {source} not found.")

if __name__ == "__main__":
    prepare_samples()
