import streamlit as st

from embeddings import  answer_with_deep_lake


def Recomendations():
    st.title("Recomendations Chatbot")


    query = "From the event data, create a summary that highlights the most frequent types of events, their timing, and any notable characteristics. Based on this summary, suggest some recommendations for optimizing future event planning."
    result = (answer_with_deep_lake(query))
    st.markdown(f"<div style='text-align: left; color: green;'>**Bot:** {result}</div>", unsafe_allow_html=True)

if __name__ == "__main__":

    Recomendations()


if __name__ == "__main__":
    
    Recomendations()

