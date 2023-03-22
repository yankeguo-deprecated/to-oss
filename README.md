# to-oss

download various resources and upload to aliyun oss

## How to use

**Basic Setup**

* Clone this repository to your own GitHub Account
* Set GitHub Actions Secrets:
    * `OSS_BUCKET`, OSS bucket name
    * `OSS_ENDPOINT`, endpoint of your oss bucket, 'https://oss-accelerate.aliyuncs.com' is suggested
    * `OSS_ACCESS_KEY_ID`
    * `OSS_ACCESS_KEY_SECRET`

**From `diffusers`**

Run GitHub Actions `from-diffusers` with Huggingface model id

**From `civitai`**

* Set GitHub Actions Secrets
    * `CIVITAI_TOKEN`

* Run GitHub Actions `from-civitai` with Civitai model sha256 checksum

**From `git`**

* Run GitHub Actions `from-git` with Git http url

**From `url`**

* Run GitHub Actions `from-url` with plain url

## Donation

See https://guoyk.xyz/donation

## Credits

Guo Y.K., MIT License
