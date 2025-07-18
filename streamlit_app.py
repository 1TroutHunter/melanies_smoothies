# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(f" :cup_with_straw: Customize Your Smoothie :cup_with_straw: ")
st.write(" Choose the fruits you want in your custom smoothie!")
#import streamlit as st

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be', name_on_order)
#from snowflake.snowpark.functions import col

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
, my_dataframe
, max_selections=5    
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

 #   st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order + """')"""

st.write(my_insert_stmt)
#st.stop()
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

#import requests
#smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
#sf_df = st.dataframe(data=smoothiefroot_response, use_container_width=True)

import requests
import streamlit as st
import pandas as pd

# Make the API call
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")

# Check if it's valid JSON
try:
    smoothiefroot_response.raise_for_status()
    data = smoothiefroot_response.json()

    # If the data is a single object (dict), put it in a list
    if isinstance(data, dict):
        data = [data]

    # Convert to DataFrame and show
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

except requests.exceptions.RequestException as e:
    st.error(f"API request failed: {e}")

except ValueError:
    st.error("Response is not valid JSON.")
    st.text(smoothiefroot_response.text)












