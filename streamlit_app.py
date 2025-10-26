import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Set app title
st.title(":cup with straw: Customize Your Smoothie!:cup with straw:")

st.write("""
**Choose the fruits you want in your custom smoothie!**
""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('the name on your smoothie will be:', name_on_order)


# Get the active Snowflake session
session = get_active_session()

# Read data from your Snowflake table
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))

# Display the data
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients:'
    ,my_dataframe, max_selections=5 
    
    #my_dataframe
    )

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
      
        st.success('Your Smoothie is ordered!', icon="✅")

