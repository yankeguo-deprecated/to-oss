import datetime
import os
import subprocess
import sys
import oss2
import torch
import re
from diffusers import StableDiffusionPipeline

from utils import tar_archive, oss_upload

re_bad_filename = re.compile(r'[^0-9a-zA-Z-]+')


def main():
    model_id = sys.argv[1].strip()

    print("model_id: " + model_id)

    os.makedirs("data", exist_ok=True)

    model = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    model.save_pretrained("data", safe_serialization=True)

    print("downloaded")

    tar_archive("data.tar", "data", remove=True)

    print("data.tar created")

    key = "models/huggingface/diffusers/" + \
          re_bad_filename.sub('-', model_id) + \
          "-" + \
          datetime.datetime.now().strftime('%Y%m%d-%H%M%S') + \
          ".tar"

    print("upload to: " + key)

    oss_upload(key, "data.tar")

    print("done")


if __name__ == "__main__":
    main()
