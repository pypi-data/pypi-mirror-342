import pandas as pd
from cat_stat_analysis.main import cat_stat_analysis

data = {
    'Gender': ['Male', 'Female', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
    'Purchase': ['Yes', 'No', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes']
}
df = pd.DataFrame(data)

cat_stat_analysis(df, 'Gender', 'Purchase')