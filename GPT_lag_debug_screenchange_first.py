from dotenv import load_dotenv
import os
import openai
import streamlit as st
import time

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

# Initialize session state variables
if 'screen' not in st.session_state:
    st.session_state.screen = 'initial'
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'loading' not in st.session_state:
    st.session_state.loading = False

# Function to start conversation
def start_conversation():
    st.session_state.screen = 'conversation'
    st.session_state.loading = True
    st.session_state.user_input = st.session_state['user_input']
    st.rerun()  # Force UI to update and show loading spinner

# Function to get GPT-4 response
def get_gpt4_response(prompt):
    api_start_time = time.time()
    response = openai.Completion.create(
        model="gpt-4o",
        prompt=prompt,
        max_tokens=150
    )
    api_end_time = time.time()
    print(f"Time taken for API call: {api_end_time - api_start_time:.2f} seconds")
    return response.choices[0].text.strip()

# Define the layout for the initial screen
def initial_screen():
    render_start_time = time.time()
    st.markdown("<h1 style='color: purple; text-align: center;'>Hi, I'm your Insurance Portal Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Ask me any insurance related question</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    card_html = """
    <div style="position: relative; text-align: center; color: white; margin-bottom: 20px; height: 250px;">
      <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px;">
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.7); padding: 10px; border-radius: 10px; width: 90%; max-width: 200px; text-shadow: 1px 1px 2px black;">
        <h4 style="margin: 0; font-size: 16px; color: white;">{caption}</h4>
      </div>
    </div>
    """

    with col1:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="Can you explain the difference between Term and Permanent Life Insurance?"), unsafe_allow_html=True)

    with col2:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="Does Auto Insurance cover my driving a rental car?"), unsafe_allow_html=True)

    with col3:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="What actually does Pet Insurance insure?"), unsafe_allow_html=True)

    with col4:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="Is Condo Insurance the same as Homeowner's Insurance?"), unsafe_allow_html=True)

    # Add vertical space after the columns
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Input area with placeholder and hidden label
    user_input = st.text_input("Your question", key="user_input", placeholder="Ask your question here", label="Enter your question", label_visibility="collapsed", on_change=start_conversation)
    render_end_time = time.time()
    print(f"Time taken to render initial screen: {render_end_time - render_start_time:.2f} seconds")

# Define the layout for the conversation screen
def conversation_screen():
    render_start_time = time.time()
    st.markdown('<div class="title-container"><h1 style="font-size: 24px; text-align: left; margin-left: 20px;">Insurance Portal Chatbot</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)


    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.markdown('</div>', unsafe_allow_html=True)

    input_placeholder = st.empty(label="")
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    
    if st.session_state.loading:
        st.markdown('<div style="text-align: center;"><span>Loading...</span></div>', unsafe_allow_html=True)
        user_input = st.session_state.user_input
        response = get_gpt4_response(user_input)
        st.session_state.conversation.append({"role": "assistant", "content": response})
        st.session_state.loading = False
        st.experimental_rerun()
    else:
        if prompt := input_placeholder.chat_input("Ask your questions here:", label="Enter your question", label_visibility="collapsed"):
            st.session_state.conversation.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = get_gpt4_response(prompt)
                st.markdown(response)
            st.session_state.conversation.append({"role": "assistant", "content": response})
    
    st.markdown('</div>', unsafe_allow_html=True)
    print(f"Time taken to render conversation screen: {render_end_time - render_start_time:.2f} seconds")

# Main function to manage the screen state
def main():
    # CSS styles to fix the title, input bar, and footer
    st.markdown(
        """
        <style>
        .title-container {
            position: fixed;
            top: 40px;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 10px 20px;
            text-align: left;
            z-index: 1001;  /* Higher than other elements */
            font-size: 24px;
        }

        .input-container {
            position: fixed;
            bottom: 50px;  /* Adjusted to create space for the disclaimer */
            left: 0;
            width: 100%;
            padding: 0;  /* Adjust padding to fit the input area */
            background-color: white;
            z-index: 1000;  /* Ensures it is above other elements but below the title */
        }

        .input-area {
            padding: 20px;  /* Add padding directly to the input area */
        }

        .disclaimer {
            position: fixed;
            bottom: 0px;  /* Positioned at the bottom of the screen */
            left: 0;
            width: 100%;
            text-align: center;
            background-color: white;
            padding: 10px;
            font-size: smaller;
            color: gray;
            z-index: 999;  /* Ensures it is above other elements but below the input container */
        }

        .chat-container {
            margin-top: 120px;  /* Adjust to leave space for the fixed title */
            margin-bottom: 150px;  /* Adjust to leave space for the fixed input bar and disclaimer */
            overflow-y: auto;
            max-height: calc(100vh - 270px);  /* Adjust this value to control the height of the scrollable chat area */
            padding: 0 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    if st.session_state.screen == 'initial':
        initial_screen()
    elif st.session_state.screen == 'conversation':
        conversation_screen()

    # Footer note
    st.markdown(
        """
        <div class="disclaimer">
            <small>Insurance Portal may display inaccurate info, so double-check important info.</small>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
