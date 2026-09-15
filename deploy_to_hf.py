import os
from huggingface_hub import HfApi

HF_TOKEN = os.environ["HF_TOKEN"]
HF_REPO_ID = os.environ["HF_REPO_ID"]

api = HfApi(token=HF_TOKEN)

api.upload_folder(
    folder_path=".", # cartella corrente
    repo_id=HF_REPO_ID, # nome dello space su HF
    repo_type="space",
    allow_patterns=["app.py", "inference.py", "requirements.txt"], # file di cui viene fatto il deploy su HF
)

print(f"Deploy completed on: https://huggingface.co/spaces/{HF_REPO_ID}")