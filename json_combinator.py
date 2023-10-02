import pandas as pd

meat_data = pd.read_json(r'coles_scraper/coles_meat.json')
pantry_data = pd.read_json(r'coles_scraper/coles_dairy_eggs.json')
eggs_dairy_data = pd.read_json(r'coles_scraper/coles_dairy_eggs.json')
fruits_vegies_data = pd.read_json(r'coles_scraper/coles_fruits_vegies.json')

merged_df = pd.concat([meat_data, pantry_data, eggs_dairy_data, fruits_vegies_data], ignore_index=True)

print(merged_df.head(5))
