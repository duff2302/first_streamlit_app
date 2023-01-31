import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

## create a function to get fruit info from fruityvice api
def get_fruityvice_data(this_fruit_choice):
	fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
   	## normalize json response
	fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
	return fruityvice_normalized

## get fruit load list function
def get_fruit_load_list():
	### Get data from SnowFlake
	with my_cnx.cursor() as my_cur:
		my_cur.execute("SELECT * FROM pc_rivery_db.public.fruit_load_list")
		return my_cur.fetchall()	

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
try:
	fruit_choice = streamlit.text_input("What fruit would you like information about?","kiwi")
	if not fruit_choice:
    		streamlit.error("Please select a fruit to get information.")
	else:
    		back_from_api = get_fruityvice_data(fruit_choice)
    		## output to screen
    		streamlit.dataframe(back_from_api)

except URLError as e:
	streamlit.error()



streamlit.header("The fruit load list contains : ")
## Button to load fruit load list
if streamlit.button("Get Fruit Load List'):
	my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
	fruit_load_list_data = get_fruit_load_list()
	streamlit.dataframe(fruit_load_list_data)

streamlit.stop()
# ask what fruit to add to list
add_my_fruit = streamlit.text_input("What fruit would you like to add?","kiwi")
streamlit.text("Thanks for adding "+ add_my_fruit)

my_cur.execute("INSERT INTO PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST VALUES ('from streamlit')")
