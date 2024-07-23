import logging
import os
from fastapi import HTTPException
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from .similarity_helper import load_pkl_file
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_KEY = os.getenv("QDRANT_KEY")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

# Load the Sentence Transformer model
encoder = SentenceTransformer("all-MiniLM-L6-v2")

def get_qdrant_client():
    """
    Initialize and return the Qdrant client.

    Returns:
        QdrantClient: The client instance for interacting with Qdrant.
    """
    try:
        client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)
        logger.info("Qdrant client initialized successfully.")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant client: {e}")
        raise

# Initialize Qdrant client
qdrant_client = get_qdrant_client()

# Load the DataFrame from the pickle file
cwd = os.getcwd()
filepath = f'{cwd}/app/data/similar_products.pkl'
qdrant_df = load_pkl_file(filepath)

def create_qdrant_collection():
    """
    Create a collection in Qdrant with the appropriate vector configuration.
    """
    vector_size = len(qdrant_df['tags'][5])  # Size of your vectors

    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )



def insert_vectors_to_collection():
    """
    Insert vectors into the Qdrant collection from the DataFrame.
    """
    points = []
    index = 0
    for _, row in qdrant_df.iterrows():
        point = PointStruct(
            id=index,
            payload={
                'uniq_id': row['uniq_id'],
                'product_name': row['product_name'],
                'brand': row['brand'],
                'medium': row['medium'],
                'colour': row['colour'],
                'sales_price': row['sales_price'],
                'rating': row['rating']
            },
            vector=row['tags']
        )
        points.append(point)
        index = index+1

    # Batch upload points to the collection
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=points)

def search_similar_products(uniq_id: str, num_similar: int):
    """
    Search for similar products in the Qdrant collection based on the provided uniq_id.

    Args:
        uniq_id (str): The unique identifier of the product to find similarities for.
        num_similar (int): The number of similar products to retrieve.

    Returns:
        Dict[str, Any]: The details of the selected product and a list of similar products.

    Raises:
        HTTPException: If the product ID is not found in the DataFrame.
    """
    try:
        # Ensure the DataFrame is loaded
        if uniq_id not in qdrant_df['uniq_id'].values:
            raise HTTPException(status_code=404, detail="Product ID not found")

        # Fetch the product_name for the given uniq_id
        product_row = qdrant_df[qdrant_df['uniq_id'] == uniq_id].iloc[0]
        product_name = product_row['product_name']

        # Encode the product name
        query_vector = encoder.encode(product_name).tolist()

        # Perform the search in Qdrant
        hits = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=num_similar + 1  # Include the product itself
        )

        # Retrieve selected product details
        selected_product_id = hits[0].id
        selected_product = qdrant_df.iloc[selected_product_id]
        selected_product_details = {
            "uniq_id": selected_product['uniq_id'],
            "product_name": selected_product['product_name'],
            "brand": selected_product['brand'],
            "colour": selected_product['colour'],
            "rating": selected_product['rating'],
            "medium": selected_product['medium'],
            "sales_price": selected_product['sales_price']
        }

        # Retrieve similar products details
        similar_products = []
        for hit in hits[1:]:
            similar_product = qdrant_df.iloc[hit.id]
            similar_products.append({
                "similar_uniq_id": similar_product['uniq_id'],
                "similar_product_name": similar_product['product_name'],
                "brand": similar_product['brand'],
                "colour": similar_product['colour'],
                "rating": similar_product['rating'],
                "medium": similar_product['medium'],
                "sales_price": similar_product['sales_price'],
                "similarity": float(hit.score)  # Convert numpy float to Python float
            })
        # Sort similar products by similarity score and use rating as tie-breaker
        similar_products = sorted(similar_products, key=lambda x: (-x['similarity'], -float(x['rating'])))
        return {
            "selected_product": selected_product_details,
            "similar_products": similar_products
        }
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")
