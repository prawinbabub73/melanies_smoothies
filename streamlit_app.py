# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)


import streamlit as st

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie wil be", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()


ingredient_list = st.multiselect('choose upto 5 ingredients:',my_dataframe,max_selections=5)
if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredient_string=''
    for fruit_chosen in ingredient_list:
        ingredient_string+=fruit_chosen+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen +' Nutrition information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        #st.text(fruityvice_response.json())
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    #st.write(ingredient_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_string + """','"""+name_on_order+"""')"""

    st.write(my_insert_stmt)
    time_to_insert= st.button('Submit your order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('your smoothie is ordered!',icon='✅')
    #if ingredient_string:
        #session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")

