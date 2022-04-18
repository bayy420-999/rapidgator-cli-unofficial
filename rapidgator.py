import requests, json, re
from os import sys
from configuration import configuration, write_token

def get_token(email, password):
    req = requests.get(f'https://rapidgator.net/api/v2/user/login?login={email}&password={password}').text
    resp = json.loads(req)['response']['token']
    print(f'Token successfully generated! token: {resp}')
    return resp

def download_file(url, token, download_path):
    if '?' in url:
        file_id = url.split('?')[0].split('/')[4]
    else:
        file_id = url.split('/')[4]

    base_url = f'https://rapidgator.net/api/v2/file/download?file_id={file_id}&token={token}'
    req = json.loads(requests.get(base_url).text)['response']['download_url']
    data = requests.get(req, stream = True)

    if 'Content-Disposition' in data.headers:
        header = resp.headers['Content-Disposition']
        filename = re.search('filename\=\"(.*?)\"', header).group().split('"')[1]

    with open(f'{download_path}{filename}', 'wb') as outfile:
        outfile.write(data.content)
        print(f'{filename} successfully saved!')

def main():
    email, password, token, download_path, is_batch_download, batch_file = configuration()
    print(
  '''
You need to login to get token which will be used to download the file(s), you dont need to generate token everytime you want to download file(s), but remember that the token will expire every few hours.\n
Choose your option:
1. Login
2. Download
  ''')
    answer = input('Your answer: ')
    if answer == '1':
        write_token(get_token(email, password))

    if answer == '2':
        if is_batch_download == True:
            with open(batch_file, 'r') as urls:
                for url in urls.read().split():
                    download_file(url, token, download_path)

        else:
            url = input('Input rapidgator url: ')
            download_file(url, token, download_path)

    answer = input('Do you want to use this program again? (y/n) ')
    if answer == 'y':
        main()
    elif answer == 'n':
        sys.exit(0)

if __name__ == '__main__':
    main()
