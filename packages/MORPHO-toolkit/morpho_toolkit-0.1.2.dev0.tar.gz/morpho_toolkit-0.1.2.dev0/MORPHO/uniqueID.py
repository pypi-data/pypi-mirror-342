import uuid
import time
import random
import string
import os

def _loadCounter():
    try:
        with open("counter.txt", "r") as f:
            return int(f.read().strip())
    except FileNotFoundError:
        return 0
    
def _saveCounter(counter):
    with open("counter.txt", "w") as f:
        f.write(str(counter))

def generateUUID():
    return str(uuid.uuid4())

def timestampID():
    return str(int(time.time()))

def randomID():
    timestamp = str(int(time.time()))
    randomChars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ID-{timestamp}-{randomChars}"

def customID(prefix="ID"):
    counter = _loadCounter()
    counter += 1
    _saveCounter(counter)
    timestamp = str(int(time.time()))
    return f"{prefix}-{counter:06d}"

def customID(prefix="ID"):
    counter = _loadCounter()
    counter += 1
    _saveCounter(counter)
    timestamp = str(int(time.time()))
    return f"{prefix}-{counter:06d}"

def resetCounter(): #resets counter
    _saveCounter(0)
