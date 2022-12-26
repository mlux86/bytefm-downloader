import json
import os
from urllib.parse import urlparse

import urllib3


def cookies_to_header(cookies):
    if cookies is None:
        return {}
    return {
        'Cookie': ';'.join(map(lambda cookie: f'{cookie["name"]}={cookie["value"]}', cookies))
    }


def get_json(url, cookies=None):
    headers = cookies_to_header(cookies)
    http = urllib3.PoolManager()
    r = http.request('GET', url, headers=headers, preload_content=False)
    return json.loads(r.data)


def download_file(url, path, cookies=None):
    headers = cookies_to_header(cookies)
    http = urllib3.PoolManager()
    r = http.request('GET', url, headers=headers, preload_content=False)
    with open(path, 'wb') as out:
        while True:
            data = r.read(2**16)
            if not data:
                break
            out.write(data)
    r.release_conn()


def file_name_from_url(url):
    a = urlparse(url)
    return os.path.basename(a.path)
