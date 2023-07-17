import datetime

from SqlRunner import get_sql_result
import streamlit as st
from summarisation import answer_question_from_document
import streamlit as st
import time

from Utils import create_folder, load_conversation, save_conversation

def chatbot_page():
    st.title("Marco Chatbot")
    st.write("Marco is a comprehensive event management platform designed primarily for travelers. It serves as a one-stop database for discovering, booking, and even hosting events. Whether you're a tourist exploring a new city or a local looking to uncover hidden gems, Marco has you covered. Our platform offers a list of diverse events and provides reservation and booking services. Additionally, event organizers can take advantage of Marco's promotional services to boost their event's visibility, regardless of its location.")
    st.write("Simple prompts a user can ask the bot")

    user_input = st.text_input("Wlecome to MarcoBot. Type your message:")
    create_folder()
    conversation = load_conversation()

    if st.button("Send"):
        try:
            with st.spinner('processing Results.Please wait...'):
                SQLresult = get_sql_result(user_input)

                result = answer_question_from_document(SQLresult)
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
                st.success('Done!')

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    chatbot_page()
