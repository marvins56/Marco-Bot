import datetime

from SqlRunner import get_sql_result
import streamlit as st
from summarisation import answer_question_from_document
import streamlit as st

from Utils import MultiChainRunner
from Utils import create_folder, load_conversation, save_conversation
from Utils import create_folder, load_conversation, save_conversation

def chatbot_page():
    st.title("Marco Chatbot")



def chatbot_page():
    st.title("Macro Chatbot")


    user_input = st.text_input("Type your message:")
    create_folder()
    conversation = load_conversation()

    if st.button("Send"):
        try:

            SQLresult = get_sql_result(user_input)

            result = answer_question_from_document(SQLresult)


            result = MultiChainRunner(user_input)

            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            st.markdown(f"<div style='text-align: left; color: green;'>**Bot:** {result}</div>", unsafe_allow_html=True)
            conversation.append({
                "role": "User",
                "time": current_time,
                "text": user_input
            })
            conversation.append({
                "role": "Bot",
                "time": current_time,
                "text": str(result)
            })
            save_conversation(conversation)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # for message in conversation:
    #     if message['role'] == 'User':
    #         st.markdown(
    #             f"<div style='text-align: right; color: blue;'>**{message['role']} ({message['time']}):** {message['text']}</div>",
    #             unsafe_allow_html=True)
    #     else:
    #         st.markdown(
    #             f"<div style='text-align: left; color: green;'>**{message['role']} ({message['time']}):** {message['text']}</div>",
    #             unsafe_allow_html=True)

if __name__ == "__main__":
    chatbot_page()
