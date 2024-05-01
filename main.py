
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

foodItem = st.text_input("Enter Food Type")

myDict = {1: "one", 2: "two", 3: "three", 4: "four"}

optionsList = list(myDict.keys())

option = st.selectbox(
    'How would you like to be contacted?',
    optionsList)

st.write('You selected Series ID:', option)
st.write("You selected Food Item: ", myDict.get(option, "Not found"))

st.image('testing.png', caption="testing stuff")

fig = plt.figure() 
plt.plot([1, 2, 3, 4, 5]) 

st.pyplot(fig)

import sys
print(sys.path)
