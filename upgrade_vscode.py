#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os, requests, sys
import shutil
import subprocess as sp

url = "https://vscode-update.azurewebsites.net/latest/linux-deb-x64/stable"
directory = "/home/asishbiswas/Downloads/vs-code-upgrade"
complete_file_name = directory + "/" + "vscode-stable.deb"


def cleanup():
    if os.path.exists(directory):
        shutil.rmtree(directory)


def install():
    print "\nInstalling latest vscode\n"
    sp.call(["sudo", "dpkg", "-i", complete_file_name])
    sp.call(["sudo", "apt", "install", "-f"])
    print "\nLatest vscode installation complete\n"


def download_latest_vscode():
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Couldn't access {} (error: {})".format(url, response.status_code))

    if not os.path.exists(directory):
        os.makedirs(directory)

    try:
        with open(complete_file_name, "wb") as f:
            chunk_size = 1024 * 1024  # 1MB
            downloaded = 0
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    downloaded += chunk_size
                    sys.stdout.write('\rDownloaded {:.2f} MB'.format(downloaded / chunk_size))
                    sys.stdout.flush()
                    f.write(chunk)
        sys.stdout.write('\rLatest version of VSCode Downloaded. ({:.2f} MB)\n'.format(downloaded / chunk_size))
    except:
        sys.stdout.write('\rDownload aborted\n')
        raise


def main():
    download_latest_vscode()
    install()
    cleanup()


if __name__ == "__main__":
    main()
