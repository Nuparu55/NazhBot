from pymongo import collection
import pymongo
import config
import re

client = pymongo.MongoClient(config.MONGO_CONN_STRING)
db = client['NazhBotDB']
notes = db['Notes']

def InsertNote(data):
    notes.insert_one({'note':data})

def GetNotes():
    notesQ = notes.find({})
    return notesQ

def DelNote(data:str):
    notes.delete_one({"note":re.compile(data, re.IGNORECASE)})

def NoteExist(data:str) -> bool:
    return (notes.find({"note":re.compile(data, re.IGNORECASE)}).count() > 0)

def ClearNotes():
    notes.delete_many({})