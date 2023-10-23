from kns_data import *
from concurrent.futures import ThreadPoolExecutor
'''
This page generates a table for our project He removes all bills from the 25th Knesset
and produces a table in which there is
The number of the bill. The name of the bill. the law suggests. The law document. Number of voters.
 Number of voters in favor. Number of voters against
'''

knesset_data_info = KnessetData()

def bills25():
     last = 2210585
     list_bills25 = []
     # while last != "2210664":
     for i in range(1):
          list_bills = knesset_data_info.get_bills(25, last)
          last = list_bills[-1]["BillID"]
          print(last)
          list_bills25 += list_bills
     return list_bills25


def infromation(list_of_bills):
     filter_list_bills = []
     for bill in list_of_bills:
          filter_bill = {"BillID": bill["BillID"], "Name": bill["Name"],"SummaryLaw":bill['SummaryLaw'], "LastUpdatedDate":
               bill["LastUpdatedDate"]}
          filter_list_bills.append(filter_bill)
     return filter_list_bills




def get_documents(my_json):
    for bill in my_json:
        try:
            bills_documents = knesset_data_info.get_bills_documents(bill_id=bill['BillID'])
            bill["document"] = bills_documents[0]['FilePath']
        except Exception as e:
            print(f"Error fetching document for {bill['BillID']}: {e}")
    return my_json



def get_billi(bills):
     for bill in bills:
          present = knesset_data_info.get_presenters_of_the_bill_by_id(bill['BillID'])
          try:
            person = present[0]['PersonID']
            person_name = knesset_data_info.get_knesset_members_info_by_personID(person)
            try:
                bill['present'] = person_name[0]['LastName'] + ' ' + person_name[0]['FirstName']
            except:
                pass
          except:
              pass


     return bills


if __name__ == "__main__":
    all_bills = bills25()
    filter_bills = infromation(all_bills)
    bills_plus_document = get_documents(filter_bills)
    finished_table = get_billi(bills_plus_document)
    for voters in finished_table:
        voters['total_vote'] = 0
        voters['in_favor'] = 0
        voters['against'] = 0
    print(finished_table)





















