import logging
from fastapi import APIRouter, HTTPException, Query
from app.model.models import SearchResponse
from ..utils.similarity_helper import find_similar_products_by_uniq_id
from ..utils.qdrant_helper import search_similar_products
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/find_similar_products", response_model=SearchResponse)
def get_similar_products(product_id: str = Query(..., alias="product_id", description="The unique identifier of the product."),
                         num_similar: int = Query(..., ge=1, le=60, description="The number of similar products to retrieve (between 1 and 60).")):
    """
    Fetches similar products based on the provided product ID.

    Args:
        product_id (str): The unique identifier of the product for which to find similar products.
        num_similar (int): The number of similar products to retrieve. Must be between 1 and 60.

    Returns:
        SearchResponse: A dictionary containing details of the selected product and a list of similar products.

    Raises:
        HTTPException: If the product ID is not found or an internal server error occurs.
    """
    try:
        if not product_id or num_similar <= 0:
            logger.error(f"Invalid input parameters: product_id={product_id}, num_similar={num_similar}")
            raise HTTPException(status_code=400, detail="Invalid input parameters.")

        logger.info(f"Fetching similar products for product_id: {product_id} with num_similar: {num_similar}")
        response = search_similar_products(product_id, num_similar)

        if not response:
            logger.warning(f"No similar products found for product_id: {product_id}")
            raise HTTPException(status_code=404, detail="No similar products found.")

        json_compatible_item_data = jsonable_encoder(response)
        return JSONResponse(content=json_compatible_item_data)

    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.error(f"Unhandled Exception: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error.")


# @router.get("/find_similar_products")
# def get_similar_products(product_id: str, num_similar: int):
#     similar_products = find_similar_products_by_uniq_id(product_id, num_similar)
#     json_compatible_item_data = jsonable_encoder(similar_products)
#     return JSONResponse(content=json_compatible_item_data)
    # try:
    #     similar_products = find_similar_products_by_uniq_id(product_id, num_similar)
    #     return similar_products
    # except HTTPException as e:
    #     raise e
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))
