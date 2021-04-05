# BHDStudio
Repo for the BHDStudio Toolset I am working on. 

## Parser

Parser inputs a video file, and creates a NFO based on the MediaInfo output of said file

Default template is included as TEMPLATE.nfo.

Automatically writes over an existing NFO of the same name

    Options:
        -h --help     Show this screen.
        --fileToParse <fileToParse> Media file you'd like to parse, full path or relative path accepted", default=None)
        --encoder <encoder> Encoder name you'd like to use in the NFO", default="Turing")
        --videoBitRate <videoBitRate> Bit rate of the video for the NFO", default=None)
        --template <template> Template file to use", default="TEMPLATE.nfo")
        --source <source> Name of the source you used to encode the media", default=None)

Installation

    1) Install Python3 for Windows: https://www.python.org/downloads/
        * You probably want to check the box to have Python3 added to your PATH variable
    2) Pip should be installed, verify with `pip -V`
        * If not, install pip3: https://phoenixnap.com/kb/install-pip-windows
    3) Install required pip packages (this will be streamlined in the future)
        * pip install pymediainfo


Usage:

    python parser.py --fileToParse <MEDIA_FILE> --encoder <YOUR_NAME> --source <NAME_OF_SOURCE> 
    When prompted, copy/paste your screenshots in


## Uploader

Uses the parser to create the NFO, then creates a torrent file and uploads it via your API key
