import streamlit as st
from pymongo import MongoClient
import pandas as pd

# MongoDB connection details
MONGO_URI = "mongodb+srv://aieworldsportso2o:a8T5wYHiQp0EuNpa@cluster0.n3a1w.mongodb.net/news_data?retryWrites=true&w=majority"
DB_NAME = "news_data"
COLLECTION1 = "dd_news_articles"
COLLECTION2 = "gujarat_samachar_articles"

# Connect to MongoDB
@st.cache_resource
def connect_to_mongo():
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        return db
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None

# Fetch data from a collection
def fetch_data(collection_name):
    db = connect_to_mongo()
    if db:
        collection = db[collection_name]
        data = list(collection.find())
        # Convert MongoDB documents to a DataFrame
        df = pd.DataFrame(data)
        if "_id" in df.columns:
            df = df.drop(columns=["_id"])  # Drop the MongoDB ID column for cleaner display
        return df
    else:
        return pd.DataFrame()

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

# Footer
st.sidebar.title("Contact Information")
st.sidebar.write("""
**Beyondata Group**
411-412, Sarthik-II, Opp. Rajpath Club,
Bodakdev, S.G. Highway, Ahmedabad, Gujarat 360054
[www.beyondatagroup.com](http://www.beyondatagroup.com) | info@beyondatagroup.com | 1800 890 6775
""")
