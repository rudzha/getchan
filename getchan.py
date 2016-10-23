import json
from functools import partial
from itertools import accumulate, repeat
from time import sleep

import requests


def iterate(f, x):
    return accumulate(repeat(x), lambda fx, _: f(fx))


def extract_thread_info(url):
    url_elements = url.split('/')
    return url_elements[3], url_elements[5]


def make_api_url(board, thread):
    return "https://a.4cdn.org/{0}/thread/{1}.json".format(board, thread)


def make_cdn_url(board, content, extension):
    return "http://i.4cdn.org/{0}/{1}{2}".format(board, content, extension)


def make_request(url, headers=None):
    return requests.get(url, headers=headers)


def get_thread_posts(response):
    return tuple(response.json()['posts']) if response.status_code == 200 else ()


def watch_thread(state):
    t_request, timeout, thread, cdn_url, last_modified = state
    if last_modified is not None:
        header = {'If-Modified-Since': last_modified}
    else:
        header = {}
    response = t_request(header)
    if response.status_code == 200:
        download = partial(download_content, cdn_url)
        last_modified = response.headers['Last-Modified']
        new_thread = (get_thread_posts(response))
        new_posts = complement_right(thread, new_thread)
        new_content = filter(None, map(extract_content, new_posts))
        list(map(download, new_content))
        combined_thread = thread + new_posts
        sleep(timeout)
        return t_request, timeout, combined_thread, cdn_url, last_modified
    elif response.status_code == 304:
        sleep(timeout)
        return t_request, timeout, thread, cdn_url, last_modified
    else:
        raise StopIteration


def complement_right(a, b):
    return tuple(item for item in b if item not in a)


def write_json(name, threads):
    post_dict = {"posts": list(threads)}
    post_json_string = json.dumps(post_dict)
    with open("{0}.json".format(name), "w") as file:
        file.write(post_json_string)


def download_content(url_fun, file_and_ext):
    file, ext = file_and_ext
    print(file, ext)
    print(url_fun(file, ext))
    r = make_request(url_fun(file, ext))
    if r.status_code == 200:
        with open("{0}{1}".format(*file_and_ext), "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return file


def extract_content(item):
    if 'tim' in item.keys():
        return item['tim'], item['ext']
