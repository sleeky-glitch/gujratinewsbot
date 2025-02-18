import streamlit as st
from pinecone import Pinecone
import openai
import datetime
from googletrans import Translator
import pandas as pd

# Check for API keys in secrets
if 'api_keys' not in st.secrets:
    st.error("API keys not found in secrets!")
    st.stop()

# Initialize OpenAI
openai_client = OpenAI(api_key=st.secrets["api_keys"]["openai"])

# Initialize Pinecone
pc = Pinecone(api_key=st.secrets["api_keys"]["pinecone"])
index = pc.Index("news-articles-18-02")

# Initialize translator
translator = Translator()

def get_embedding(text):
    """Get embedding for a text using OpenAI API"""
    try:
        response = openai_client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        return response.data[0].embedding
    except Exception as e:
        st.error(f"Error getting embedding: {e}")
        return None

def translate_to_english(text):
    """Translate text to English if it's in Gujarati"""
    try:
        detected = translator.detect(text)
        if detected.lang != 'en':
            return translator.translate(text, dest='en').text
        return text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

def translate_to_gujarati(text):
    """Translate text to Gujarati"""
    try:
        return translator.translate(text, dest='gu').text
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text

def search_news(query, top_k=5):
    """Search news articles using the query"""
    # Translate query to English if it's in Gujarati
    english_query = translate_to_english(query)

    # Get embedding for the query
    query_embedding = get_embedding(english_query)
    if query_embedding is None:
        return []

    # Search in Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    return results.matches

def format_results(results):
    """Format search results for display"""
    formatted_results = []
    for result in results:
        metadata = result.metadata
        formatted_result = {
            'Title': metadata['title'],
            'Date': metadata['date'],
            'Source': metadata['collection'],
            'Link': metadata['link'],
            'Score': result.score
        }
        formatted_results.append(formatted_result)
    return formatted_results

def main():
    st.title("Bilingual News Bot 📰")
    st.write("Ask questions about news in English or ગુજરાતી")

    # Add a sidebar with information
    with st.sidebar:
        st.header("About")
        st.write("This news bot can search through articles in English and Gujarati.")
        st.write("You can ask questions like:")
        st.write("- What happened in cricket in the last 10 days?")
        st.write("- છેલ્લા 10 દિવસમાં ક્રિકેટમાં શું થયું?")
        st.write("- Latest news about Gujarat")
        st.write("- ગુજરાતના તાજા સમાચાર")

    # Query input
    query = st.text_input(
        "Enter your question:",
        placeholder="What happened in cricket in the last 10 days? / છેલ્લા 10 દિવસમાં ક્રિકેટમાં શું થયું?"
    )

    if query:
        with st.spinner('Searching for relevant news...'):
            # Search for news
            results = search_news(query)

            if results:
                # Format and display results
                formatted_results = format_results(results)
                df = pd.DataFrame(formatted_results)

                # Display results
                st.subheader("Search Results:")
                for idx, row in df.iterrows():
                    with st.expander(f"{idx + 1}. {row['Title']}"):
                        col1, col2 = st.columns([3, 1])

                        with col1:
                            st.write(f"**Date:** {row['Date']}")
                            st.write(f"**Source:** {row['Source']}")
                            st.write(f"**Relevance Score:** {row['Score']:.2f}")
                            st.write(f"**Link:** [{row['Link']}]({row['Link']})")

                        with col2:
                            if st.button(f"Translate", key=f"trans_{idx}"):
                                if any(ord(c) > 127 for c in row['Title']):
                                    translated = translate_to_english(row['Title'])
                                    st.write("🇺🇸 English:")
                                else:
                                    translated = translate_to_gujarati(row['Title'])
                                    st.write("🇮🇳 ગુજરાતી:")
                                st.write(translated)
            else:
                st.warning("No relevant news found for your query.")

if __name__ == "__main__":
    main()

# Created/Modified files during execution:
# No files are created or modified - this is a Streamlit web application
