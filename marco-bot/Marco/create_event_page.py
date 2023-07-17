import datetime
import os
import uuid
import streamlit as st
import mysql.connector

from Utils import UPLOAD_DIR, save_image

from chatbot_page import chatbot_page

from Recomendations import Recomendations

def create_event_page():
    with st.form("create_event_form"):
        name = st.text_input("Event Name")
        desc = st.text_area("Description")
        eventDate = st.date_input("Start Date", value=datetime.date.today())
        eventDate = eventDate.strftime("%Y-%m-%d")
        eventEndDate = st.date_input("End Date", value=datetime.date.today())
        eventEndDate = eventEndDate.strftime("%Y-%m-%d")
        eventTime = st.number_input("Start Time", step=1)
        eventEndTime = st.time_input("End Time")
        location = st.text_input("Location")
        image = st.file_uploader("Image")

        is_free = st.checkbox("Free")
        if not is_free:
             price = 0

        price = st.number_input("Price", key="price_input")
        filters = st.text_input("Event Category")
        bookingLink = st.text_input("Link")

        if st.form_submit_button("Create"):
            try:
                conn = mysql.connector.connect(
                    user='root', password='password', host='localhost', database='macrol'
                )
                cursor = conn.cursor()

                image_filename = str(uuid.uuid4()) + '.jpg'
                save_image(image, image_filename)
                image = os.path.join(UPLOAD_DIR, image_filename)

                insert_stmt = (
                    "INSERT INTO items (name, `desc`, eventDate, eventEndDate, eventTime, eventEndTime, `list`, image, price, filters, bookingLink) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                )

                data =  (name, desc, eventDate, eventEndDate, eventTime, eventEndTime, location, image, price, filters, bookingLink)

                cursor.execute(insert_stmt, data)
                conn.commit()
                conn.close()

                st.success("Event created successfully!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")



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
    "—": create_event_page,
    "ChatBot": chatbot_page,
    "Recomendation": Recomendations,
    "introduction": intro
}

demo_name = st.sidebar.selectbox("Choose a Action", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
