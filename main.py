import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


foodItem = st.text_input("Enter Food Type")

myDict = {1: "one", 2: "two", 3: "three", 4: "four"}

optionsList = list(myDict.keys())


option = st.selectbox(
    'How would you like to be contacted?',
    optionsList)

st.write('You selected Series ID:', option)
st.write("You selected Food Item: ", optionsList[option])


st.imapge('testing.png', caption = "testing stuff")

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
