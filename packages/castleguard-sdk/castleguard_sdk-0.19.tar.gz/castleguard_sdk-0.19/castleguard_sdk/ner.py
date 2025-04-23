
import requests
from castleguard_sdk.castleguard_base import CastleGuardBase


class Ner(CastleGuardBase):

    def named_entity_recognition(self, text):
        """
        Performs named entity recognition (NER) on a given text.

        :param text: The input text for NER.
        :return: Extracted entities or None if the request fails.
        """
        url = f'{self.base_url}/ner/ner-text'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        query = {
            "inputText": text
        }

        response = requests.post(url, headers=headers, params=query)
        if response.status_code == 200:
            ner_result = response.json()
            #self.log(f"NER result: {ner_result}", logLevel=1)
            return ner_result
        else:
            self.log(f"NER extraction failed: {response.text}", logLevel=3)
            return None

    def named_entity_recognition_multiple_text(self, text_list):
        """
        Performs named entity recognition (NER) on a given text.

        :param  text_list: The list of input text for NER.
        :return: List of extracted entities or None if the request fails.
        """
        url = f'{self.base_url}/ner/ner-texts'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        params = {
            'inputTexts': text_list
        }

        response = requests.post(url, headers=headers, params=params)
        if response.status_code == 200:
            ner_result = response.json()
            return ner_result
        else:
            self.log(f"NER extraction failed: {response.text}", logLevel=3)
            return None
