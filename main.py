import streamlit as st
import pandas as pd
from db import DBSelecter

db_obj = DBSelecter("films.db")
# Заголовок страницы
st.title('Поиск фильмов')

# Опции фильтров
min_year = db_obj.fetch_one("SELECT MIN(Year) FROM Films", int)
max_year = db_obj.fetch_one("SELECT MAX(Year) FROM Films", int)

# Виджеты для фильтров
with st.sidebar:
    st.write("## Фильтры")
    use_filters = st.checkbox('Использовать фильтры')
    if use_filters:
        year_range = st.slider('Выберите год выпуска фильма', min_year, max_year, (min_year, max_year))
        min_rating = st.slider('Минимальный рейтинг', 0.0, 10.0, 0.0)
        max_rating = st.slider('Максимальный рейтинг', 0.0, 10.0, 10.0)

# Фильтрация данных
filtered_data = db_obj.select("SELECT * FROM Films")

# Применение фильтров, если галочка активирована
if use_filters:
    filtered_data = db_obj.select(f"SELECT * FROM Films WHERE (Year BETWEEN {year_range[0]} AND {year_range[1]}) AND Rating BETWEEN {min_rating} AND {max_rating}")

# Поиск по заголовку
search_query = st.text_input('Поиск по названию фильма')

# Применение поиска
if search_query:
    filtered_data = filtered_data[filtered_data['Title'].str.contains(search_query, case=False)]

# Отображение результатов
if len(filtered_data) == 1:
    st.subheader(filtered_data.iloc[0]['Title'])
    st.write(f"Год выпуска: {filtered_data.iloc[0]['Year']}")
    st.write(f"Рейтинг: {filtered_data.iloc[0]['Rating']}")
    st.text_area("Описание", filtered_data.iloc[0]['Summary'])

    y_video = filtered_data.iloc[0]["YouTube Trailer"]
    if y_video:
        st.video(f"https://www.youtube.com/watch?v={y_video}")
else:
    st.write(filtered_data)
