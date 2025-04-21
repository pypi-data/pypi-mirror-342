def goodhello():
    print("YAY")
    return 1

def readFile(name):
    try:
        with open(name, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Exception: {e}")
        return False

def isValidJSONString(str):
    import json
    try:
        json.loads(str)
        return True
    except json.JSONDecodeError:
        return False

def timestamp(format="UNIX"):
    import time
    from datetime import datetime
    if format == "UNIX":
        return str(int(time.time()))
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))