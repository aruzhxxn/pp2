# json.py

import json

# python dictionary
student = {
    "name": "Aruzhan",
    "age": 17,
    "city": "Almaty"
}

# python → json
json_text = json.dumps(student)
print(json_text)

# write to file
with open("student.json", "w") as f:
    json.dump(student, f)

# read from file
with open("student.json", "r") as f:
    data = json.load(f)

print(data)