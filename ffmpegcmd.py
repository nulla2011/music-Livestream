# -*- coding: UTF-8 -*-
import random
import math


def createffmpegcmd(filePath, fileType, musicLength, offset, bgvPath,
                    timerColor, infoColor, timerShadow, infoShadow, globalFont,
                    infoFont, timerFont, title, artist, rtmp):
    startt = random.randint(0, 8 * 60 - int(musicLength))
    if int(offset) < 10:
        offsetstr = '0' + offset
    else:
        offsetstr = offset
    cmdstring = (
        "ffmpeg -y -threads 0 -re -itsoffset 00:00:" + offsetstr + " -i \"" +
        filePath + "\" -ss " + str(startt) + " -i \"" + bgvPath + "\" -t " +
        str(musicLength + int(offset)) +
        #" -vf \"colorlevels=rimin=0.2:gimin=0.2:bimin=0.2:romax=0.9:gomax=0.9:bomax=0.9,vignette,"   
        " -vf \"movie=chi.mp4:loop=0,scale=192x108,setpts=N/FRAME_RATE/TB[gif];[0:v][gif]overlay=x=0:y=615:shortest=1:eof_action=pass,"
        #播放时间 
        # #for linux,it is 10 backslashs before %S; for windows, is 5
        "drawtext=text=\'%{pts\\:gmtime\\:0\\:%M\\\\\\\\\\:%S}\':r=30:x=(w-tw)/2:y=h/4*3-th+h/16:fontfile="
        + timerFont + ":fontsize=45:fontcolor=" + timerColor +
        ":shadowcolor=" + timerShadow + ":shadowx=2:shadowy=2,"
        #上方注意
        " drawtext=fontfile=" + globalFont +
        ":text=*不支持点歌*:x=(w-tw)/2:y=h/25:fontsize=48:fontcolor=0xF84031:borderw=2:bordercolor=0xFDF1F6DD,"
        #左上说明
        " drawtext=fontfile=" + globalFont +
        ":text=\'\• 使用vps+自制程序（已开源）随机播放库中的音乐\':x=w/14:y=h/7:fontsize=32:fontcolor=0xFFFFFFBB,"
        " drawtext=fontfile=" + globalFont +
        ":text=\'\• 几年前的歌曲库了，正在准备整理传新歌\':x=w/14:y=h/7+th*1.5:fontsize=32:fontcolor=0xFFFFFFBB,"
        " drawtext=fontfile=" + globalFont +
        ":text=\'\• 不支持点歌，因为没bu流hui量xie\':x=w/14:y=h/7+th*1.5*2:fontsize=32:fontcolor=0xFFFFFFBB,"
        " drawtext=fontfile=" + globalFont +
        ":text=\'\• 如果视频画面停住请刷新\':x=w/14:y=h/7+th*1.5*3:fontsize=32:fontcolor=0xFFFFFFBB,"
        #左下todo
        " drawtext=fontfile=" + globalFont +
        ":text=\'todo\\:切歌不断流\':x=w/7:y=(h-th)/12*11:fontsize=30:fontcolor=0xDDDDDD,"
        #test
        " drawtext=fontfile=" + globalFont +
        ":text=試\\\v試\\\v竖\\\v排:x=w/13*12:y=h/4:fontsize=40:fontcolor=0xAFAFAF,"
    )
    #歌曲信息
    if title != "" and artist != "":  #信息非空
        if len(title) + len(artist) > 33:  #文字超长
            cmdstring += (
                " drawtext=fontfile=" + infoFont + ":text=\'" + title +
                "\':x=(w-tw)/2:y=h/19*10:fontsize=40:fontcolor=" + infoColor +
                ":borderw=2:bordercolor=" + infoShadow + ","
                " drawtext=fontfile=" + infoFont + ":text=\'" + artist +
                "\':x=(w-tw)/2:y=h/19*10+th*2:fontsize=32:fontcolor=" +
                infoColor + ":borderw=2:bordercolor=" + infoShadow + ",")
        else:
            cmdstring += (" drawtext=fontfile=" + infoFont + ":text=\'" +
                          title + " - " + artist +
                          "\':x=(w-tw)/2:y=h/19*10:fontsize=34:fontcolor=" +
                          infoColor + ":borderw=2:bordercolor=" + infoShadow +
                          ",")
    #右下当前日期时间
    cmdstring += (
        " drawtext=fontfile=" + globalFont +
        ":text=\'%{localtime}\':x=w*10/13:y=h*11/12:fontsize=25:fontcolor=white:shadowcolor=0x6821C999:shadowx=2:shadowy=2\""
    )
    if fileType == 'm4a':  #m4a直接拷贝音频流
        cmdstring += (
            " -vcodec libx264 -g 50 -b:v 700k -acodec copy -bufsize 2000k -maxrate 1100k -preset ultrafast -f flv \""
            + rtmp + "\"")
    else:
        cmdstring += (
            " -vcodec libx264 -g 50 -b:v 700k -acodec aac -b:a 256k -bufsize 2000k -maxrate 1100k -preset ultrafast -f flv \""
            + rtmp + "\"")
    return cmdstring
