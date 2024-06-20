import requests
import json
import yaml
import sys

def load_key():
    with open('LeakPy/data/api-keys.yaml') as file:
        api_key = yaml.safe_load(file)
    return api_key['api-keys']['leakcheck']['api-key']

def search_cred(email):
    url_base = 'https://leakcheck.io/api/v2/query/'
    api_key = load_key()
    headers = {'Accept': 'application/json',
               'X-API-Key': api_key}
    
    r = requests.get(url_base + email, headers=headers) 

    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error searching credentials for {email}: {r.status_code} - {r.text}")
        return None

def show_passwords(api_response):
    results = []
 
    if api_response.get('found', 0) > 0 and api_response.get('result'): 
        for entry in api_response['result']:
            if 'password' in entry:
                results.append(entry['password'])

    return results

def show_help(prog_name):
    print(f"Usage: {prog_name} <email file>")
    exit(0)

def main():
    if len(sys.argv) != 2:
        show_help(sys.argv[0])

    with open(sys.argv[1]) as emails_file:
        for email in emails_file:
            api_response = search_cred(email.strip())
            if api_response:
                passwords = show_passwords(api_response)
                for password in passwords:
                    print(password)

if __name__ == '__main__':
    main()
