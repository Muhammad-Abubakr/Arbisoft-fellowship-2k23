persons_data = [
    {
        "name": "John Doe",
        "age": 30,
        "occupation": "Engineer",
        "city": "New York",
        "email": "john.doe@example.com"
    },
    {
        "name": "Jane Smith",
        "age": 28,
        "occupation": "Designer",
        "city": "Los Angeles",
        "email": "jane.smith@example.com"
    },
    {
        "name": "Michael Johnson",
        "age": 35,
        "occupation": "Teacher",
        "city": "Chicago",
        "email": "michael.johnson@example.com"
    }
]

def key_exists(dict, key):
    print(dict.keys())
    if key in dict.keys():
        return True
    else:
        return False
    
for each in persons_data:
    print(key_exists(each, "name"))
    
