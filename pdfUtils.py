import time

import requests
from typing import List
from pypdf import PdfReader
import os
import asyncio
import aiohttp
from pypdf.generic import NullObject


async def get_file_size(file_path):
    return os.path.getsize(file_path)


def file_exists(file_path):
    return os.path.exists(file_path)


def convert_file_size(size_in_bytes):
    # Convert size from bytes to kilobytes, megabytes, and gigabytes
    size_in_kilobytes = size_in_bytes / 1024
    size_in_megabytes = size_in_kilobytes / 1024
    size_in_gigabytes = size_in_megabytes / 1024

    if int(size_in_gigabytes) > 0:
        return f"{round(size_in_gigabytes, 2)} GB"
    elif int(size_in_megabytes) > 0:
        return f"{round(size_in_megabytes, 2)} MB"
    elif int(size_in_kilobytes) > 0:
        return f"{round(size_in_kilobytes, 2)} KB"
    else:
        return f"{round(size_in_bytes, 2)} B"


async def download_pdf(url, destination):
    response = requests.get(url)

    with open(f"downloads/{destination}", 'wb') as output_file:
        output_file.write(response.content)


async def download_pdf_async(url, filename):
    destination = f"downloads/{filename}"
    if file_exists(destination):
        print(f"Downloaded {destination}")
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    with open(destination, 'wb') as file:
                        while True:
                            chunk = await response.content.read(1024)
                            if not chunk:
                                break
                            file.write(chunk)
                    print(f"Downloaded {destination}")
                else:
                    print(f"Failed to download {url}")


async def get_pdf_data(name: str):
    print(f"Extracting info on {name}")
    before = int(round(time.time() * 1000))
    path = f"downloads/{name}"
    info = {
        "cohort": 2019,
        "size": convert_file_size(await get_file_size(path)),
        "usageData": {
            "views": [],
            "summaries": [],
            "Explanations": [],
            "SampleQuestions": []
        },

        "aiData": {
            "title": "",
            "summary": ""
        },
    }
    try:
        reader = PdfReader(path)
        info["pageCount"]: len(reader.pages)
        if reader.metadata is not None:
            if reader.metadata.title is not None:
                info["title"] = reader.metadata.title
    except NullObject:
        pass
    return info


async def download_pdfs(links_and_keys):
    start = time.time()
    tasks = []
    for item in links_and_keys:
        url = item[0]
        name = item[1]
        print(f"Getting {name}")
        task = asyncio.create_task(download_pdf_async(url, name))
        tasks.append(task)
    await asyncio.gather(*tasks)


async def get_info_from_pdfs(names: List[str]):
    start = time.time()
    tasks = []
    for name in names:
        task = asyncio.create_task(get_pdf_data(name))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    print(f"Time check: {int(time.time() - start)}\n")
    return results
