
import streamlit as st
import pandas as pd
import numpy as np

foodItem = st.text_input("Enter Food Type")
st.write("Your chosen food item", foodItem)

myDict = {1: "one", 2: "two", 3: "three", 4: "four"}

optionsList = list(myDict.keys())

option = st.selectbox(
    'What option would you like?',
    optionsList)

st.write('You selected Series ID:', option)
st.write("You selected Food Item: ", myDict.get(option, "Not found"))

st.image('testing.png', caption="testing stuff")


