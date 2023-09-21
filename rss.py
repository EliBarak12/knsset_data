import requests
import xml.etree.ElementTree as ET
import logging


class KnessetDataExtractor:
    def __init__(self, base_url):
        self.base_url = base_url
        self.namespaces = {
            '': "http://www.w3.org/2005/Atom",
            'd': "http://schemas.microsoft.com/ado/2007/08/dataservices",
            'm': "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"
        }

    def fetch_xml(self, relative_url):
        try:
            url = f"{self.base_url}/{relative_url}"
            print(url)
            response = requests.get(url)

            if response.status_code == 200:
                xml_content = response.content
                return ET.fromstring(xml_content)
            else:
                logging.error("Failed to fetch XML content. Status code: %d", response.status_code)
                return None

        except requests.exceptions.RequestException as e:
            logging.error("An error occurred: %s", str(e))
            return None
        except ET.ParseError as e:
            logging.error("XML parsing error: %s", str(e))
            return None

    def extract_entries(self, xml_root):
        entries = xml_root.findall('entry', self.namespaces)
        return entries

    @staticmethod
    def clean_tag_name(name):
        if name[0] == '{' and '}' in name:
            return name.split('}')[1]
        else:
            return name

    def extract_props(self, entry):
        props_parent = entry.find('content', self.namespaces).find('m:properties', self.namespaces)
        result = {}

        for prop in props_parent:
            result[self.clean_tag_name(prop.tag)] = prop.text

        return result


    def extract_data(self, relative_url):
        xml_root = self.fetch_xml(relative_url)
        print(xml_root)
        if xml_root:
            entries = self.extract_entries(xml_root)
            data_array = []

            for entry in entries:
                props = self.extract_props(entry)
                data_array.append(props)

            return data_array

        return []

    @staticmethod
    def return_data(data):
        formatted_data = []
        for item in data:
            formatted_item = {}
            for key in item:
                formatted_item[key] = item[key] or ''
            formatted_data.append(formatted_item)
        return formatted_data


class KnessetData:
    def __init__(self):
        self.base_url = "https://knesset.gov.il/Odata/ParliamentInfo.svc"

    def create_data_extractor(self):
        return KnessetDataExtractor(self.base_url)


    def kns_num(self,url,knesset_num):
        kns_num_filter = "?$filter=KnessetNum eq "
        kns_num_filter += str(knesset_num)

        return url + kns_num_filter

    def get_by_id(self, url, bill_id):
        if "$" in url:
            url += "&"
        else:
            url += "?"
        bill_id_filter = "$filter=BillID eq "
        bill_id_filter += str(bill_id)

        return url + bill_id_filter

    def skip_token(self, url, amount_of_token):
        if "$" in url:
            url += "&"
        else:
            url += "?"
        skip_tokens_filter = "$skiptoken="
        skip_tokens_filter += str(amount_of_token)
        url += skip_tokens_filter
        print(url)
        return url



    def get_bills_documents(self, bill_id=2209493):
        bills_document_url = "KNS_DocumentBill"
        knesset_data_extractor = self.create_data_extractor()
        bills_document_data = knesset_data_extractor.extract_data(self.get_by_id(bills_document_url, bill_id))
        response = knesset_data_extractor.return_data(bills_document_data)
        return response

    def get_bills(self,kns_number=25, amount_of_token=2209000):
        bill_url = "KNS_Bill"
        knesset_data_extractor = self.create_data_extractor()
        bill_url = self.kns_num(bill_url,kns_number)
        bill_data = knesset_data_extractor.extract_data(self.skip_token(bill_url, amount_of_token))
        response = knesset_data_extractor.return_data(bill_data)
        return response

    def get_presenters_of_the_bill(self,amount_of_token=200200):
        bill_initiator_url = "KNS_BillInitiator"
        knesset_data_extractor = self.create_data_extractor()
        bill_initiator_data = knesset_data_extractor.extract_data(self.skip_token(bill_initiator_url, amount_of_token))
        response = knesset_data_extractor.return_data(bill_initiator_data)
        return response

    def get_knesset_members_info(self,amount_of_token=30000):
        person_url = "KNS_Person"
        knesset_data_extractor = self.create_data_extractor()
        person_data = knesset_data_extractor.extract_data(self.skip_token(person_url, amount_of_token))
        response = knesset_data_extractor.return_data(person_data)
        return response


    def tables_types(self):
        types_url = "KNS_ItemType"
        knesset_data_extractor = self.create_data_extractor()
        types_data = knesset_data_extractor.extract_data(types_url)
        response = knesset_data_extractor.return_data(types_data)
        return response

    # def votes(self):
    #     votes_url ="Votes.svc/View_vote_rslts_hdr_Approved?$filter=knesset_num eq 2"
    #     knesset_data_extractor = KnessetDataExtractor("https://knesset.gov.il/Odata/")
    #     types_data = knesset_data_extractor.extract_data(votes_url)
    #     response = knesset_data_extractor.return_data(types_data)
    #     print(response)




if __name__ == "__main__":
    knesset_data_info = KnessetData()
    # print(knesset_data_info.tables_types())
    # print(knesset_data_info.get_bills(kns_number=25, amount_of_token=2209000))
    #print(knesset_data_info.votes())



    bills = knesset_data_info.get_bills()
    members = knesset_data_info.get_knesset_members_info(amount_of_token=30000)
    presenters = knesset_data_info.get_presenters_of_the_bill(amount_of_token=200200)

    def filter_bills(bills_array):
        my_json = []
        for bill in bills_array:
            one_bill = {}
            one_bill['BillID'] = bill['BillID']
            one_bill['Name'] = bill['Name']
            one_bill['SummaryLaw'] = bill['SummaryLaw']
            my_json.append(one_bill)

        return my_json

    def get_documents(my_json):
        for bill in my_json:
            try:
                bills_documents = knesset_data_info.get_bills_documents(bill_id=bill['BillID'])
                bill["document"] = bills_documents[0]['FilePath']
            except:
                pass

    def get_person(billInitiators,persons):
        members = {}
        for member in persons:
            members[member['PersonID']] = member['LastName'] + " " +member['FirstName']

        presents = {}
        for billi in billInitiators:
            try:
                presents[billi['BillID']] = members[billi['PersonID']]
            except:

                pass

        return presents

    bill_id_person = get_person(presenters,members)
    print(bill_id_person)






        
    my_json = filter_bills(bills)
    get_documents(my_json)
    print(my_json)






