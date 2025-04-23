

from datetime import datetime
import json
import requests
from castleguard_sdk.castleguard_base import CastleGuardBase


class Chat(CastleGuardBase):
    def chat(self, prompt, chat_id=None):
        """
        Interacts with the chat endpoint to generate a response from the model.
        
        :param prompt: The input prompt to send to the model.
        :param chat_id: Optional chat session ID.
        :return: Chatbot response or 'Unknown' if the request fails.
        """
        chat_url = f'{self.base_url}/chat-completion/chat'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        # Reuse the same Chat ID for the same session, or create a new one
        if not chat_id:
            params = {
                "displayName": "Chat " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            chat_response = requests.post(chat_url, headers=headers, params=params)
            if chat_response.status_code == 200:
                chat_id = json.loads(chat_response.text).get('id')
            else:
                self.log("Failed to create chat session", logLevel=3)
                return "Unknown", None

        # Post a message to the chat

        message_url = f'{self.base_url}/chat-completion/completions'
        message_payload = {
            "chatId": chat_id,
            "prompt": prompt,
            "model": "default",  # replace with actual model if needed
            "bestOf": 0,
            "echo": True,
            "frequencyPenalty": 0,
            "logitBias": {},
            "logprobs": 0,
            "maxTokens": 0,
            "n": 0,
            "presencePenalty": 0,
            "seed": 0,
            "stop": True,
            "stream": True,
            "streamOptions": "string",
            "suffix": "string",
            "temperature": 0,
            "topP": 0,
            "user": "string"
        }

        message_response = requests.post(message_url, json=message_payload, headers=headers)
        if message_response.status_code == 200:
            response_dict = json.loads(message_response.text)
            bot_message = response_dict.get('botMessage', {}).get('chatMessage')
            return bot_message, chat_id
        else:
            self.log(f"Failed to get response for prompt: {prompt}", logLevel=3)
            return "Unknown", chat_id

    def chat_with_collection(self, prompt, collection_id=None):
        """
        Interacts with the chat endpoint to generate a response from the model.
        
        :param prompt: The input prompt to send to the model.
        :param chat_id: Optional chat session ID.
        :return: Chatbot response or 'Unknown' if the request fails.
        """
        chat_url = f'{self.base_url}/chat-completion/chat'
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        # create a new chat session
        chat_id = None        
        params = {
            "displayName": "Chat " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
        chat_response = requests.post(chat_url, headers=headers, params=params)
        if chat_response.status_code == 200:
            chat_id = json.loads(chat_response.text).get('id')
        else:
            self.log("Failed to create chat session", logLevel=3)
            self.log(f"Error: {chat_response.text} statuse{chat_response.status_code}", logLevel=3)
            return "Unknown", None
        
        # attach collection to chat
        attach_collection_url = f'{self.base_url}/chat-completion/chat/collection-id/{chat_id}'
        attach_collection_payload = [collection_id]
        
        requests.patch(attach_collection_url, json=attach_collection_payload, headers=headers)
        
        # Post a message to the chat
        message_url = f'{self.base_url}/chat-completion/completions'
        message_payload = {
            "chatId": chat_id,
            "prompt": prompt,
            "model": "default",  # replace with actual model if needed
            "bestOf": 0,
            "echo": True,
            "frequencyPenalty": 0,
            "logitBias": {},
            "logprobs": 0,
            "maxTokens": 0,
            "n": 0,
            "presencePenalty": 0,
            "seed": 0,
            "stop": True,
            "stream": True,
            "streamOptions": "string",
            "suffix": "string",
            "temperature": 0,
            "topP": 0,
            "user": "string"
        }
        try:
            message_response = requests.post(message_url, json=message_payload, headers=headers)
            message_response.raise_for_status()  # Check for HTTP errors
        except requests.exceptions.RequestException as e:
            self.log(f"Failed to get response for prompt: {prompt}", logLevel=3)
            self.log(f"Error: {e}", logLevel=3)
            return "Unknown", chat_id
        response_dict = json.loads(message_response.text)
        bot_message = response_dict.get('botMessage')
        chat_message = bot_message.get('chatMessage')
        return chat_message, chat_id
    
