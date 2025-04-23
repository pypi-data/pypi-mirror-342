import os
import re
import sys
import time
import inspect
import requests


class CastleGuardBase:
    def __init__(self):
        self.base_url = None
        self.username = None
        self.password = None
        self.token = None

    def _normalize_url(self, base_url, default_version):
        """
        Normalize the base URL to ensure it includes an API version.

        :param base_url: The base URL provided by the user.
        :param default_version: The default API version to append if none is provided.
        :return: The normalized URL with the correct API version.
        """
        # Check if base_url already contains an API version (e.g., /api/vX where X can be any version)
        if re.search(r'/api/v\d+$', base_url):
            return base_url
        # If base_url ends with a slash, strip it
        if base_url.endswith('/'):
            base_url = base_url.rstrip('/')
        # Append the default version if no version is provided
        return f"{base_url}/api/{default_version}"

    def log(self, message, logLevel=1):
        """
        Sends log messages to the CastleGuard logging endpoint as URL parameters.

        :param message: Log message.
        :param logLevel: Log level (0-6).
        """
        if not self.token:
            print("Cannot log message because authentication failed.")
            return

        url = f'{self.base_url}/logger'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }

        params = {
            'message': message,
            'logLevel': logLevel
        }

        try:
            response = requests.post(url, headers=headers, params=params)
            if response.status_code == 200:
                print(f"Logging: {message}")
            else:
                print(f"Failed to send log: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Log request failed: {e}")

    def _get_status_codes(self, document_ids, url, headers, document_type="unknown"):
        """
        Gets the status of a generic document.

        :param document_ids: The IDs of the documents.
        :param url: The URL to get the document status.
        :param headers: Headers for the request.
        :return: List of status codes if successful, None otherwise.
        """

        running_document_ids = document_ids.copy()
        statuses = []
        while len(running_document_ids) > 0:
            params = {
                'documentIds': running_document_ids
            }
            response = requests.get(url, headers=headers, params=params)

            if response.status_code != 200:
                self.log(
                    f"Failed to get {document_type} document: {response.text}",
                    logLevel=3
                )
                return None

            for document in response.json():
                job_detail = document.get('jobDetail', {})
                status = job_detail.get('status', None)
                if status == 2:
                    if document.get('id') in running_document_ids:
                        running_document_ids.remove(document.get('id'))
                        statuses.append({
                            "document_id": document.get('id'),
                            "status": job_detail.get('statusCode', None),
                            "status_code": job_detail.get('status', None),
                            "status_name": job_detail.get('statusName', None)
                        })
            if len(running_document_ids) > 0:
                time.sleep(5)

        return statuses

    def _get_status_code(self, url, headers, document_type="unknown"):

        status = None
        while status != 2:
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                self.log(f"Failed to get the {document_type} document: {response.text}", logLevel=3)
                return None

            document = response.json()
            job_detail = document.get('jobDetail', {})
            status = job_detail.get('status', None)
            if status == 2:
                status_code = job_detail.get('statusCode', None)
                return status_code

            time.sleep(5)

    def _download_document(
        self,
        url: str,
        headers: dict,
        file_name: str,
        save_dir=".",
        document_type="unknown"
    ):
        try:
            response = requests.get(url, headers=headers)

            if save_dir.startswith("."):
                save_dir = os.path.join(self._get_caller_file_path(4), save_dir)

            save_dir = os.path.normpath(save_dir)

            # Make sure the directory exists
            os.makedirs(save_dir, exist_ok=True)

            if response.status_code != 200:
                self.log(f"Failed to download {document_type} document: {response.text}", logLevel=3)
                return None

            save_path = os.path.join(save_dir, file_name)
            with open(save_path, 'wb') as file:
                file.write(response.content)

            return save_path
        except Exception as e:
            self.log(f"Download request failed: {e}", logLevel=3)
            return None

    def _get_caller_file_path(self, depth=2):
        # return os.path.abspath(os.getcwd())
        frame = inspect.stack()[depth]  # Get the frame of the caller
        caller_file = frame[0]
        caller_dir = os.path.dirname(os.path.abspath(caller_file.f_code.co_filename))
        return caller_dir
