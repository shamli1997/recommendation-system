import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from utils.similarity_helper import load_pkl_file
import os

filepath = os.path.join(os.path.dirname(__file__), 'data/qdrant_data.pkl')

# Load the DataFrame from the pickle file
df = load_pkl_file(filepath)

print(df.iloc[0]["product_name"])
# Streamlit app layout
st.title("Product Similarity Search")

# Set the default product index
default_product_index = 8
# Dropdown for product selection with default product index
product_name = st.selectbox("Select a Product", df['product_name'], index=default_product_index)
num_similar = st.selectbox("Number of Similar Products", [5, 10, 15, 20, 25, 30, 35, 40, 50, 55, 60])


# Get the uniq_id for the selected product_name
uniq_id = df[df['product_name'] == product_name]['uniq_id'].values[0]

# Make a request to the FastAPI endpoint
try:
    response = requests.get(f"http://fastapi:8000/find_similar_products?product_id={uniq_id}&num_similar={num_similar}")
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    selected_product = data['selected_product']
    similar_products = data['similar_products']

    st.write("Selected Product Details")
    c1, c2, c3 = st.columns(3)
    with c1:
        if 'medium' in selected_product and selected_product['medium']:
            image_url = selected_product['medium'].split('|')[0]
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image)
    with c2:
        st.text('Product Name:')
        st.text('Brand:')
        st.text('Colour:')
        st.text('Rating:')
        st.text('Price:')
    with c3:
        st.text(selected_product['product_name'])
        st.text(", ".join(selected_product['brand']))
        st.text(", ".join(selected_product['colour']))
        rating = f"{selected_product['rating']} ⭐" 
        st.text(rating)
        price = f"₹ {selected_product['sales_price']}"
        st.text(price)

    st.success('Here are the recommendations!!')

    for i in range(0, len(similar_products), 5):
        cols = st.columns(5)
        for col, product in zip(cols, similar_products[i:i+5]):
            with col:
                if 'medium' in product and product['medium']:
                    image_url = product['medium'].split('|')[0]
                    response = requests.get(image_url)
                    image = Image.open(BytesIO(response.content))
                    st.image(image)
                st.text(product['similar_product_name'])
                st.text(", ".join(product['brand']))
                st.text(", ".join(product['colour']))
                price = f"₹ {product['sales_price']}"
                st.text(price)
                rating = product['rating'] + ' ⭐'
                st.text(rating)
                



except requests.exceptions.HTTPError as http_err:
    st.error(f"HTTP error occurred: {http_err}")
except requests.exceptions.RequestException as req_err:
    st.error(f"Request error occurred: {req_err}")
except Exception as err:
    st.error(f"An error occurred: {err}")


# Hide Streamlit style
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer: {
                visibility: visible;
                display: block;
                position: relative;
                padding: 5px;
                top: 2px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
