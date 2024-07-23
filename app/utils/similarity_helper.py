from fastapi import FastAPI, HTTPException
import pickle
from typing import List, Dict, Any
import numpy as np
import os

# Load data from pickle file on startup
def load_pkl_file(filepath):
    with open(filepath, 'rb') as file:
        similar_products_df = pickle.load(file)
        return similar_products_df



def find_similar_products_by_uniq_id(uniq_id: str, num_similar: int) -> Dict[str, Any]:
    """
    Find similar products based on the product's unique ID using precomputed embeddings stored in a pickle file.

    Embedding Creation and Saving:
    1. Create Sentence Embeddings:
        - Used the SentenceTransformer model from the sentence-transformers library to create embeddings for the product tags.
        - The model used is 'sentence-transformers/all-mpnet-base-v2', which is a pre-trained model designed for generating sentence embeddings.
        - Encoded the tags into embeddings and converted them to numpy arrays for easier manipulation.

    2. Save Embeddings to a Pickle File:
        - After creating the embeddings, saved them into a pickle file for later use.

    The function `find_similar_products_by_uniq_id` uses cosine similarity to find similar products.
    It ensures that the given product ID exists, retrieves the similar products, and sorts them by similarity score and rating as a tie-breaker.

    Args:
        uniq_id (str): The unique identifier of the product.
        num_similar (int): The number of similar products to retrieve.

    Returns:
        Dict[str, Any]: A dictionary containing the selected product details and a list of similar products.

    Raises:
        HTTPException: If the product ID is not found.
    """
    cwd = os.getcwd()
    filepath = os.path.join(os.path.dirname(__file__), '../data/similar_products.pkl')
    similar_products_df = load_pkl_file(filepath)
    if uniq_id not in similar_products_df['uniq_id'].values:
        raise HTTPException(status_code=404, detail="Product ID not found")

    product_row = similar_products_df[similar_products_df['uniq_id'] == uniq_id].iloc[0]
    similar_products = product_row['similar_products'][:num_similar]

    # Sort similar products by similarity score and use rating as tie-breaker
    similar_products = sorted(similar_products, key=lambda x: (-x['similarity'], -float(x['rating'])))
    
    # Convert numpy data types to standard Python types
    for product in similar_products:
        product['similarity'] = float(product['similarity'])  # Convert numpy float to Python float
        if isinstance(product['rating'], np.generic):
            product['rating'] = product['rating'].item()  # Convert numpy type to Python type
        if isinstance(product['sales_price'], np.generic):
            product['sales_price'] = product['sales_price'].item()  # Convert numpy type to Python type

    # Sort similar products by similarity score and use rating as tie-breaker
    similar_products = sorted(similar_products, key=lambda x: (-x['similarity'], -float(x['rating'])))

    selected_product_details = {
        "uniq_id": product_row['uniq_id'],
        "product_name": product_row['product_name'],
        "brand": product_row['brand'],
        "colour": product_row['colour'],
        "rating": product_row['rating'],
        "medium": product_row['medium'],
        "sales_price": product_row['sales_price']
    }

    return {
        "selected_product": selected_product_details,
        "similar_products": similar_products
    }