import openpyxl as px
import pymongo
from pymongo import MongoClient
#This module retrieves all contacts from the contacts_list excel sheet and stores them in our database. The purpose of this module was to input all 900 pieces of data into our MongoDB Database without having to do it manually. However, we are no longer rendering the contact information for the website  as it is not ethical to show everybodys information
workbook = px.load_workbook('previous_committee.xlsx', True)
sheet = workbook.get_sheet_by_name(name='Sheet1')
client = MongoClient('localhost', 27017)
database = client.KKNY

for row in sheet.iter_rows("A2:F32"):
    counter = 1
    info = {}
    for column in row:
        counter += 1
        if column.value:
            if counter == 2:
                info["Year"] = column.value
            if counter == 3:
                info["President"] = column.value
            if counter == 4:
                info["Vice President"] = column.value
            if counter == 5:
                info["Secretary"] = column.value
            if counter == 6:
                info["Joint Treasurer"] = column.value
            if counter == 7:
                info["Treasurer"] = column.value
    database.previous_committee.insert_one(info)
