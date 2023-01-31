import streamlit
import pandas as pd
import requests

## fuit list
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index("Fruit")

## app components
streamlit.title("My parents new healty diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avovado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado", "Banana"])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

# Get fruits from fruitvice.com API
streamlit.header("Fruityvice Fruit Advice!")
fruit_choice = streamlit.text_input("What fruit would you like information about?","kiwi")
streamlit.text("The user selected "+ fruit_choice) 
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

## normalize json response
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())

## output to screen
streamlit.dataframe(fruityvice_normalized)

