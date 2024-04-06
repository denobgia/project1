import pandas as pd

def findBestBookmaker(df):
    # Calculate the inverse of each price by dividing 1 by the price column
    df['inverse_price'] = 1 / df['price']
    # Group the DataFrame by id and bookmaker's title and calculate the sum of the inverse_price column for each group
    summarized_df = df.groupby(['id', 'bookmakers.title'])['inverse_price'].sum().reset_index()
    # Gruppiere pro Bookmakers.title und gib den Durchschnitt der inverse_price aus.
    grouped_df = summarized_df.groupby('bookmakers.title')['inverse_price'].mean().reset_index()
    # Finde den index mit dem tiefstem inverse_price
    min_index = grouped_df['inverse_price'].idxmin()
    # Bookmaker mit tiefstem inverse_Price
    best_bookmaker = grouped_df.loc[min_index, 'bookmakers.title']
    lowest_inverse_price = round(grouped_df.loc[min_index, 'inverse_price'],2)
    result = {'bookmaker': best_bookmaker, 'margin': lowest_inverse_price}

    return result
      