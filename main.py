
import streamlit as st
import pandas as pd
import numpy as np

st.write("hello World")

foodItem = st.text_input("Enter Food Type")
st.write("Your chosen food item", foodItem)

myDict = {1: "one", 2: "two", 3: "three", 4: "four"}

optionsList = list(myDict.values())

option = st.selectbox(
    'What option would you like?',
    optionsList)

selected_key = next(key for key, value in myDict.items() if value == option)

st.write('You selected Series ID:', option)
st.write("You selected Food Item: ", myDict.get(option, "Not found"))

st.image('testing.png', caption="testing stuff")


