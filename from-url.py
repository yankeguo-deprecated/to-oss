import posixpath
import sys

import urllib3.util

from utils import oss_upload, curl_download


def main():
    remote_url = sys.argv[1].strip()

    u: urllib3.util.Url = urllib3.util.parse_url(remote_url)

    filename = posixpath.basename(u.path)

    print(f"downloading {filename}")

    curl_download(filename, remote_url)

    key = "files/" + u.hostname + u.path

    print(f"uploading {key}")

    oss_upload(key, filename)

    print("done")


if __name__ == '__main__':
    main()
