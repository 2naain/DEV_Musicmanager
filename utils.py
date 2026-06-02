import os
from supabase import create_client
from dotenv import load_dotenv
from pathlib import Path
import shutil
from fastapi import File, UploadFile, HTTPException

load_dotenv()

IMG_DIR = Path("files/img")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")


def save_img_local(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Archivo Invalido")

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    dest = IMG_DIR / file.filename

    with dest.open("wb") as store:
        shutil.copyfileobj(file.file, store)

    return dest


## SUPABASE
def supabase_client():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise RuntimeError("No credentials")
    return create_client(url, key)


def save_img_remote(file: UploadFile):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Archivo Invalido")

    contents = file.file.read()
    path = file.filename

    supa_client = supabase_client()

    response = supa_client.storage.from_(SUPABASE_BUCKET).upload(
        path=path,
        file=contents,
        file_options={"contente-type": file.content_type},
    )
    stored_url_bucket = (supa_client.
                         storage.
                         from_(SUPABASE_BUCKET).
                         get_public_url(path))

    return stored_url_bucket
