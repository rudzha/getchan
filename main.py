#!/usr/bin/env python3
import argparse
from functools import partial
from time import sleep

from getchan import *


# TODO: Handle Duplicate Original Thread
# TODO: Incremental timeout
# TODO: Non-blocking image download
# TODO: Proper Python packaging, setuptools, etc


def main(args):
    thread_string = args.thread
    board, thread = extract_thread_info(thread_string)

    download_location = mkdir(board, thread)
    json_api_url = make_api_url(board, thread)
    cdn_url = partial(make_cdn_url, board)
    download = partial(download_content, cdn_url, download_location)
    write_json_to_dir = partial(write_json, download_location)
    api_request = partial(make_request, json_api_url)

    results_it = iterate(watch_thread, ((), (), api_request, None))

    final_result = ()
    for result in results_it:
        # Evil mutation, how to get rid, pls?
        final_result = result
        list(map(download, result[1]))
        sleep(30)

    final_thread = list(final_result)[0]
    write_json_to_dir(thread, final_thread)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download 4chan threads")
    parser.add_argument('thread', metavar='thread', help="Pass the link to the thread")
    arguments = parser.parse_args()
    main(arguments)
