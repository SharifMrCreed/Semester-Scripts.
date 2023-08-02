import time

import requests
from pypdf import PdfReader
import os


def get_file_size(file_path):
    return os.path.getsize(file_path)


def print_file_size(size_in_bytes):
    # Convert size from bytes to kilobytes, megabytes, and gigabytes
    size_in_kilobytes = size_in_bytes / 1024
    size_in_megabytes = size_in_kilobytes / 1024
    size_in_gigabytes = size_in_megabytes / 1024

    if int(size_in_gigabytes) > 0:
        return f"{round(size_in_gigabytes, 2)} GB"
    elif int(size_in_megabytes) > 0:
        return f"{round(size_in_megabytes, 2)} MB"
    elif int(size_in_megabytes) > 0:
        return f"{round(size_in_kilobytes, 2)} KB"
    else:
        return f"{round(size_in_bytes, 2)} B"


def download_pdf(url, destination):
    response = requests.get(url)

    with open(destination, 'wb') as output_file:
        output_file.write(response.content)


def get_pdf_data(pdf_file_path):
    before = int(round(time.time() * 1000))
    reader = PdfReader(pdf_file_path)
    return {
        "title": {reader.metadata.title},
        "dateCreated": {reader.metadata.creation_date},
        "dateModified": {reader.metadata.modification_date},
        "size": get_file_size(pdf_file_path),
        "pageCount": len(reader.pages),
        "texts": [page.extract_text() for page in reader.pages],
        "usageData": {
            "views": [],
            "summaries": [],
            "Explanations": [],
            "SampleQuestions": []
        },

        "aiData": {
            "title": "aiTitle",
            "summary": "Summary"
        },
    }
