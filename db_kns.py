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


conn = sqlite3.connect("bills_database1.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bills (
        BillID TEXT PRIMARY KEY,
        Name TEXT,
        SummaryLaw TEXT,
        LastUpdatedDate TEXT,
        DocumentPath TEXT,
        Presenter TEXT,
        TotalVotes INTEGER,
        InFavorVotes INTEGER,
        AgainstVotes INTEGER
    )
''')

try:

    for bill in finished_table:
        cursor.execute("INSERT INTO bills VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (bill['BillID'], bill['Name'], bill['SummaryLaw'], bill['LastUpdatedDate'],
                        bill['document'], bill.get('present', ''), bill['total_vote'], bill['in_favor'], bill['against']))

except:
    pass
conn.commit()


conn = sqlite3.connect("bills_database1.db")
cursor = conn.cursor()
bill_id_to_update = '2208258'
cursor.execute("UPDATE bills SET TotalVotes = TotalVotes + 1, InFavorVotes = InFavorVotes + 1 WHERE BillID = ?",
               (bill_id_to_update,))

conn.commit()
conn.close()




conn = sqlite3.connect("bills_database1.db")
cursor = conn.cursor()


cursor.execute("SELECT * FROM bills where BillID = 2208258")
rows = cursor.fetchall()


for row in rows:
    print("BillID:", row[0])
    print("Name:", row[1])
    print("SummaryLaw:", row[2])
    print("LastUpdatedDate:", row[3])
    print("DocumentPath:", row[4])
    print("Presenter:", row[5])
    print("TotalVotes:", row[6])
    print("InFavorVotes:", row[7])
    print("AgainstVotes:", row[8])
    print("")

conn.close()