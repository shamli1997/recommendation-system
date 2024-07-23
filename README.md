# Product Recommendation System

## Project Overview

This project is a product recommendation system designed to retrieve and display similar products based on a given product’s unique ID (`uniq_id`). The system uses various methods for similarity calculation, including basic vectorization, advanced NLP embeddings, and optimized vector searches using Qdrant.

## Video Walkthrough

Here's a walkthrough of implemented features:

<img src='https://github.com/shamli1997/recommendation-system/blob/main/precommendation_demo.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

## Approaches

## Data Preprocessing

Selected columns for recommendations:

- `uniq_id`: Unique identifier for each product.
- `product_name`: Name of the product, useful for textual similarity.
- `tags`: Merged column including brand, color, and meta keywords.

Combining these attributes into a single 'tags' column creates a comprehensive representation of each product, enhancing the system's ability to find better matches and provide relevant recommendations.

### 1. Basic Version with Sklearn

The first approach involves preprocessing the dataset and vectorizing product attributes using `CountVectorizer`. Cosine similarity is then calculated between these vectors to find the most similar products. This method provides a basic understanding of similarity calculation using simple vector representations.

#### Limitations:

- Limited semantic understanding.
- Sparse vectors might not capture complex relationships between words effectively.

### 2. Enhanced Version Using Sentence Transformers

The second approach improves upon the first by using the SentenceTransformer model 'all-mpnet-base-v2' to encode product tags into embeddings. This provides more accurate vector representations, and cosine similarity is calculated on these embeddings to identify similar products.

#### Improvements:

- Better semantic understanding.
- Dense embeddings capture complex relationships.

#### Limitations:

- Scalability issues due to computational expense.

### 3. Optimized Version Using Qdrant and Sentence Transformers

The third approach optimizes similarity search by combining SentenceTransformer embeddings with Qdrant, a high-performance vector search engine. This allows for efficient and accurate nearest neighbor searches, making the system scalable for large datasets.

#### Improvements:

- Efficient handling of large datasets.
- Fast and scalable nearest neighbor searches using Qdrant's optimized algorithms.

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Steps to Setup

1. **Clone the Repository**

   ```bash
   git clone https://github.com/shamli1997/recommendation-system.git
   cd Recommendation_system
   ```

2. **Build Docker Images**

   ```bash
   docker-compose build
   ```

3. **Run the Docker Containers**

   ```bash
   docker-compose up
   ```

4. **Access the Applications**

- FastAPI : http://localhost:8000/docs
- Streamlit: http://localhost:8501
