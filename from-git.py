import sys
import datetime

import urllib3.util

from utils import tar_archive, oss_upload, git_clone


def main():
    git_url = sys.argv[1].strip()

    print("cloning repository")

    git_clone("data", git_url, lfs=True, purge=True)

    print("creating data.tar")

    tar_archive("data.tar", "data")

    print("data.tar created")

    u: urllib3.util.Url = urllib3.util.parse_url(git_url)

    key = "repos/" + u.hostname + "/" + \
          u.path.removeprefix("/").removesuffix(".git").lower().replace('/', '--') + "-" + \
          datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + \
          ".tar"

    print("upload to: " + key)

    oss_upload(key, "data.tar")

    print("done")


if __name__ == '__main__':
    main()
