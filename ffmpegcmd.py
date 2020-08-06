# -*- coding: UTF-8 -*-
import random


def createffmpegcmd(filePath, fileType, musicLength, bgvPath, timerColor,
                    infoColor, globalFont, infoFont, title, artist, rtmp):
    startt = random.randint(0, 8 * 60 - int(musicLength))
    cmdstring = (
        "ffmpeg -y -threads 0 -re -i \"" + filePath + "\" -ss " + str(startt) +
        " -i \"" + bgvPath + "\" -t " + str(musicLength) +
        #" -vf \"colorlevels=rimin=0.2:gimin=0.2:bimin=0.2:romax=0.9:gomax=0.9:bomax=0.9,vignette,"
        #for linux
        " -vf \"drawtext=text=\'%{pts\\:gmtime\\:0\\:%M\\\\\:%S}\':r=30:x=(w-tw)/2:y=h/8*5+h/8:fontsize=45:fontcolor="
        + timerColor + ":shadowcolor=0x482123ED:shadowx=2:shadowy=2,"
        " drawtext=fontfile=" + globalFont +
        ":text=*不支持点歌*:x=(w-tw)/2:y=h/25:fontsize=48:fontcolor=0xF84031:borderw=2:bordercolor=0xFDF1F6DD,"
        " drawtext=fontfile=" + globalFont +
        ":text=\'•\\\v•\\\v•\\\v•\':x=w/10:y=h/8:fontsize=32:fontcolor=white,"
        " drawtext=fontfile=" + globalFont +
        ":text=\'todo\\:切歌不断流\':x=w/7:y=(h-th)/12*11:fontsize=30:fontcolor=0xDDDDDD,"
        " drawtext=fontfile=" + globalFont +
        ":text=試\\\v試\\\v竖\\\v排:x=w/13*12:y=h/4:fontsize=40:fontcolor=0xAFAFAF,"
    )
    if title != "" and artist != "":  #信息非空
        if len(title) + len(artist) > 33:  #文字超长
            cmdstring += (
                " drawtext=fontfile=" + infoFont + ":text=\'" + title +
                "\':x=(w-tw)/2:y=h/7*4:fontsize=32:fontcolor=" + infoColor +
                ":borderw=2:bordercolor=0xFDF1F6DD,"
                " drawtext=fontfile=" + infoFont + ":text=\'" + artist +
                "\':x=(w-tw)/2:y=h/7*4+th*1.8:fontsize=32:fontcolor=" +
                infoColor + ":borderw=2:bordercolor=0xFDF1F6DD,")
        else:
            cmdstring += (" drawtext=fontfile=" + infoFont + ":text=\'" +
                          title + " - " + artist +
                          "\':x=(w-tw)/2:y=h/7*4:fontsize=32:fontcolor=" +
                          infoColor + ":borderw=2:bordercolor=0xFDF1F6DD,")
    cmdstring += " drawtext=fontfile=" + globalFont + ":text=\'%{localtime}\':x=w*8/10:y=h*11/12:fontsize=25:fontcolor=white:shadowcolor=0x6821C999:shadowx=2:shadowy=2\""
    if fileType == 'm4a':  #m4a直接拷贝音频流
        cmdstring += (
            " -vcodec libx264 -g 50 -b:v 500k -acodec copy -bufsize 1000k -preset ultrafast -f flv \""
            + rtmp + "\"")
    else:
        cmdstring += (
            " -vcodec libx264 -g 50 -b:v 500k -acodec aac -b:a 256k -bufsize 1000k -preset ultrafast -f flv \""
            + rtmp + "\"")
    return cmdstring
