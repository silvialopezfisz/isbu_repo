import pymssql 
import pandas as pd
from db_connect_helpers import readin_csv
from db_connect_helpers import retrieve_telephones, retrieve_emails
from db_connect_helpers import insert_company_entry, insert_telephone_entry, insert_email_entry

DATABASE = 'isbu_db'
USERNAME = 'sa'
PASSWORD = 'reallyStrongPwd123'

df = readin_csv('infosecindex.csv')
df = df
# company_df, telephone_df, email_df = separate_dfs(df)
 
conn = pymssql.connect(server = 'localhost', 
                      user = USERNAME,
                      password = PASSWORD,
                      database = DATABASE)

print(" CONNECTED TO DB SUCCESFULLY")

cursor = conn.cursor()  

# Go through the CSV and add each Company, with its respective Telephone and Email entries
for index in df.index:
    
    company_name = df['company_name'][index]
    company_tagline = df['company_tagline'][index]
    telephone = df['telephone'][index]
    email = df['email'][index]
    website = df['website'][index]


    # Insert a company if it doesn't already exist in the db, carry over its company_id if it does
    last_company_id = insert_company_entry(company_name, company_tagline, website, conn, cursor)
    
    # Insert a telephone entry for the corresponding company
    insert_telephone_entry(telephone, last_company_id, conn, cursor)

    insert_email_entry(email, last_company_id, conn, cursor)

cursor.close()
conn.close()
