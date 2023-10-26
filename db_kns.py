import sqlite3
from set_tables import *


# all_bills = bills25()
# filter_bills = infromation(all_bills)
# bills_plus_document = get_documents(filter_bills)
# finished_table = get_billi(bills_plus_document)
# for voters in finished_table:
#     voters['total_vote'] = 0
#     voters['in_favor'] = 0
#     voters['against'] = 0
# print(finished_table)

#
# conn = sqlite3.connect("bills_database1.db")
# cursor = conn.cursor()
#
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS bills (
#         BillID TEXT PRIMARY KEY,
#         Name TEXT,
#         SummaryLaw TEXT,
#         LastUpdatedDate TEXT,
#         DocumentPath TEXT,
#         Presenter TEXT,
#         TotalVotes INTEGER,
#         InFavorVotes INTEGER,
#         AgainstVotes INTEGER
#     )
# ''')
#
# try:
#
#     for bill in finished_table:
#         cursor.execute("INSERT INTO bills VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                        (bill['BillID'], bill['Name'], bill['SummaryLaw'], bill['LastUpdatedDate'],
#                         bill['document'], bill.get('present', ''), bill['total_vote'], bill['in_favor'], bill['against']))
#
# except:
#     pass
# conn.commit()


# conn = sqlite3.connect("bills_database1.db")
# cursor = conn.cursor()
# bill_id_to_update = '2208258'
# cursor.execute("UPDATE bills SET TotalVotes = TotalVotes + 1, InFavorVotes = InFavorVotes + 1 WHERE BillID = ?",
#                (bill_id_to_update,))
#
# conn.commit()
# conn.close()




conn = sqlite3.connect("bills_database1.db")
cursor = conn.cursor()


cursor.execute("SELECT * FROM bills")
rows = cursor.fetchall()
print(rows)
#
# for row in rows:
#     print("BillID:", row[0])
#     print("Name:", row[1])
#     print("SummaryLaw:", row[2])
#     print("LastUpdatedDate:", row[3])
#     print("DocumentPath:", row[4])
#     print("Presenter:", row[5])
#     print("TotalVotes:", row[6])
#     print("InFavorVotes:", row[7])
#     print("AgainstVotes:", row[8])
#     print("")
#
# conn.close()
party_names = [
    'Likud_For','Likud_Against', 'YeshAtidNationalUnity_For', 'YeshAtidNationalUnity_Against',
    'Shas_For', 'Shas_Against', 'Mafdal_ReligiousZionism_For', 'Mafdal_ReligiousZionism_Against',
    'UnitedTorahJudaism_For', 'UnitedTorahJudaism_Against', 'OtzmaYehudit_For', 'OtzmaYehudit_Against',
    'YisraelBeiteinu_For', 'YisraelBeiteinu_Against', 'UnitedArabList_For', 'UnitedArabList_Against',
    'Hadash_Taal_For', 'Hadash_Taal_Against', 'LaborParty_For', 'LaborParty_Against',
    'Noam_For', 'Noam_Against'
]


a = []
for i in rows:
    b = {}
    b['BillID'] = i[0]
    for x in party_names:
        b[x] = 0
    a.append(b)

conn = sqlite3.connect("billsParties_database1.db")
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS BillPart (
    billid TEXT PRIMARY KEY,
    Likud_For INT,
    Likud_Against INT,
    YeshAtidNationalUnity_For INT,
    YeshAtidNationalUnity_Against INT,
    Shas_For INT,
    Shas_Against INT,
    Mafdal_ReligiousZionism_For INT,
    Mafdal_ReligiousZionism_Against INT,
    UnitedTorahJudaism_For INT,
    UnitedTorahJudaism_Against INT,
    OtzmaYehudit_For INT,
    OtzmaYehudit_Against INT,
    YisraelBeiteinu_For INT,
    YisraelBeiteinu_Against INT,
    UnitedArabList_For INT,
    UnitedArabList_Against INT,
    Hadash_Taal_For INT,
    Hadash_Taal_Against INT,
    LaborParty_For INT,
    LaborParty_Against INT,
    Noam_For INT,
    Noam_Against INT
)''')


try:
    for bill in a:
        columns = ', '.join(bill.keys())
        placeholders = ', '.join(['?'] * len(bill))
        values = tuple(bill.values())
        cursor.execute(f"INSERT INTO BillPart ({columns}) VALUES ({placeholders})", values)
except Exception as e:
    print("Error:", e)

conn.commit()
conn.close()


conn = sqlite3.connect("billsParties_database1.db")
cursor = conn.cursor()

# Select all columns from the "BillVotes" table
cursor.execute("SELECT * FROM BillPart")
data = cursor.fetchall()

# Print the data
for row in data:
    print(row)

conn.close()