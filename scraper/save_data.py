import pandas as pd
import json

def write_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def write_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
