from argparse import ArgumentParser
from pymediainfo import MediaInfo
from shutil import copyfile
import os
import re


# Function for getting the raw mediaInfo
def getMediaInfo(path):
    mediaInfo = MediaInfo.parse(path,output="STRING",full=False)
    mediaInfo=mediaInfo.encode(encoding="utf8")
    mediaInfo=mediaInfo.decode('utf8','strict')
    return mediaInfo


if __name__ == '__main__':
    parser = ArgumentParser(description="Parses video files to create a NFO complying to BHDStudio standards via a TEMPLATE")
    parser.add_argument("--fileToParse", help="Media file you'd like to parse, full path or relative path accepted", default=None)
    parser.add_argument("--encoder", help="Encoder name you'd like to use in the NFO", default="Turing")
    parser.add_argument("--videoBitRate", help="Bit rate of the video for the NFO", default=None)
    parser.add_argument("--template", help="Template file to use", default="TEMPLATE.nfo")
    parser.add_argument("--source", help="Name of the source you used to encode the media", default=None)

    # Check to ensure the file to parse is a file we can read
    args = parser.parse_args()
    if args.fileToParse == None or not (os.access(args.fileToParse,os.R_OK)):
        print("Could not read file provided. Exiting")
        exit()
    if not (os.access(args.template,os.R_OK)):
        print("Could not read template file called %s, exiting" % args.template)

    #TODO: Check if video file is something we can actually run mediaInfo on

    print("Arguments validated")

    # Change the mediaInfo string into an array, each item in array is a line
    mediaInfo = getMediaInfo(args.fileToParse).splitlines()
    # Find the name of the NFO based on the name of the video file
    nfoName = mediaInfo[1].split(":")[1][1:]
    nfoName = nfoName[:-3]
    nfoName += "nfo"
    chapters = "Named"
    # Determine if the chapters are named or numbered
    for n in mediaInfo:
        if "00:00:00.000" in n:
            firstChapter = n.split(":")[3][1:]
            if firstChapter == "Chapter 1":
                chapters = mediaInfo[-2].split(":")[3][9:]  

    if chapters == "Named":
        print("Chapters appear to be NAMED based on MediaInfo")
    else:
        print("Chapters appears to be NUMBERED based on MediaInfo, (1-%s)" % chapters)
    # Get size of the file
    size = mediaInfo[5].split(":")[1][1:]
    print("File size is %s, based on MediaInfo" % size)
    # Get duration of the media
    duration = mediaInfo[6].split(":")[1][1:]
    print("Duration is %s, based on MediaInfo" % duration)
    # Here we have to check and make sure it's the correct line, since 4K media has it stored on
    # a different line
    if "Width" in mediaInfo[23]:
        width = re.sub(" ","",mediaInfo[23].split(":")[1][1:-7])
        height = mediaInfo[24].split(":")[1][1:-7]
        aspectRatio = mediaInfo[25].split(":")[1][1:]
    elif "Width" in mediaInfo[24]:
        width = re.sub(" ","",mediaInfo[24].split(":")[1][1:-7])
        height = mediaInfo[25].split(":")[1][1:-7]
        aspectRatio = mediaInfo[26].split(":")[1][1:]
    # Create resolution string
    resolution = width + " x " + height + " (" + aspectRatio + ")"
    print("Resolution is %s, based on MediaInfo" %resolution)
    print("Encoder will be %s" % args.encoder)
    print("NFO will be created titled '%s'" % nfoName)
    # Make a new file from the template file
    copyfile(args.template,nfoName)
    fileIn = open(nfoName, "rt")
    fileData = fileIn.read()
    fileIn.close()
    # Replace everything in the new file we created
    fileData = fileData.replace("<CHAPTERS>", chapters)
    fileData = fileData.replace("<SIZE>", size)
    fileData = fileData.replace("<DURATION>", duration)
    fileData = fileData.replace("<RESOLUTION>", resolution)
    fileData = fileData.replace("<ENCODER>", args.encoder)
    fileOut = open(nfoName, "wt")
    fileOut.write(fileData)
    fileOut.close()
    print("Parsing complete, file created. Please check for errors!")
    exit(1)
