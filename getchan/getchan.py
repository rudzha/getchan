import json
import os
import copy
import requests
import re


# Oh no, the evil regex
def extract_thread_info(url):
    url_pattern = re.compile("^.*/([a-z]+)/thread/(\d+)")
    matched_groups = re.match(url_pattern, url)
    return matched_groups.groups()


def make_api_url(board, thread):
    return "https://a.4cdn.org/{0}/thread/{1}.json".format(board, thread)


def make_cdn_url(board, content, extension):
    return "http://i.4cdn.org/{0}/{1}{2}".format(board, content, extension)


def make_request(url, headers=None):
    return requests.get(url, headers=headers)


# Preserve the original
def get_thread_posts(response):
    return tuple(copy.deepcopy(response.json()['posts']))


# TODO: Clean this mess up.
def watch_thread(state):
    thread, _, t_request, last_modified = state
    header = {'If-Modified-Since': last_modified} if last_modified is not None else {}
    response = t_request(header)
    if response.status_code == 200:
        last_modified = response.headers['Last-Modified']
        new_thread = get_thread_posts(response)
        new_posts = tuple(filter(lambda x: x not in thread, new_thread))
        combined_thread = thread + new_posts
        print(new_posts)
        return combined_thread, new_posts, t_request, last_modified
    elif response.status_code == 304:
        return thread, (), t_request, last_modified
    else:
        raise StopIteration


def write_json(location, name, threads):
    post_dict = {"posts": list(threads)}
    post_json_string = json.dumps(post_dict)
    with open("{0}/{1}.json".format(location, name), "w") as file:
        file.write(post_json_string)


def mkdir(board, thread):
    path = "./{0}_{1}".format(board, thread)
    (os.makedirs(path, exist_ok=True))
    return path


def download_content(url_fun, location, file_and_ext):
    print(os.getpid(), file_and_ext)
    file, ext = file_and_ext
    r = make_request(url_fun(file, ext))
    out_file = "{0}/{1}{2}".format(location, *file_and_ext)
    if r.status_code == 200:
        with open(out_file, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return out_file


def extract_content(item):
    if 'tim' in item.keys():
        return item['tim'], item['ext']
