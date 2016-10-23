#!/usr/bin/env python3
import argparse
from functools import reduce

from getchan import *


# TODO: Handle Duplicate Original Thread
# TODO: Incremental timeout
# TODO: Directories
# TODO: Non-blocking image download


def main(args):
    thread_string = args.thread
    board, thread = extract_thread_info(thread_string)
    json_api_url = make_api_url(board, thread)
    cdn_url = partial(make_cdn_url, board)
    api_request = partial(make_request, json_api_url)
    results = iterate(watch_thread, (api_request, 15, (), cdn_url, None))
    final_result = reduce(lambda x, y: y, results)
    _, _, final_thread, _, _ = final_result
    write_json(thread, final_thread)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download 4chan threads")
    parser.add_argument('thread', metavar='thread', help="Pass the link to the thread")
    arguments = parser.parse_args()
    main(arguments)
