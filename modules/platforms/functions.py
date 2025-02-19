import requests
from hashlib import md5


def get_resource(tmp_dir, url, platformName):
    domainList = requests.get(url, allow_redirects=True)
    open(F"{tmp_dir}{platformName}.json", 'wb').write(domainList.content)


def generate_program_key(programName, programURL):
    program_key = md5(
        f"{programName}|{programURL}".encode('utf-8')).hexdigest()
    return program_key


def find_program(db, platformName, programKey):
    data = db[platformName].find_one({'programKey': programKey})
    return data


def remove_elements(array1, array2):
    for element in array2:
        array1.remove(element)


def save_data(db, platformName, programKey, dataJson):
    db[platformName].update_one({'programKey': programKey}, {
        '$set': dataJson}, upsert=True)

def check_program_type(data,watcherData,notifications):
    pt_notify_status = False
    if data['isNewProgram']:
        
        if data['programType'] == "rdp" and notifications['watch_rdp']:
            pt_notify_status = True
        elif data['programType'] == "vdp" and notifications["watch_vdp"]: 
            pt_notify_status = True
    else:
        if watcherData['programType'] == "rdp" and notifications['watch_rdp']:
            pt_notify_status = True
        elif watcherData['programType'] == "vdp" and notifications["watch_vdp"]: 
            pt_notify_status = True   
    return pt_notify_status  
    