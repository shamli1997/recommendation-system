from pydantic import BaseModel
from typing import List, Dict, Any

class SimilarProductResponse(BaseModel):
    """
    A model representing the details of a similar product.

    Attributes:
        similar_uniq_id (str): The unique identifier of the similar product.
        similar_product_name (str): The name of the similar product.
        brand (List[str]): A list of brands associated with the similar product.
        colour (List[str]): A list of colours available for the similar product.
        rating (str): The rating of the similar product.
        medium (str): A URL to images of the similar product.
        sales_price (str): The sales price of the similar product.
        similarity (float): The similarity score between the selected product and the similar product.
    """
    similar_uniq_id: str
    similar_product_name: str
    brand: List[str]
    colour: List[str]
    rating: str
    medium: str
    sales_price: str
    similarity: float

class SearchResponse(BaseModel):
    """
    A model representing the response structure for a product similarity search.

    Attributes:
        selected_product (Dict[str, Any]): A dictionary containing details of the selected product.
        similar_products (List[SimilarProductResponse]): A list of similar products with their details.
    """
    selected_product: Dict[str, Any]
    similar_products: List[SimilarProductResponse]