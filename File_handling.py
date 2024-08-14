import pandas as pd
import numpy as np
import re
import requests
from io import StringIO
from base64 import b64encode, b64decode
import json
import streamlit as st

GITHUB_TOKEN = st.secrets["GitHub"]["apikey"]
REPO = "AzeemChaudhry/attendance_merger"
BRANCH = "main"
def github_request(method, url, data=None, headers=None):
    response = requests.request(method, url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def get_file_content(path):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = github_request("GET", url, headers=headers)
    content = b64decode(response['content']).decode()
    return content, response['sha']

def update_file(path, content, sha):
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    data = {
        "message": "Update file",
        "content": b64encode(content.encode()).decode(),
        "sha": sha,
        "branch": BRANCH
    }
    response = github_request("PUT", url, data=data, headers=headers)
    return response