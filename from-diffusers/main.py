import datetime
import os
import subprocess
import sys
import oss2
import torch
import re
from diffusers import StableDiffusionPipeline

re_bad_filename = re.compile(r'[^0-9a-zA-Z-]+')


def main():
    model_id = sys.argv[1].strip()

    print("model_id: " + model_id)

    os.makedirs("data", exist_ok=True)

    model = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    model.save_pretrained("data", safe_serialization=True)

    print("downloaded")

    subprocess.run(["tar", "-cvf", "data.tar", "data"], check=True)

    print("data.tar created")

    oss2.defaults.connection_pool_size = 5

    bucket = oss2.Bucket(
        oss2.Auth(os.getenv('OSS_ACCESS_KEY_ID'), os.getenv('OSS_ACCESS_KEY_SECRET')),
        os.getenv('OSS_ENDPOINT'),
        os.getenv('OSS_BUCKET'),
    )

    key = "models/huggingface/diffusers/" + \
          re_bad_filename.sub('-', model_id) + \
          "-" + \
          datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + \
          ".tar"

    print("upload to: " + key)

    ctx = {'last_rate': 0}

    def progress_callback(consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            if rate != ctx['last_rate']:
                print(f'uploading: {rate}%')
                ctx['last_rate'] = rate

    oss2.resumable_upload(
        bucket, key, "data.tar",
        multipart_threshold=100 * 1024 * 1024,
        progress_callback=progress_callback,
        num_threads=4,
    )

    print("done")


if __name__ == "__main__":
    main()
