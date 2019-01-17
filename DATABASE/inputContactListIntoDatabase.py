import openpyxl as px
import pymongo
from pymongo import MongoClient
#This module retrieves all contacts from the contacts_list excel sheet and stores them in our database. The purpose of this module was to input all 900 pieces of data into our MongoDB Database without having to do it manually. However, we are no longer rendering the contact information for the website  as it is not ethical to show everybodys information
workbook = px.load_workbook('contacts_list.xlsx', True)
sheet = workbook.get_sheet_by_name(name='contacts')
client = MongoClient('localhost', 27017)
database = client.KKNY

for row in sheet.iter_rows("A3:L957"):
    counter = 0
    info = {}
    for column in row:
        counter += 1
        if column.value:
            if counter == 2:
                info["First Name"] = column.value
            if counter == 3:
                info["Last Name"] = column.value
            if counter == 7:
                info["Street"] = column.value
            if counter == 8:
                info["City"] = column.value
            if counter == 9:
                info["State"] = column.value
            if counter == 10:
                info["Zip"] = column.value
            if counter == 11:
                info["Phone Number"] = column.value
            if counter == 12:
                info["Email"] = column.value
            if counter == 13:
                info["Cell Phone"] = column.value
    database.contact_list.insert_one(info)
