from kns_data import *

knesset_data_info = KnessetData()


d = [{'BillID': '2209528', 'KnessetNum': '25', 'Name': 'הצעת חוק הבטחת מסגרת השמה חוץ-ביתית לקטינים נזקקים, התשפ"ד-2023'
          , 'SubTypeID': '54', 'SubTypeDesc': 'פרטית', 'PrivateNumber': '3936', 'CommitteeID': '', 'StatusID': '104'
          , 'Number': '', 'PostponementReasonID': '', 'PostponementReasonDesc': '', 'PublicationDate': ''
          , 'MagazineNumber': '', 'PageNumber': '', 'IsContinuationBill': '', 'SummaryLaw': '', 'PublicationSeriesID': '', 'PublicationSeriesDesc': ''
          , 'PublicationSeriesFirstCall': '', 'LastUpdatedDate': '2023-10-16T08:53:59.23'}
     , {'BillID': '2209529', 'KnessetNum': '25', 'Name': 'הצעת חוק העברת מידע בין רשויות, התשפ"ד-2023',
        'SubTypeID': '54', 'SubTypeDesc': 'פרטית', 'PrivateNumber': '3983', 'CommitteeID': '', 'StatusID': '104',
        'Number': '', 'PostponementReasonID': '', 'PostponementReasonDesc': '', 'PublicationDate': '', 'MagazineNumber': ''
          , 'PageNumber': '', 'IsContinuationBill': '', 'SummaryLaw': '', 'PublicationSeriesID': '',
        'PublicationSeriesDesc': '', 'PublicationSeriesFirstCall': '', 'LastUpdatedDate': '2023-10-16T08:53:59.92'}
     , {'BillID': '2209530', 'KnessetNum': '25',
        'Name': 'הצעת חוק שירות המדינה (מינויים) (תיקון - העדפת מועמדים תושבי פריפריה), התשפ"ד-2023',
        'SubTypeID': '54', 'SubTypeDesc': 'פרטית', 'PrivateNumber': '3961', 'CommitteeID': '', 'StatusID': '104'
          , 'Number': '', 'PostponementReasonID': '', 'PostponementReasonDesc': '', 'PublicationDate': ''
          , 'MagazineNumber': '', 'PageNumber': '', 'IsContinuationBill': '', 'SummaryLaw': '',
        'PublicationSeriesID': '', 'PublicationSeriesDesc': '', 'PublicationSeriesFirstCall': ''
          , 'LastUpdatedDate': '2023-10-16T08:54:00.2'}]


def bills25():
     last = 2150000
     list_bills25 = []
     while last != "2210664":
          list_bills = knesset_data_info.get_bills(25, last)
          last = list_bills[-1]["BillID"]
          list_bills25 += list_bills
     return list_bills25


def infromation(list_of_bills):
     filter_list_bills = []
     for bill in list_of_bills:
          filter_bill = {"BillID": bill["BillID"], "Name": bill["Name"],"SummaryLaw":bill['SummaryLaw'], "LastUpdatedDate":
               bill["LastUpdatedDate"]}
          filter_list_bills.append(filter_bill)
     return filter_list_bills


filters = infromation(d)

def get_documents(my_json):
    for bill in my_json:
        try:
            bills_documents = knesset_data_info.get_bills_documents(bill_id=bill['BillID'])
            bill["document"] = bills_documents[0]['FilePath']
        except:
            pass

    return my_json

adde = get_documents(filters)

def get_billi(bills):
     for bill in bills:
          present = knesset_data_info.get_presenters_of_the_bill_by_id(bill['BillID'])
          print(present)
          person = present[0]['PersonID']
          person_name = knesset_data_info.get_knesset_members_info_by_personID(person)
          print(person_name)
          bill['present'] = person_name[0]['LastName'] + ' ' + person_name[0]['FirstName']
     return bills

biil = get_billi(adde)

print(biil)

























