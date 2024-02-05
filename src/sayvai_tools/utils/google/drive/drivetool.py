import io
import os
from pprint import pprint

import pandas as pd
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from service import Create_Service


class Drive:
    """Tool that allows you to work with Google Drive."""

    name = "drive"
    description = (
        "Useful for creating, update, delete and other changes in Google Drive."
    )

    def __init__(
        self,
        SERVICE_ACCOUNT_FILE: str,
        API_NAME: str = "drive",
        API_VERSION: str = "v3",
        SCOPES: list[str] = ["https://www.googleapis.com/auth/drive"],
    ):
        self.service = Create_Service(
            SERVICE_ACCOUNT_FILE, API_NAME, API_VERSION, SCOPES
        )

    """Function to create a new folder in drive."""

    def create_folder(self, folder_name: str, parent_id: str | None = None):
        if parent_id is not None:
            """Create folder in mentioned directory."""
            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [parent_id],
            }
        else:
            """Creates folder in the outer directory."""
            file_metadata = {
                "name": folder_name,
                "mimeType": "application/vnd.google-apps.folder",
            }
        response = self.service.files().create(body=file_metadata).execute()
        print(
            f"Folder '{response['name']}' with id '{response['id']}' has been successfully created."
        )
        return "Folder creation is successful."

    """Function to upload a file in drive."""

    def upload_file(
        self, file_path: str, file_name, mime_type: str, parent_id: str | None = None
    ):
        if parent_id is not None:
            """Upload file in mentioned directory."""
            file_metadata = {
                "name": file_name,
                "parents": [parent_id],
                "mimeType": mime_type,
            }
        else:
            """Upload file in the outer directory."""
            file_metadata = {"name": file_name, "mimeType": mime_type}
        media = MediaFileUpload(file_path, mimetype=mime_type)
        response = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(
            f"File '{response['name']}' with id '{response['id']}' has been successfully uploaded."
        )
        return "File upload is successful."

    """Function to download a file from drive."""

    def download_file(self, file_id: str, file_name: str):
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(file_name, "wb")
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))
        fh.seek(0)
        print(
            f"File '{file_name}' with id '{file_id}' has been successfully downloaded."
        )
        return "File download is successful."

    """Function to copy a file in drive."""

    def copy_file(self, source_file_id: str, parent_id: str):
        file_metadata = {
            "name": "sayvai_logo.jpg",
            "parents": [parent_id],
            "starred": True,
            "description": "This is a logo of SayvAI",
        }
        response = (
            self.service.files()
            .copy(fileId=source_file_id, body=file_metadata)
            .execute()
        )
        print(
            f"File '{response['name']}' with id '{response['id']}' has been successfully copied."
        )
        return "File copy is successful."

    """Function to get drive account information."""

    def get_account_info(self):
        response = self.service.about().get(fields="*").execute()
        pprint(response)
        for k, v in response.get("storageQuota").items():
            print("{0}: {1:.2f}MB".format(k, int(v) / 1024**2))
            print("{0}: {1:.2f}GB".format(k, int(v) / 1024**3))
        return "Account information is successful."

    """Function to get list of files in drive'}"""

    def get_list_of_files(self, parent_id: str):
        query = f"parents = '{parent_id}'"
        results = (
            self.service.files()
            .list(
                pageSize=1000,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)",
                q=query,
            )
            .execute()
        )
        print(results)
        items = results.get("files", [])
        data = []
        for row in items:
            if row["mimeType"] != "application/vnd.google-apps.folder":
                row_data = []
                try:
                    row_data.append(round(int(row["size"]) / 1000000, 2))
                except KeyError:
                    row_data.append(0.00)
                row_data.append(row["id"])
                row_data.append(row["name"])
                row_data.append(row["modifiedTime"])
                row_data.append(row["mimeType"])
                data.append(row_data)
        cleared_df = pd.DataFrame(
            data,
            columns=["size_in_MB", "id", "name", "last_modification", "type_of_file"],
        )
        print(cleared_df)
        return "List of files is successful."

    """Function to delete a file or folder in drive."""

    def delete_file(self, file_id: str):
        self.service.files().delete(fileId=file_id).execute()
        print(f"File/Folder with id '{file_id}' has been successfully deleted.")
        return "File/Folder deletion is successful."

    """Function to update a file in drive."""

    def update_file(self, file_id: str, file_path: str, mime_type: str):
        media = MediaFileUpload(file_path, mimetype=mime_type)
        response = (
            self.service.files().update(fileId=file_id, media_body=media).execute()
        )
        print(
            f"File '{response['name']}' with id '{response['id']}' has been successfully updated."
        )
        return "File update is successful."
