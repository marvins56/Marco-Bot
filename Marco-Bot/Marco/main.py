from st_pages import Page, show_pages

from chatbot_page import chatbot_page
from create_event_page import create_event_page
from Recomendations import Recomendations

if __name__ == "__main__":
    # Declare the pages

    chatbot_page = Page("C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/chatbot_page.py", "Chatbot", "💬")
    Recomendations = Page("C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/Recomendations.py", "Recomendations", "🧾")
    create_event_page = Page("C:/Users/jukas/Desktop/Mackro/Marco-Bot/Marco/create_event_page.py", "Create Event", "📅")

    # Show the pages in the sidebar
    show_pages([
        chatbot_page,
        create_event_page,
        Recomendations,
    ])
