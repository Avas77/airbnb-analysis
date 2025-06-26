import pandas as pd
from sqlalchemy import create_engine

db_user = 'postgres'
db_pass = 'buddy123'
db_host = 'localhost'
db_port = '5432'
db_name = 'airbnb'

engine = create_engine(f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}') 

df = pd.read_csv('dataset/listings.csv')

columns_to_keep = [
    'id', 'name', 'host_id', 'host_name',
    'neighbourhood', 'latitude', 'longitude', 'room_type', 'price',
    'minimum_nights', 'number_of_reviews', 'last_review',
    'reviews_per_month', 'calculated_host_listings_count', 'availability_365'
]
df = df[columns_to_keep]

df['price'] = df['price'].replace('[$,]', '', regex=True).astype(float)
df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
df = df.dropna(subset=['price'])
df.to_sql('listings', engine, if_exists='replace', index=False)

print("✅ Data loaded successfully into PostgreSQL.")