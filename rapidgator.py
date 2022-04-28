import os
import subprocess
import re
import json
from datetime import datetime

import requests

from configuration import configuration, write_token




api = 'https://rapidgator.net/api/v2'

def get_token(email, passwd):
    global api
    res = requests.get(f'{api}/user/login?login={email}&password={passwd}')
    token = json.loads(res.text)['response']['token']
    print(f'Token successfully generated! token: {token}')
    return token

# TODO: `name` cannot have `.html` i.e. user cannot download HTML files.
def extract_file_id_and_name(url):
    name = None
    if '.html?referer' in url:
        file_id, name = re.search('file/(.*?)/(.*?).html\?', url).groups()
    elif '?referer' in url:
        file_id = re.search('file/(.*?)\?referer', url).group(1)
    elif '.html' in url:
        file_id, name = re.search('file/(.*?)/(.*?).html', url).groups()
    else:
        file_id = re.search('file/(.*?)(?:/)?$', url).group(1)
    return file_id, name
         
def download_file(url, token, path):
    global api
    file_id, filename = extract_file_id_and_name(url)
    url = f'{api}/file/download?file_id={file_id}&token={token}'
    res = json.loads(requests.get(url).text)
    if not res['status'] == 200:
        return f'Error! {res}'
    url = res['response']['download_url']
    # If we have filename already, just download.
    if filename is not None:
        subprocess.run(['wget', '-O', os.path.join(path, filename), url])
        return f'File saved: {os.path.join(path, filename)}'
    # Otherwise, save a temp file with header in its first 10 lines.
    start_t = datetime.now().strftime('%Y%m%dT%H%M%S+08')
    tmp_name = str(os.path.join(path, start_t))
    subprocess.run(['wget', '--save-headers', '-O', tmp_name, url])
    # Now, get filename from header and remove it.
    header = subprocess.check_output(['head', '-10', tmp_name], text=True)
    if 'filename' in header:
        name = re.search('filename\=\"(.*?)\"', header).group(1)
        name = str(os.path.join(path, name))
        subprocess.run(['sed', '-i', '1,11d', tmp_name])
        subprocess.run(['mv', tmp_name, name])
        return f'File saved: {name}'
    # If the filename cannot be found, tell user.
    return f'Filename cannot be determined! File saved: {tmp_name}'

def main():
    email, passwd, token, path, is_batch_download, batch_file = configuration()
    
    if not os.path.isdir(path):
        os.mkdir(path)

    print('Login is needed every few hours to get a valid token.', end=' ')     
    if input('Login? [y/n]: ') in ['y', 'Y', 'yes', 'Yes']:
        write_token(get_token(email, passwd))

    if is_batch_download == True:
        with open(batch_file, 'r') as f:
            urls = f.readlines()
        for url in urls:
            print(download_file(url, token, path))
    else:
        url = input('Input rapidgator url: ')
        print(download_file(url, token, path))
    return

if __name__ == '__main__':
    main()
