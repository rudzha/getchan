#!/usr/bin/env python3
import argparse
from time import sleep
from functools import partial
from toolz.itertoolz import iterate
from multiprocessing import Pool
from toolz.curried import map, filter, pipe

from getchan import extract_thread_info, mkdir, make_api_url, make_cdn_url, download_content, write_json, make_request, watch_thread, extract_content


def main(args):
    thread_string = args.thread
    board, thread = extract_thread_info(thread_string)

    download_location = mkdir(board, thread)
    download_pool = Pool(4)

    json_api_url = make_api_url(board, thread)
    cdn_url = partial(make_cdn_url, board)

    download = partial(download_content, cdn_url, download_location)
    write_json_to_dir = partial(write_json, download_location)
    api_request = partial(make_request, json_api_url)

    results_it = iterate(watch_thread, ((), (), api_request, None))
    final_result = ()

    # Priming that iterator, to get that instant download
    next(results_it)

    for result in results_it:
        final_result = result
        downloadable_content = pipe(result[1],
                                    map(extract_content),
                                    filter(None)
                                    )

        download_pool.map_async(download, downloadable_content)
        sleep(30)

    final_thread = list(final_result)[0]
    write_json_to_dir(thread, final_thread)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download 4chan threads")
    parser.add_argument('thread', metavar='thread', help="Pass the link to the thread")
    arguments = parser.parse_args()
    main(arguments)
