import sys
from datetime import datetime

import requests
import traceback
from html_tools.html_unpacker import fetch_dynamic_html


def get_html(url, use_selenium=False, timeout=10, use_content=False, scroll=True, sleep=10):
    try:
        if use_selenium:
            return fetch_dynamic_html(url)
        else:
            if use_content:
                return requests.get(url, timeout=timeout).content
            else:
                response = requests.get(url, timeout=timeout)
                html = response.text
            return html

    except Exception as e:
        print(f"Error fetching url {url}: {e}")
    return ""


PRINT_DEBUG_LOG = False
PRINT_DEBUG_WARNING = False
PRINT_DEBUG_ERROR = False

SAVE_DEBUG_LOG = False
SAVE_DEBUG_WARNING = False
SAVE_DEBUG_ERROR = False

debug_log_file = 'debug/logs.txt'
debug_log_file_details = 'debug/logsDetail.txt'
debug_warning_file = 'debug/warnings.txt'
debug_warning_file_details = 'debug/warningsDetail.txt'
debug_error_file = 'debug/errors.txt'
debug_error_file_details = 'debug/errorsDetail.txt'


def _build_stacktrace():
    import traceback
    return traceback.format_exc()


def _create_debug_row(content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stacktrace = _build_stacktrace()
    return {
        "regular": f"\nat{timestamp}:\n{content}\n\n",
        "detailed": f"\nat{timestamp}:\n{content}\n{stacktrace}\n\n"
    }


def _internal_debug(content, print_flag, save_flag, file, file_details):
    if print_flag:
        print(content)
        if isinstance(content, Exception):
            traceback.print_exc()
    if save_flag:
        row = _create_debug_row(content)
        with open(file, 'a') as f:
            f.write(row["regular"])
        with open(file_details, 'a') as f:
            f.write(row["detailed"])


def debug_log(content):
    _internal_debug(content, PRINT_DEBUG_LOG, SAVE_DEBUG_LOG, debug_log_file, debug_log_file_details)


def debug_warning(content):
    _internal_debug(content, PRINT_DEBUG_WARNING, SAVE_DEBUG_WARNING, debug_warning_file, debug_warning_file_details)


def debug_error(content):
    _internal_debug(content, PRINT_DEBUG_ERROR, SAVE_DEBUG_ERROR, debug_error_file, debug_error_file_details)


def console_input(message=""):
    if "--yes-to-all" in sys.argv:
        print(message)
        return ""
    return input(message)
