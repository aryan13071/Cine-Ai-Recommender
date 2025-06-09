# 🎬 Cine AI Recommender

An interactive movie recommendation web app built using Streamlit that suggests the top 5 similar movies based on user input.

## 🔧 Features
- Developed using **Streamlit** for an intuitive and responsive UI.
- **Content-based filtering** using TF-IDF/CountVectorizer to vectorize metadata tags.
- **Cosine similarity** to identify and recommend similar movies.
- Dynamic fetching of **movie posters** using the OMDb API.
- Clean, grid-style result display using `st.columns` in a 5-column format.
- Robust **data preprocessing and cleaning** pipeline.

## 📸 Demo
(Add a screenshot or GIF here)

## 🚀 How to Run
1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## 🌐 API Used
- [OMDb API](http://www.omdbapi.com/)

## 📁 Dataset
- Movie metadata from TMDb/Kaggle (mention the source)

## 🧠 Techniques Used
- TF-IDF, CountVectorizer, Cosine Similarity

## 🛠️ Tech Stack
- Python
- Streamlit
- Pandas, Scikit-learn
