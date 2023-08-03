import firebase_admin
import time
from firebase_admin import credentials, firestore

cred = credentials.Certificate("semester_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
reference = ""

# notes =>: universities > courses > course unit > notes

# get Universities
start = time.time()
print("getting uis")
print(f"Time check: {0}")

reference += "Universities"
universities = db.collection(reference).stream()
university = next(universities).to_dict()

print(university)
print("\n\n")
print("getting courses")
print(f"Time check: {int(time.time() - start)}")

reference += f"/{university['node']}/courses"
courses = db.collection(reference).stream()
for crs in courses:
    course = crs.to_dict()

    print(course["title"])
    print("\ngetting course units")
    print(f"Time check: {int(time.time() - start)}\n")

    reference += f"/{course['code']}/courseUnits"
    courseUnits = db.collection(reference).stream()
    for unt in courseUnits:
        another_ref = reference
        unit = unt.to_dict()

        print(unit["title"])
        print("\ngetting notes")
        print(f"Time check: {int(time.time() - start)}\n")
        another_ref += f"/{unit['code']}/notes"
        notes = db.collection(another_ref).stream()

        for nte in notes:
            note = nte.to_dict()
            print(note)

