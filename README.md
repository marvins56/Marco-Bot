# Marco-Bot

Marco - Your Event Companion

![image](https://github.com/marvins56/Marco-Bot/assets/82571414/b928a824-2e11-4300-af83-7fc3e6eab7ea)


Marco is a comprehensive event management platform designed primarily for travelers. It serves as a one-stop database for discovering, booking, and even hosting events. Whether you're a tourist exploring a new city or a local looking to uncover hidden gems, Marco has you covered.

**Features**

Discover diverse events based on location and preferences.
Reservation and booking services for all listed events.
Capability to host and manage your events.
Promotional services for event organizers to increase visibility.

**Installation**

Clone the repository:

[git clone https://github.com/your-github-username/marco.git](https://github.com/marvins56/Marco-Bot.git)


**Install the dependencies:**

pip install -r requirements.txt

**Usage**

To run Marco, execute the following command:navigate to the main.py and run the command

streamlit run main.py

**environment Variables**

Copy the example.env file and create a new file called .env paste the content and replace the spaces with the api keys

**Database Connection**

in case you have csv files and you want to convert them to MYSQL run the csvToMysql.py file to convert to mysql.
import the database into your workbench.

look for files with functions with 

**db = SQLDatabase.from_uri("mysql+mysqlconnector://root:password@localhost/<databaseName-Here>")**
