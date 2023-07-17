# from st_pages import Page, show_pages

# from chatbot_page import chatbot_page
# from create_event_page import create_event_page
# from Recomendations import Recomendations

# if __name__ == "__main__":
#     # Declare the pages

#     chatbot_page = Page("C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/chatbot_page.py", "Chatbot", "💬")
#     Recomendations = Page("C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/Recomendations.py", "Recomendations", "🧾")
#     create_event_page = Page("C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/create_event_page.py", "Create Event", "📅")

#     # Show the pages in the sidebar
#     show_pages([
#         chatbot_page,
#         create_event_page,
#         Recomendations,
#     ])

import streamlit as st
from chatbot_page import chatbot_page
from create_event_page import create_event_page
from Recomendations import Recomendations

def intro():
    import streamlit as st

    st.write("# Welcome to Macro! 👋")
    st.sidebar.success("Select a Action")

    st.markdown(
        """
        Marco is a comprehensive event management platform designed primarily for travelers. It serves as a one-stop database for discovering, booking, and even hosting events. Whether you're a tourist exploring a new city or a local looking to uncover hidden gems, Marco has you covered. Our platform offers a list of diverse events and provides reservation and booking services. Additionally, event organizers can take advantage of Marco's 
        promotional services to boost their event's visibility, regardless of its location.

        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Marco can do!

       
    """
    )


page_names_to_funcs = {
    "—": intro,
    "ChatBot": chatbot_page,
    "Recomendation": Recomendations,
    "Event Creation": create_event_page
}

demo_name = st.sidebar.selectbox("Choose a Action", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()