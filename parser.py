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


def parse(sourceName, fileToParse, encoder, videoBitRate, template, source, screenshotsLinks):
    print("Source name will be set to %s" % sourceName)
    # Change the mediaInfo string into an array, each item in array is a line
    mediaInfo = getMediaInfo(fileToParse).splitlines()
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
    # Calculate video bit rate
    if "2160p" in mediaInfo[1]:
        # It's in the MediaInfo correct, so pull it out
        videoBitRate = int(mediaInfo[20].split(":")[1][1:-5])
    # For 1080p and 720p, MediaInfo rounds the video bit rate
    # So we take the overall bit rate, which isn't rounded, and
    # subtract the audio bitrate (640 for 1080p, 448 for 720p)
    elif "1080p" in mediaInfo[1]:
        overallBitRate = int(re.sub(" ","",mediaInfo[7].split(":")[1][1:-5]))
        videoBitRate = overallBitRate - 640
    elif "720p" in mediaInfo[1]:
        overallBitRate = int(re.sub(" ","",mediaInfo[7].split(":")[1][1:-5]))
        videoBitRate = overallBitRate - 448
    else:
        print("Title did not contain 2160p, 1080p, or 720p!!")
        print("Does not conform, exiting...")
        exit(-1)
    print("Video bit rate will be %d based upon MediaInfo calculation" % videoBitRate)
    print("Encoder will be %s" % encoder)
    print("NFO will be created titled '%s'" % nfoName)
    # Make screenshot formatting
    screenshots = ""
    for idx, link in enumerate(screenshotsLinks):
        # We only want to process every other
        if idx % 2 != 0 or idx == len(screenshotsLinks)-2:
            continue
        screenshots+=(link)
        screenshots+="  "
        screenshots+=(screenshotsLinks[idx+2])
        screenshots+="\n"
        screenshots+="\n"
    # Trim the last newlines to avoid spacing out the [/center] tag
    screenshots = screenshots.rstrip()
    # Make a new file from the template file
    copyfile(template,nfoName)
    fileIn = open(nfoName, "rt")
    fileData = fileIn.read()
    fileIn.close()
    # Replace everything in the new file we created
    fileData = fileData.replace("<SOURCE>", sourceName)
    fileData = fileData.replace("<CHAPTERS>", chapters)
    fileData = fileData.replace("<SIZE>", size)
    fileData = fileData.replace("<DURATION>", duration)
    fileData = fileData.replace("<VIDEO_BIT_RATE>", str(videoBitRate))
    fileData = fileData.replace("<RESOLUTION>", resolution)
    fileData = fileData.replace("<ENCODER>", encoder)
    fileData = fileData.replace("<SCREENS>",screenshots)
    fileOut = open(nfoName, "wt")
    fileOut.write(fileData)
    fileOut.close()
    print("Parsing complete, file created. Please check for errors!")
    return 1

if __name__ == '__main__':
    parser = ArgumentParser(description="Parses video files to create a NFO complying to BHDStudio standards via a TEMPLATE")
    parser.add_argument("--fileToParse", help="Media file you'd like to parse, full path or relative path accepted", default=None)
    parser.add_argument("--encoder", help="Encoder name you'd like to use in the NFO", default="Turing")
    parser.add_argument("--videoBitRate", help="Bit rate of the video for the NFO", default=None)
    parser.add_argument("--template", help="Template file to use", default="TEMPLATE.nfo")
    parser.add_argument("--source", help="Source of which you encoded the media from", default="<SOURCE>")
    #parser.add_argument("--automaticScreenshots", help="Automatic for automatic screenshot upload, manual for supplying the links")
    #parser.add_argument("--screenshotsFolder", help="If using automatic screenshots, you must specify the folder", required='--automaticScreenshots' in sys.argv)
    args = parser.parse_args()
    # Check to ensure the file to parse is a file we can read
    if args.fileToParse == None or not (os.access(args.fileToParse,os.R_OK)):
        print("Could not read file provided. Exiting")
        exit()
    if not (os.access(args.template,os.R_OK)):
        print("Could not read template file called %s, exiting" % args.template)

    #TODO: Check if screenshots folder is readable
    #TODO: Check if video file is something we can actually run mediaInfo on

    print("Arguments validated")
    print("Screenshot links required")
    print("Enter/Paste your links, then press Enter (might have to do it twice...)")
    screenshotsLinks = []
    while True:
        try:
            line = input()
            if not line:
                break
        except:
            break
        screenshotsLinks.append(line)
    if(len(screenshotsLinks) % 2 != 0):
        # Odd number of screenshots
        print("You must supply an even number of screenshots for before and after")
        exit(-1)
    parse(args.source, args.fileToParse, args.encoder, args.videoBitRate, args.template, args.source, screenshotsLinks)
    
