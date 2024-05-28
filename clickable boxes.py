from dotenv import load_dotenv
import os

load_dotenv()

openai_key = os.getenv("OPENAI_KEY")

import streamlit as st
from openai import OpenAI


# Initialize session state variables
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
    st.session_state.conversation = []

def start_conversation():
    st.session_state.conversation_started = True

def copy_text_to_input(text):
    st.session_state.prompt_input = text

# Define the layout for the initial screen
def initial_screen():
    st.markdown("<h1 style='color: purple; text-align: center;'>Hi, I'm your Insurance Portal Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Ask me any insurance related question</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    card_html = """
    <div style="position: relative; text-align: center; color: white; margin-bottom: 20px; height: 250px;">
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.7); padding: 10px; border-radius: 10px; width: 90%; max-width: 200px; text-shadow: 1px 1px 2px black;">
        <h4 style="margin: 0; font-size: 16px; color: white;">{caption}</h4>
      </div>
    </div>
    """

    with col1:
        card_text = "Can you explain the difference between Term and Permanent Life Insurance?"
        st.button(card_text, key="card1", on_click=copy_text_to_input, args=(card_text,))

    with col2:
        card_text = "Does Auto Insurance cover my driving a rental car?"
        st.button(card_text, key="card2", on_click=copy_text_to_input, args=(card_text,))

    with col3:
        card_text = "What actually does Pet Insurance insure?"
        st.button(card_text, key="card3", on_click=copy_text_to_input, args=(card_text,))

    with col4:
        card_text = "Is Condo Insurance the same as Homeowner's Insurance?"
        st.button(card_text, key="card4", on_click=copy_text_to_input, args=(card_text,))

    # Add vertical space after the columns
    st.markdown("<br><br><br>", unsafe_allow_html=True)

# Define the layout for the conversation screen
def conversation_screen():
    st.markdown("<h2>Conversation</h2>", unsafe_allow_html=True)
    for entry in st.session_state.conversation:
        if entry['type'] == 'user':
            st.markdown(f"**User:** {entry['text']}")
        else:
            st.markdown(f"**Bot:** {entry['text']}")

# Handle the prompt input and conversation logic
if st.session_state.conversation_started:
    conversation_screen()
    user_input = st.text_input(label="Enter your prompt", key="prompt_input", placeholder="Ask your question here")

    if user_input:
        st.session_state.conversation.append({"type": "user", "text": user_input})
        # Placeholder for bot response; replace with your bot interaction logic
        bot_response = "This is a response from the bot."
        st.session_state.conversation.append({"type": "bot", "text": bot_response})
else:
    initial_screen()
    # Add CSS styling for the input box
    st.markdown("""
        <style>
        .stTextInput > div > input {
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            width: 100%;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)
    # above was the added CSS styling
    user_input = st.text_input("Enter a prompt here", 
    on_change=start_conversation, placeholder="Ask your question here")

st.markdown(
    """
    <script>
        function copy_text_to_input(text) {
            document.querySelector('input#prompt_input').value = text;
        }
    </script>
    """,
    unsafe_allow_html=True,
)
# Footer note
st.markdown("<small>Insurance Portal may display inaccurate info. Please double-check important info.</small>", unsafe_allow_html=True)
