import os
import shutil
import sys
import datetime

import urllib3.util

from utils import tar_archive, oss_upload


def main():
    u: urllib3.util.Url = urllib3.util.parse_url(sys.argv[1].strip())

    shutil.rmtree(os.path.join("data", ".git"))

    tar_archive("data.tar", "data")

    print("data.tar created")

    key = "repos/" + u.hostname + "/" + \
          u.path.removesuffix(".git").lower().replace('/', '--') + "-" + \
          datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + \
          ".tar"

    print("upload to: " + key)

    oss_upload(key, "data.tar")

    print("done")


if __name__ == '__main__':
    main()
