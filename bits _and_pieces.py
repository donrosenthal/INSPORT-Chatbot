import streamlit as st

# # Title of the app
# st.title("Simple Streamlit App")

# # Get user input
# user_input = st.text_input("Enter some text:")

# # Display the user input
# if user_input:
#     st.write("You entered:", user_input)


import streamlit as st

st.set_page_config(page_title="Calculator App")

st.title("Simple Calculator")

num1 = st.number_input("Enter the first number:", min_value=0.0, step=0.1)
num2 = st.number_input("Enter the second number:", min_value=0.0, step=0.1)

result = num1 + num2
st.write(f"The sum of {num1} and {num2} is {result}")

