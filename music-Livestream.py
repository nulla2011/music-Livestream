# -*- coding: UTF-8 -*-
import os
import sys
import random
import configparser
from configparser import Error
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.id3 import ID3

conf = configparser.ConfigParser()
try:
    conf.read("music-Livestream.ini")
    rtmp = conf.get('main', 'rtmp_url')
    musicpath = conf.get('main', 'musicpath')
    videopath = conf.get('main', 'videopath')
    bgvPath=conf.get('main', 'bgvPath')
    timercolor = conf.get('colors', 'timercolor')
    infocolor = conf.get('colors', 'infocolor')
    globalfont = conf.get('fonts', 'globalfont')
    infofont = conf.get('fonts', 'infofont')
    enableVideo = int(conf.get('main', 'enableVideo'))
except Exception:
    print("config file not correct! creating,,,")
    os.system("rename music-Livestream.ini music-Livestream.ini.bak")
    os.system(
        "cp music-Livestream_example.ini music-Livestream.ini")  #for linux
    sys.exit(0)
maxlength = 7 * 60 + 15
fileList = []


def getMusicFile(path):
    try:
        currentList = os.listdir(path)
    except FileNotFoundError:
        print("path not found,please check music-Livestream.ini")
        sys.exit(0)
    for eachF in currentList:
        tempPath = path + '/' + eachF
        if os.path.isfile(tempPath):
            if eachF.endswith('.flac'):
                fileList.append([tempPath, 'flac'])
            elif eachF.endswith('.mp3'):
                fileList.append([tempPath, 'mp3'])
            elif eachF.endswith('.m4a'):
                fileList.append([tempPath, 'm4a'])
            else:
                continue
        else:
            getMusicFile(tempPath)


def getVideoFile(path):
    try:
        currentList = os.listdir(path)
    except FileNotFoundError:
        print("path not found,please check music-Livestream.ini")
        sys.exit(0)
    for eachF in currentList:
        tempPath = path + '/' + eachF
        if os.path.isfile(tempPath):
            if eachF.endswith('.flv'):
                fileList.append([tempPath, 'flv'])
            elif eachF.endswith('.mp4'):
                fileList.append([tempPath, 'mp4'])
            else:  #不存mkv格式的短视频，所以不考虑mkv；ts仅用于生放，所以也不考虑ts
                continue
        else:
            getVideoFile(tempPath)


def ftype(s):
    if s == "mp3" or s == "flac" or s == "m4a":
        return 1
    elif s == "mp4" or s == "flv":
        return 2
    else:
        return -1


