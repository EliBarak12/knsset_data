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

    def get_by_person_id(self, url, person_id):
        if "$" in url:
            url += "&"
        else:
            url += "?"
        bill_id_filter = "$filter=PersonID eq "
        bill_id_filter += str(person_id)

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

    def get_presenters_of_the_bill(self,amount_of_token=202500):
        bill_initiator_url = "KNS_BillInitiator"
        knesset_data_extractor = self.create_data_extractor()
        bill_initiator_data = knesset_data_extractor.extract_data(self.skip_token(bill_initiator_url, amount_of_token))
        response = knesset_data_extractor.return_data(bill_initiator_data)
        return response

    def get_presenters_of_the_bill_by_id(self, id=2209530):
        bill_initiator_url = "KNS_BillInitiator"
        knesset_data_extractor = self.create_data_extractor()
        bill_initiator_data = knesset_data_extractor.extract_data(self.get_by_id(bill_initiator_url, id))
        response = knesset_data_extractor.return_data(bill_initiator_data)
        return response

    def get_knesset_members_info(self,amount_of_token=30000):
        person_url = "KNS_Person"
        knesset_data_extractor = self.create_data_extractor()
        person_data = knesset_data_extractor.extract_data(self.skip_token(person_url, amount_of_token))
        response = knesset_data_extractor.return_data(person_data)
        return response

    def get_knesset_members_info_by_personID(self, p=23597):
        person_url = "KNS_Person"
        knesset_data_extractor = self.create_data_extractor()
        person_data = knesset_data_extractor.extract_data(self.get_by_person_id(person_url, p))
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






        






