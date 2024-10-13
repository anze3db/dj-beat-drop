import os
import shutil
import zipfile
from io import BytesIO

import requests

from dj_beat_drop.utils import red, get_latest_django_version


def download_django(version):
    template_url = f"https://github.com/django/django/archive/refs/tags/{version}.zip"
    target_dir = f"/tmp/django_template/{version}"
    response = requests.get(template_url)
    if response.status_code != 200:
        red("Failed to download the Django template.")
    else:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(target_dir)

    return target_dir


def copy_template_dir(download_dir, latest_version, minor_version):
    template_dir_src = os.path.join(
        download_dir, f"django-{latest_version}/django/conf/project_template"
    )
    template_dir_dst = os.path.join(
        os.getcwd(), "src/dj_beat_drop/templates", minor_version
    )
    if os.path.exists(template_dir_dst):
        shutil.rmtree(template_dir_dst)
    shutil.copytree(template_dir_src, template_dir_dst)


def main():
    latest_version, minor_version = get_latest_django_version()
    download_dir = download_django(latest_version)
    copy_template_dir(download_dir, latest_version, minor_version)
    shutil.rmtree("/tmp/django_template")


if __name__ == "__main__":
    main()