def main(argv):
    while True:
        global fileList
        if len(argv) >= 2:
            if argv[1] == "music":
                getMusicFile(musicpath)
            elif argv[1] == "video":
                if enableVideo:
                    getVideoFile(videopath)
                else:
                    print("video not enabled,check music-Livestream.ini")
                    return (-1)
            elif argv[1] == "-s":
                if len(argv) < 3:
                    print("param ERROR!")
                    return -1
                else:
                    getMusicFile(musicpath)
                    if enableVideo: getVideoFile(videopath)
                    resultList = []
                    for f in fileList:
                        if (f[0].find(argv[2]) != -1):
                            resultList.append(f)
                    if len(resultList) == 0:
                        print("not fond!")
                        return -1
                    else:
                        fileList.clear()
                        fileList = resultList.copy()
            else:
                getMusicFile(musicpath)
                if enableVideo: getVideoFile(videopath)
        else:
            getMusicFile(musicpath)
            if enableVideo: getVideoFile(videopath)
        try:
            ran = random.randint(0, len(fileList) - 1)
        except ValueError:
            print("no file fond")
            continue
        if ftype(fileList[ran][1]) == 1:
            title = ""
            artist = ""
            artistList = []
            if fileList[ran][1] == 'flac':
                audio = FLAC(fileList[ran][0])
                for meta in audio.tags:
                    if (meta[0] == 'TITLE' or meta[0] == 'Title'):
                        title = meta[1].replace('\x00', '')  #部分结尾有谜之字符
                    if (meta[0] == 'ARTIST' or meta[0] == 'Artist'):
                        artistList.append(meta[1].replace('\x00', ''))  #部分结尾有谜之字符
                artist = "/".join(artistList)
                musicLength = audio.info.length
                if musicLength > maxlength:
                    print("too long")
                    continue
            elif fileList[ran][1] == 'mp3':
                audio = MP3(fileList[ran][0])
                musicLength = audio.info.length
                if musicLength > maxlength:
                    print("too long")
                    continue
                else:
                    audio = ID3(fileList[ran][0])
                    artist = audio['TPE1'].text[0]
                    title = audio["TIT2"].text[0]
            elif fileList[ran][1] == 'm4a':
                audio = MP4(fileList[ran][0])
                musicLength = audio.info.length
                if musicLength > maxlength:
                    print("too long")
                    continue
                else:
                    title = audio.tags['\xa9nam'][0]
                    artist = audio.tags['\xa9ART'][0]
            else:
                continue
            try:
                startt=random.randint(0,8*60-int(musicLength))
                ffmpegcmd = (
                    "ffmpeg -y -threads 0 -re -i \"" + fileList[ran][0] +
                    "\" -ss "+str(startt)+" -i \"" +bgvPath+"\" -t "+
                    str(musicLength) +
                    #" -vf \"colorlevels=rimin=0.2:gimin=0.2:bimin=0.2:romax=0.9:gomax=0.9:bomax=0.9,vignette,"
                    #for linux
                    " -vf \"drawtext=text=\'%{pts\\:gmtime\\:0\\:%M\\\\\:%S}\':r=30:x=(w-tw)/2:y=h/8*5+h/8:fontsize=45:fontcolor="  
                    + timercolor + ":shadowcolor=0x482123ED:shadowx=2:shadowy=2,"
                    " drawtext=fontfile=" + globalfont +
                    ":text=*不支持点歌*:x=(w-tw)/2:y=h/25:fontsize=48:fontcolor=0xF84031:borderw=2:bordercolor=0xFDF1F6DD,"
                    " drawtext=fontfile=" + globalfont +":text=\'•\\\v•\\\v•\\\v•\':x=w/10:y=h/8:fontsize=32:fontcolor=white,"
                    " drawtext=fontfile=" + globalfont +
                    ":text=\'todo\\:切歌不断流\':x=w/7:y=(h-th)/12*11:fontsize=30:fontcolor=0xDDDDDD,"
                    " drawtext=fontfile=" + globalfont +
                    ":text=試\\\v試\\\v竖\\\v排:x=w/13*12:y=h/4:fontsize=40:fontcolor=0xAFAFAF,"
                )
                if title != "" and artist != "":  #信息非空
                    if len(title) + len(artist) > 33:  #文字超长
                        ffmpegcmd += (
                            " drawtext=fontfile=" + infofont + ":text=\'" + title +
                            "\':x=(w-tw)/2:y=h/7*4:fontsize=32:fontcolor=" +
                            infocolor + ":borderw=2:bordercolor=0xFDF1F6DD,"
                            " drawtext=fontfile=" + infofont + ":text=\'" +
                            artist +
                            "\':x=(w-tw)/2:y=h/7*4+th*1.8:fontsize=32:fontcolor=" +
                            infocolor + ":borderw=2:bordercolor=0xFDF1F6DD,")
                    else:
                        ffmpegcmd += (
                            " drawtext=fontfile=" + infofont + ":text=\'" + title +
                            " - " + artist +
                            "\':x=(w-tw)/2:y=h/7*4:fontsize=32:fontcolor=" +
                            infocolor + ":borderw=2:bordercolor=0xFDF1F6DD,")
                ffmpegcmd += " drawtext=fontfile=" + globalfont + ":text=\'%{localtime}\':x=w*8/10:y=h*11/12:fontsize=25:fontcolor=white:shadowcolor=0x6821C999:shadowx=2:shadowy=2\""
                if fileList[ran][1] == 'm4a':  #m4a直接拷贝音频流
                    ffmpegcmd += (
                        " -vcodec libx264 -g 500 -b:v 500k -acodec copy -bufsize 1000k -preset ultrafast -f flv \""
                        + rtmp + "\"")
                else:
                    ffmpegcmd += (
                        " -vcodec libx264 -g 500 -b:v 500k -acodec aac -b:a 256k -bufsize 1000k -preset ultrafast -f flv \""
                        + rtmp + "\"")
            except Exception:
                print("command ERROR!")
                continue
        elif ftype(fileList[ran][1]) == 2:  #flv/MP4视频直接推，没什么好说的
            ffmpegcmd = ("ffmpeg -y -threads 0 -re -i \"" + fileList[ran][0] +
                        "\" -codec copy -bufsize 1000k -f flv \"" + rtmp + "\"")
        else:
            print("type ERROR")
            continue
        print(ffmpegcmd)
        fileList.clear()  #清空列表准备下次写入
        if not (rtmp.startswith('rtmp')):
            with open("current_command.sh", 'w', encoding='utf-8') as f:
                f.write(ffmpegcmd)
        try:
            os.system(ffmpegcmd)
        except Exception:
            print("ERROR!")
            continue


if __name__ == "__main__":
    main(sys.argv)