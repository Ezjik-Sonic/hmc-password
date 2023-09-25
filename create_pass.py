import requests
import time
import hashlib, hmac
import json
import sys
import urllib.parse

current_GMT = time.gmtime()


hostname = sys.argv[1]
mode = sys.argv[2]
url = sys.argv[3]
public= sys.argv[4]
private= sys.argv[5]
projectID = '6' # UNIX
# projectID = '6' # test





def create_head(path, data=None):

    timestamp = str(int(time.time()))
    if data:
        unhashed = (f'{path}{timestamp}{str(data)}')
    else:
        unhashed = (f'{path}{timestamp}')

    hash_hmc = hmac.new(private.encode('utf-8'), unhashed.encode('utf-8'), hashlib.sha256).hexdigest()

    headers = {
        'X-Public-Key': public, 
        'X-Request-Hash': hash_hmc,
        'X-Request-Timestamp': timestamp,	
        'Content-Type': 'application/json; charset=utf-8',
    }

    return headers

def checkIfExists(hostname):
    path = 'api/v5/passwords/search'
    search_string = (f'/name:{hostname} username_email:root.json')
    urlencode = urllib.parse.quote(search_string)

    head = create_head(path + urlencode)
    url1 = url + path + urlencode

    listOfFound = requests.get(url1, headers=head, verify=False, auth=False)
    if listOfFound.ok:
        # Если мы выполняем только проверку, то полезно будет знать, есть ли похожие записи, но с другим именем.
        if mode == 'check':
            return listOfFound.json()

        # Поскольку поиск идет не по точному имени, а выводит все что содержит наш запрос,
        # то TPM возвращает нам лист из найденных записей и для каждой записи
        # необходимо выполнить дополнительную проверку на точное совпадение
        for password in listOfFound.json():
            if password['name'].lower() == hostname.lower():
                return password
    else:
        print(listOfFound.text)



def generatePassword():
    path = 'api/v5/generate_password.json'
    head = create_head(path=path)
    url1 = url + path
    newPassword = requests.get(url1, headers=head, verify=False, auth=False)
    if newPassword.ok:
        return newPassword.json()
    else:
        print(newPassword.text)


def create_password():
    path = 'api/v5/passwords.json'
    newPassword = generatePassword()
    data = json.dumps({"name": hostname, "project_id":6, "username": "root", "password": newPassword['password']})

    head = create_head(path=path, data=data)
    url1 = url + path

    r = requests.post(url1, headers=head, verify=False, data=data, auth=False)
    if r.ok:
        print (newPassword['password'])
    else:
        print(r.text)


def update_password(passwordID):
    newPassword = generatePassword()
    ID = passwordID['id']
    path = (f'api/v5/passwords/{ID}.json')
    data = json.dumps({"password": newPassword['password']})

    head = create_head(path=path, data=data)
    url1 = url + path
    r = requests.put(url1, headers=head, verify=False, data=data, auth=False)
    if r.ok:
        print (newPassword['password'])
    else:
        print(r.text)


def main():
    passwordID = checkIfExists(hostname)
    # print(passwordID)
    if passwordID and mode == 'update':
        update_password(passwordID)
    if not passwordID and mode == 'create':
        create_password()
    if mode == 'check':
        for password in passwordID:
            if password:
                print(f'ID: {password["id"]} - NAME: {password["name"]} - USERNAME: {password["username"]}')
            else:
                print(f'not found')

if __name__ == "__main__":
    main()






