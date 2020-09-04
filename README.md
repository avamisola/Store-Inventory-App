# python_techdegree_project_4
 A Store Inventory


Setup:

1. Create a new virtual Python environment
python -m venv env

2. Activate your new virtual Python environment
Mac/Linux:
source ./env/bin/activate
Windows:
.\env\Scripts\activate

3. Install required dependencies into your Python environment
pip install -r requirements.txt

4. Run the app
python app.py


Summary:

This app loads data from csv file into a database.
The database model is created using the peewee module.
User can use menu to navigate database and backup database to csv file.


App main menu:

======================================================
--Welcome to the Store Inventory Database--
Select an option by entering the corresponding letter
v) View entry in database
a) Add entry to database
b) Backup the database to csv
q) Quit the app
======================================================
