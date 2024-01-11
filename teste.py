from pprint import pprint

from src.database import clean_file, read, save

data = [
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
    {"data": "aa", "dataa": "asas"},
]

save(data, "database.txt")

pprint(read("database.txt"))

clean_file("database.txt")
