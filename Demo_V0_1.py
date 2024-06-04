
import os
import openai
import streamlit as st

# Load environment variables
openai_key = os.getenv("OPENAI_KEY")


# Initialize OpenAI client
client = openai.OpenAI(api_key=openai_key) # stores the instance of the OpenAI class in client for API calls

# Streamlit is a declaritive programming paradigm, and the script runs once per change in the UI
# Because of this, state does not persist across different runs of the scriot
# To get around this, Streamlit allows the use of a sgle gloabal Python dictionary "session.state", the contents 
# of which are fully controlled by ther code. Essentially, Streamlit requires the use of globally-scoped variables
# wihich can make the code very hard to read, and has all the expected pitfalls of global variables. Welcome back FORTRAN and COBOL :-)

# The following is used to determine if this is the first run through the script
# If so, we use the initial screen (which welcomes the user, etc,)
# If not we use the conversation screen
# Initialize session state variables
if 'screen' not in st.session_state:
    st.session_state.screen = 'initial'
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Function to start conversation
# When a conversation is initiated in the initial screen, this function is called
def start_conversation():
    st.session_state.screen = 'conversation' # First, change the screen state to conversation
    user_input = st.session_state['user_input'] # Then we grab the user's first prompt from "user input" which 
                                                # was set when theorugh a declaration in the initial screen layout (remember,
                                                # we're dealing with a declarative language
    # Define the system pronmpt
    system_message = {"role": "system", "content": "Acting as an expert in U.S. personal insurance, please answer questions from the user in a helpful and supportive way about Life Insurance, Disability Insurance, Long Term Care Insurance, Auto Insurance, Umbrella Insurance, and Homeowners Insurance (including Condo insurance and Renters insurance). If the user asks a question about a different type of insurance, reply that you are not trained to discuss those types of insurance but would be happy to talk to them about Life Insurance, Disability Insurance, Long Term Care Insurance, Auto Insurance, and Homeowner's, Condo, and Renter's Insurance. If the user asks a question outside the realm of personal insurance in the United States, politely answer that you would love to help them, but are only trained to discuss issues and questions regarding personal insurance in the U.S. Users may be quite new to the domain of insurance so it is very important that you are welcoming and helpful, and that answers are complete and correct. Please err on the side of completeness rather than on the side of brevity, and always be truthful and accurate. And this is very important: please let the user know that they should always contact an insurance professional before making any important decisions."}

    # Define the user prompt with content already captured
    st.session_state.conversation = [{"role": "user", "content": user_input}]
    
    # Package the uer prompt and the system prompt, pass it to the LLM to get its response
    response = get_gpt4_response(user_input, system_message)
    
    # in order to enable a multi-turn conversation, append this rurn's messages to the already stored 
    # previous conversation turns so they canbe sent aling with the users next prompt.
    st.session_state.conversation.append({"role": "assistant", "content": response})

# Function to get GPT-4 response
def get_gpt4_response(prompt, system_message):
    response = client.chat.completions.create(     #chat completions is part of the OpenAI API set.
        model="gpt-4o",
        messages=[
            system_message,
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# Define the layout for the initial screen
# This works through the Steamlit UI foundation, but requires a lot of HTML and CSS anyway
# unsafe_allow has to be set to True to allow HTMl and CSS
# This sets up on the intial screen only a title in <h1>, welcome in <h2, four columns to display four prompt suggestions 
# plus the user wwuery input area and a disclaimer
def initial_screen():
    st.markdown("<h1 style='color: purple; text-align: center;'>Hi, I'm your Insurance Portal Chatbot</h1>", unsafe_allow_html=True) 
    st.markdown("<h2 style='text-align: center;'>Ask me any insurance related question</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    card_html = """
    <div style="position: relative; text-align: center; color: white; margin-bottom: 20px; height: 250px;">
         <img src="{img_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 10px;">
      <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background-color: rgba(0, 0, 0, 0.7); padding: 10px; border-radius: 10px; width: 90%; max-width: 200px; text-shadow: 1px 1px 2px black; text-align: center;">
        <h4 style="margin: 0; font-size: 16px; color: white; text-align: center;">{caption}</h4>.
      </div>
    </div>
    """

    with col1:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="Can you explain the difference between Term and Permanent Life Insurance?"), unsafe_allow_html=True)

    with col2:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="Does Auto Insurance cover my driving a rental car?"), unsafe_allow_html=True)

    with col3:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="What does Long Term Care Insurance actually cover?"), unsafe_allow_html=True)

    with col4:
        st.markdown(card_html.format(img_url="https://via.placeholder.com/150", caption="Is Condo Insurance the same as Homeowner's Insurance?"), unsafe_allow_html=True)

    # Add vertical space after the columns
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Input area with placeholder text -- where user will enter their query
    user_input = st.text_input(key="user_input", placeholder="Ask your question here", label=" ", on_change=start_conversation)


# Define the layout for the conversation screen
# Once the conversation has started, replace the intro and welcome <h1?> and <h2> lines, 
# and the four suggestion prompts with a smaller offset title, scolling conversation area, prompt input area
def conversation_screen():
   
    st.markdown('<div class="title-container"><h1 style="font-size: 24px; text-align: left; margin-left: 20px;">Insurance Portal Chatbot</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)

    for message in st.session_state.conversation: 
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    st.markdown('</div>', unsafe_allow_html=True)

    input_placeholder = st.empty()
    st.markdown('<div class="input-area">', unsafe_allow_html=True)
    
    if prompt := input_placeholder.chat_input("Ask your questions here:"):
        st.session_state.conversation.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Acting as an expert in U.S. personal insurance, please answer questions from the user in a helpful and supportive way about Life Insurance, Disability Insurance, Long Term Care Insurance, Auto Insurance, Umbrella Insurance, and Homeowners Insurance (including Condo insurance and Renters insurance). If the user asks a question about a different type of insurance, reply that you are not trained to discuss those types of insurance but would be happy to talk to them about Life Insurance, Disability Insurance, Long Term Care Insurance, Auto Insurance, and Homeowner's, Condo, and Renter's Insurance. If the user asks a question outside the realm of personal insurance in the United States, politely answer that you would love to help them, but are only trained to discuss issues and questions regarding personal insurance in the U.S. Users may be quite new to the domain of insurance so it is very important that you are welcoming and helpful, and that answers are complete and correct. Please err on the side of completeness rather than on the side of brevity, and always be truthful and accurate. And this is very important: please let the user know that they should always contact an insurance professional before making any important decisions."},
                    *st.session_state.conversation
                ],
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.conversation.append({"role": "assistant", "content": response})
    
    st.markdown('</div>', unsafe_allow_html=True)
   

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
