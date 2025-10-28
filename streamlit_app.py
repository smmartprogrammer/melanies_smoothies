from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import streamlit as st
import requests
import pandas as pd


# Set app title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("""
**Choose the fruits you want in your custom smoothie!**
""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Create Snowflake session using Streamlit secrets (stored under [connections.snowflake])
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

session = create_session()

# Existing Snowpark DataFrame
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(
    col("FRUIT_NAME"),
    col("SEARCH_ON")
)

# Convert Snowpark DataFrame to pandas DataFrame
pd_df = my_dataframe.to_pandas()

# Display pandas DataFrame in Streamlit
st.dataframe(data=pd_df, use_container_width=True)

# Display multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ' '

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders(ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
    """


#st.text(smoothiefroot_response.json())


time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
