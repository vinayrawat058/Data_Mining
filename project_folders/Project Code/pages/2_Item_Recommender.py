import streamlit as st

st.title("Item Recommender 🛍️")

# Input for dataset upload
uploaded_file = st.file_uploader("Upload your dataset (CSV format):", type="csv")
if uploaded_file:
    import pandas as pd
    data = pd.read_csv(uploaded_file)
    st.write("Dataset Preview:")
    st.write(data.head())

    # Example recommender system
    user_input = st.text_input("Enter an item or keyword:")
    if user_input:
        # Simple keyword-based recommender
        recommended_items = data[data.apply(lambda row: user_input.lower() in row.to_string().lower(), axis=1)]
        st.write("Recommended Items:")
        st.write(recommended_items.head())
