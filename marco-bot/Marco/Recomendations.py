import streamlit as st

from embeddings import RecommendationChain


def Recomendations():
    st.title("Recomendations Chatbot")
    st.write("Welcome to Marco Recomendation Centre")

    query = "From the event data, create a summary that highlights the most frequent types of events, their timing, and any notable characteristics and descriptions. Based on this summary, suggest some event types recommendations for users for which they are morelikely to adapt to.."
    with st.spinner('processing Results.Please wait...'):
        result = (RecommendationChain(query))
        st.write(result)
        # st.markdown(f"<div style='text-align: left; color: green;'>**Bot:** {result}</div>", unsafe_allow_html=True)
        st.success('Done!')
if __name__ == "__main__":
    
    Recomendations()



