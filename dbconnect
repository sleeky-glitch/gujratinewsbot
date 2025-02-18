import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB connection details
MONGO_URI = "mongodb+srv://a8T5wYHiQp0EuNpa:aieworldsportso2o@cluster0.mongodb.net/news_data?retryWrites=true&w=majority"
DB_NAME = "news_data"
COLLECTION1 = "dd_news_articles"
COLLECTION2 = "gujarat_samachar_articles"

# Connect to MongoDB
@st.cache_resource
def connect_to_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    return db

# Fetch data from a collection
def fetch_data(collection_name):
    db = connect_to_mongo()
    collection = db[collection_name]
    data = list(collection.find())
    return pd.DataFrame(data)

# Streamlit app
st.title("MongoDB Data Viewer")

# Sidebar for collection selection
st.sidebar.title("Select Collection")
collection_option = st.sidebar.selectbox(
    "Choose a collection to display:",
    [COLLECTION1, COLLECTION2]
)

# Display data
if collection_option:
    st.write(f"Displaying data from collection: **{collection_option}**")
    data = fetch_data(collection_option)
    if not data.empty:
        st.dataframe(data)
    else:
        st.write("No data found in the selected collection.")

# Instructions for hosting on GitHub Cloud
st.sidebar.title("Hosting Instructions")
st.sidebar.write("""
1. Save this script as `app.py`.
2. Create a `requirements.txt` file with the following content:
   ```
   streamlit
   pymongo
   pandas
   ```
3. Push the files to a GitHub repository.
4. Deploy the app on [Streamlit Cloud](https://streamlit.io/cloud).
""")
