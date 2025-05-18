import io, os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_ID = "1HFPEQYjeJQtQvwu8eaMO1hW6jpY7jik6"


def _drive_service():
    creds = service_account.Credentials.from_service_account_info(
        {k: v for k, v in os.environ.items() if not k.startswith("_")},
        scopes=SCOPES,
    )
    return build("drive", "v3", credentials=creds)


def upload_csv_to_gdrive(bytes_data: bytes, filename: str):
    service = _drive_service()

    media = MediaIoBaseUpload(
        io.BytesIO(bytes_data), mimetype="text/csv", resumable=False
    )
    try:
        metadata = {"name": filename, "parents": [FOLDER_ID]}
        created = (
            service.files()
            .create(
                body=metadata,
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            )
            .execute()
        )
        print("File created ✔ (id:", created["id"] + ")")
    except HttpError as err:
        print("Drive API error:", err)
        if getattr(err, "content", None):
            print(
                err.content.decode() if isinstance(err.content, bytes) else err.content
            )
        raise
