# to-oss

download various resources and upload to aliyun oss

## How to use

**Basic Setup**

* Clone this repository to your own GitHub Account
* Set [GitHub Actions Secrets](settings/secrets/actions):
    * `OSS_BUCKET`, OSS bucket name
    * `OSS_ENDPOINT`, endpoint of your oss bucket, 'https://oss-accelerate.aliyuncs.com' is suggested
    * `OSS_ACCESS_KEY_ID`
    * `OSS_ACCESS_KEY_SECRET`

**From `diffusers`**

Run [Github Actions](actions/workflows/from-diffusers.yml) with Huggingface model id

**From `civitai`**

* Set [GitHub Actions Secrets](settings/secrets/actions)
    * `CIVITAI_TOKEN`

* Run [Github Actions](actions/workflows/from-civitai.yml) with Civitai model checksum

## Donation

See https://guoyk.xyz/donation

## Credits

Guo Y.K., MIT License
