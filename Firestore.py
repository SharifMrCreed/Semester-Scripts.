import firebase_admin
import time
from firebase_admin import credentials, firestore
from pdfUtils import *
import asyncio

cred = credentials.Certificate("semester_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
reference = ""

# notes =>: universities > courses > course units > notes

# get Universities
start = time.time()
print("getting uis")

reference += "Universities"
universities = db.collection(reference).stream()
university = next(universities).to_dict()

print(university)
print(f"Time check: {int(time.time() - start)}\n")

start = time.time()
print("getting courses")
reference += f"/{university['node']}/courses"
courses = db.collection(reference).stream()
print(f"Time check: {int(time.time() - start)}\n")
start = time.time()

for crs in courses:
    course = crs.to_dict()
    cu_start = time.time()
    print(course["title"])
    print("\ngetting course units")
    reference += f"/{course['code']}/courseUnits"
    courseUnits = db.collection(reference).stream()

    with open("LocalFiles/notes.json", "w") as file:
        for unt in courseUnits:
            another_ref = reference
            unit = unt.to_dict()

            print(f"\nGetting {unit['title']} notes")
            notes_start = time.time()
            another_ref += f"/{unit['code']}/notes"
            nts = db.collection(another_ref).stream()
            notes = [note.to_dict() for note in nts]
            asyncio.run(
                download_pdfs([[note['downloadLink'], note['id']] for note in notes])
            )
            info_list = asyncio.run(
                get_info_from_pdfs(notes)
            )
            for item in info_list:
                db.collection(another_ref).document(item['id']).set(
                    item, merge=True
                )
                file.write(f"{str(item)},\n")
            print(f"Time check {unit['title']} notes: {int(time.time() - notes_start)}\n")

        print(f"Time check Course Units: {int(time.time() - cu_start)}\n")

print(f"Time check Course: {int(time.time() - start)}\n")
