import firebase_admin
import time
from firebase_admin import credentials, firestore

cred = credentials.Certificate("semester_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# get Universities
start = time.time()
print("getting uis")
print(f"Time check: {start}")
universities = db.collection("Universities").stream()

print("getting courses")
print(f"Time check: {time.time() - start}")
university = next(universities).to_dict()
courses = db.collection(f"Universities/{university['node']}/courses").stream()

for crs in courses:
    course = crs.to_dict()
    print(course["title"])
    print("getting course units")
    print(f"Time check: {time.time() - start}")
    courseUnits = db.collection(f"Universities/{university['node']}/courses/{course['code']}/courseUnits").stream()
    for unt in courseUnits:
        unit = unt.to_dict()
        print(unit)

# def get_notes(university_name, course_code, course_unit_code):
#     university_name = university_name.replace(" ", "")  # remove spaces
#     ref_path = f"Universities/{university_name}/courses/{course_code}/courseUnits/{course_unit_code}/notes"
#     ref = db.reference(ref_path)
#
#     data = ref.get()
#
#     return data
