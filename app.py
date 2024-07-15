import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Function to compute TF-IDF and cosine similarity
def compute_similarity(df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['name'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# Function to get product recommendations
def get_recommendations(product_id, df, cosine_sim):
    idx = df.index[df['id'] == product_id].tolist()[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]  # Get top 5 similar products
    product_indices = [i[0] for i in sim_scores]
    return df.iloc[product_indices]

# Streamlit UI
def main():
    st.title("Myntra Product Recommendation System")

    # Load data from CSV file
    csv_file = r'C:\Users\91989\Downloads\archive(1)\small.csv'  # Replace with your CSV file path
    df = pd.read_csv(csv_file)

    # Compute TF-IDF and cosine similarity
    cosine_sim = compute_similarity(df)

    product_id = st.number_input("Enter Product ID", min_value=1, max_value=len(df), step=1)
    if st.button("Get Recommendations"):
        recommendations = get_recommendations(product_id, df, cosine_sim)
        st.write("Top 5 similar products:")
        for index, row in recommendations.iterrows():
            st.write(f"Name: {row['name']}")
            st.write("---")

if __name__ == "__main__":
    main()
