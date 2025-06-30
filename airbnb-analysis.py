import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}') 

df = pd.read_csv('dataset/listings.csv')

hosts_df = df[['host_id', 'host_name']].drop_duplicates()

neighbour_df = df[['neighbourhood_cleansed', 'neighbourhood_group_cleansed']].drop_duplicates()
neighbour_df['neighbourhood_id'] = range(1, len(neighbour_df) + 1)

df = df.merge(neighbour_df, on=['neighbourhood_cleansed', 'neighbourhood_group_cleansed'])
listings_df = df[[
    'id', 'name', 'host_id', 'neighbourhood_id', 'latitude', 'longitude',
    'room_type', 'price', 'minimum_nights', 'availability_365'
]]
reviews_df = df[['id', 'number_of_reviews', 'last_review', 'reviews_per_month']].rename(columns={'id': 'listing_id'})

listings_df.loc[:, 'price'] = listings_df['price'].replace('[$,]', '', regex=True).astype(float)
reviews_df['last_review'] = pd.to_datetime(reviews_df['last_review'], errors='coerce')
reviews_df['reviews_per_month'] = reviews_df['reviews_per_month'].fillna(0)
listings_df = listings_df.dropna(subset=['price'])
reviews_df = reviews_df.dropna(subset=['last_review'])
neighbour_df = neighbour_df.rename(columns={'neighbourhood_cleansed': 'neighbourhood', 'neighbourhood_group_cleansed': 'neighbourhood_group'})

hosts_df.to_sql('hosts', engine, if_exists='replace', index=False)
neighbour_df[['neighbourhood', 'neighbourhood_group', 'neighbourhood_id']].to_sql('neighbourhoods', engine, if_exists='append', index=False)
listings_df.to_sql('listings', engine, if_exists='append', index=False)
reviews_df.to_sql('reviews_summary', engine, if_exists='append', index=False)

print("✅ Data loaded successfully into PostgreSQL.")