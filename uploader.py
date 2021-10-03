import os
import json
from colorama import Fore, Style
from argparse import ArgumentParser

def startup():
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

    torrentPasskey = os.getenv("TORRENTPASSKEY")
    if torrentPasskey == None or len(torrentPasskey) != 32:
        print(Fore.RED + "Torrent Passkey not entered or formatted correctly" + Fore.WHITE)
        exit(0)
    bhdApiKey = os.getenv("BHDAPIKEY")
    bhdUrl = os.getenv("BHDUPLOADURL")
    logLocation = os.getenv("x")
    mediaFolder = os.getenv("MEDIAFOLDER")
    screenshotsFolder = os.getenv("SCREENSHOTSFOLDERNAME")



if __name__ == '__main__':
    print(Fore.GREEN + "Welcome to BHDStudio Uploader")
    print("Loading in .env file...")
    startup()
    