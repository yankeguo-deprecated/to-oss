import os
import shutil
import subprocess

import oss2


def git_clone(output, url, lfs=False, purge=False):
    if lfs:
        subprocess.run(["git", "lfs", "install"], check=True)
    subprocess.run(["git", "clone", url, "--depth", '1', '--recursive', output], check=True)
    if purge:
        shutil.rmtree(os.path.join(output, ".git"))


def tar_archive(tar_file, src_file):
    subprocess.run(["tar", "-cvf", tar_file, src_file], check=True)


def curl_download(local_file: str, file_url: str):
    os.makedirs(os.path.dirname(local_file), exist_ok=True)

    subprocess.run([
        'curl',
        '-SL',
        '-o',
        local_file,
        file_url,
    ], check=True)


def oss_upload(key: str, local_file: str):
    print(f"uploading {local_file} to {key}")

    oss2.defaults.connection_pool_size = 5

    bucket = oss2.Bucket(
        oss2.Auth(os.getenv('OSS_ACCESS_KEY_ID'), os.getenv('OSS_ACCESS_KEY_SECRET')),
        os.getenv('OSS_ENDPOINT'),
        os.getenv('OSS_BUCKET'),
    )

    ctx = {'last_rate': 0}

    def progress_callback(consumed_bytes, total_bytes):
        if not total_bytes:
            return
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        if rate != ctx['last_rate']:
            print(f'uploading: {rate}%')
            ctx['last_rate'] = rate

    oss2.resumable_upload(
        bucket, key, local_file,
        multipart_threshold=100 * 1024 * 1024,
        progress_callback=progress_callback,
        num_threads=4,
    )
