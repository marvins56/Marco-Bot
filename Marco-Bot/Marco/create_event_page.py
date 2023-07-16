import datetime
import os
import uuid
import streamlit as st
import mysql.connector

from Utils import UPLOAD_DIR, save_image


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

if __name__ == "__main__":
    create_event_page()
