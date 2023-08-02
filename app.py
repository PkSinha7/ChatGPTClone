from PIL import Image
from streamlit_chat import message
import streamlit as st
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory,
                                                  ConversationSummaryMemory,
                                                  ConversationBufferWindowMemory
                                                  )

# load_dotenv()

# UI

if 'conversation' not in st.session_state:
    st.session_state['conversation'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] = ''

im = Image.open("web-cam.ico")
im2 = Image.open("web-cam.png")
st.set_page_config(page_title="Your Personal Assistant", page_icon=im, layout="wide")

st.markdown("<h1 style='text-align: center;'> How may I help you? </h1>", unsafe_allow_html=True)
st.sidebar.image(im2, width=60)

tabs_font_css = """
<style>
div[class*="stTextInput"] label p {
  font-size: 26px;
  font-style: italic; 
  font-family: cursive; 
  color: white;
}
</style>
"""

st.write(tabs_font_css, unsafe_allow_html=True)

st.session_state['API_Key'] = st.sidebar.text_input("Enter Your API Key", type='password')

summarise_button = st.sidebar.button("Summarise the conversation", key="summarise")
if summarise_button:
    summarise_placeholder = st.sidebar.write("Here is the summary of our conversation:" + st.session_state['conversation'].memory.buffer)


def getResponse(userInput, api_key):
    if st.session_state['conversation'] is None:
        llm = OpenAI(
            temperature=0,
            openai_api_key=api_key,
            model_name='text-davinci-003'
        )

        st.session_state['conversation'] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm)
        )

    response = st.session_state['conversation'].predict(input=userInput)
    print(st.session_state['conversation'].memory.buffer)

    return response


response_container = st.container()
container = st.container()

with container:
    with st.form(key='my_form', clear_on_submit=True):
        user_input = st.text_area("Your question goes here:", key='input', height=100)
        submit_button = st.form_submit_button(label='Send')

        if submit_button:
            st.session_state['messages'].append(user_input)
            model_response = getResponse(user_input, st.session_state['API_Key'])
            st.session_state['messages'].append(model_response)

            with response_container:
                for i in range(len(st.session_state['messages'])):
                    if (i % 2) == 0:
                        message(st.session_state['messages'][i], is_user=True, key=str(i) + '_user')
                    else:
                        message(st.session_state['messages'][i], key=str(i) + '_AI')
