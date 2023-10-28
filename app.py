

import pickle
import streamlit as st
import numpy as np

model = pickle.load(open('artifacts/model.pkl','rb'))
book_names = pickle.load(open('artifacts/book_names.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))

def fetch_poster(suggestion):
    book_name, ids_index, poster_url = [], [], []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])
    
    for name in book_name[0]:
          ids = np.where(final_rating['title'] == name)[0][0]
          ids_index.append(ids)

    for idx in ids_index:
          url = final_rating.iloc[idx]['image_url']
          poster_url.append(url)
    
    return poster_url

def recommend_book(book_name):
    books_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6 )

    poster_url = fetch_poster(suggestion)
    
    for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for book in books:
                books_list.append(book)
    return books_list , poster_url   




st.header('Book Recommender System')
selected_books = st.selectbox("Select a book", book_names)

if st.button('Recommend'):
    recommendation_books, poster_url = recommend_book(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
         st.text(recommendation_books[1])
         st.image(poster_url[1])
    with col2:
         st.text(recommendation_books[2])
         st.image(poster_url[2])
    with col3:
         st.text(recommendation_books[3])
         st.image(poster_url[3])
    with col4:
         st.text(recommendation_books[4])
         st.image(poster_url[4])
    with col5:
         st.text(recommendation_books[5])
         st.image(poster_url[5])


