# -*- coding: UTF-8 -*-
import os
import sys
import random
import time
import configparser
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.id3 import ID3
import ffmpegcmd
import reverseBackslash

conf = configparser.ConfigParser(interpolation=None)
try:
    conf.read("music-Livestream.ini")
    rtmp = conf.get('main', 'rtmp_url')
    musicpath = reverseBackslash.reverseB(conf.get('main', 'musicpath'))
    videopath = reverseBackslash.reverseB(conf.get('main', 'videopath'))
    bgvPath = reverseBackslash.reverseB(conf.get('main', 'bgvPath'))
    enableVideo = int(conf.get('main', 'enableVideo'))
    aOffset = conf.get('main', 'offset')
    timercolor = conf.get('colors', 'timercolor')
    infocolor = conf.get('colors', 'infocolor')
    timershadow = conf.get('colors', 'timershadow')
    infoshadow = conf.get('colors', 'infoshadow')
    globalfont = conf.get('fonts', 'globalfont')
    infofont = conf.get('fonts', 'infofont')
    timerfont = conf.get('fonts', 'timerfont')
except Exception:
    print("config file not correct! creating,,,")
    os.system("mv music-Livestream.ini music-Livestream.ini.bak")  #for linux
    os.system(
        "cp music-Livestream_example.ini music-Livestream.ini")  #for linux
    sys.exit(0)
maxlength = 7 * 60 + 15
fileList = []


class Musicinfo:
    def __init__(self, Path):
        self.path = Path
        self.mtype = (os.path.splitext(Path)[1])[1:]

    def Length(self):
        if self.mtype == "mp3":
            audio = MP3(self.path)
        elif self.mtype == "flac":
            audio = FLAC(self.path)
        elif self.mtype == "m4a":
            audio = MP4(self.path)
        else:
            print("file type not support!")
            return -1
        return audio.info.length

    def artist(self):
        if self.mtype == "mp3":
            audio = ID3(self.path)
            return audio['TPE1'].text[0]
        elif self.mtype == "flac":
            artistList = []
            audio = FLAC(self.path)
            for tag in audio.tags:
                if (tag[0] == 'ARTIST' or tag[0] == 'Artist'):
                    artistList.append(tag[1].replace('\x00', ''))  #部分结尾有谜之字符
            return ("/".join(artistList))
        elif self.mtype == "m4a":
            audio = MP4(self.path)
            return audio.tags['\xa9ART'][0]

    def title(self):
        if self.mtype == "mp3":
            audio = ID3(self.path)
            return audio["TIT2"].text[0]
        elif self.mtype == "flac":
            audio = FLAC(self.path)
            for tag in audio.tags:
                if (tag[0] == 'TITLE' or tag[0] == 'Title'):
                    return tag[1].replace('\x00', '')  #部分结尾有谜之字符
        elif self.mtype == "m4a":
            audio = MP4(self.path)
            return audio.tags['\xa9nam'][0]


'''
def ext(path):
    name=path.split('/')[-1]
    extension=name.split('.')[-1]
    return extension
'''


def getMusicFile(path):
    try:
        currentList = os.listdir(path)
    except FileNotFoundError:
        print("path not found,please check music-Livestream.ini")
        sys.exit(0)
    for eachF in currentList:
        tempPath = path + '/' + eachF
        if os.path.isfile(tempPath):
            if eachF.lower().endswith('.flac'):
                fileList.append(tempPath)
            elif eachF.lower().endswith('.mp3'):
                fileList.append(tempPath)
            elif eachF.lower().endswith('.m4a'):
                fileList.append(tempPath)
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
            if eachF.lower().endswith('.flv'):
                fileList.append(tempPath)
            elif eachF.lower().endswith('.mp4'):
                fileList.append(tempPath)
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
                        fullname = os.path.split(f)[1]
                        fname = os.path.splitext(fullname)[0]
                        if (fname.find(argv[2]) != -1):
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
        currentFilePath = fileList[ran]
        currentFileType = (os.path.splitext(fileList[ran])[1])[1:]
        if ftype(currentFileType) == 1:
            M = Musicinfo(currentFilePath)
            musicLength = M.Length()
            if musicLength > maxlength:
                print("too long")
                continue
            if musicLength < 0:
                print("too short or file type ERROR")
                continue
            title = M.title()
            artist = M.artist()
            # audio only
            # 2 currentfile, mLength, offset, bgv, 2 color, 2 shadow, 3 font, info, output
            try:
                cmd = ffmpegcmd.createffmpegcmd(
                    currentFilePath, currentFileType, musicLength, aOffset,
                    bgvPath, timercolor, infocolor, timershadow, infoshadow,
                    globalfont, infofont, timerfont, title, artist, rtmp)
            except Exception:
                print("command ERROR!")
                continue
        elif ftype(currentFileType) == 2:  #flv/MP4视频直接推，没什么好说的
            cmd = f"ffmpeg -y -threads 0 -re -i \"{currentFilePath}\" -codec copy -bufsize 1000k -f flv \"{rtmp}\""
        else:
            print("type ERROR")
            continue
        print(cmd)
        fileList.clear()  #清空列表准备下次写入
        if not (rtmp.startswith('rtmp')):
            with open("current_command.sh", 'w', encoding='utf-8') as f:
                f.write(cmd)
        with open("player.log", 'a+', encoding='utf-8') as l:
            timeStr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            filename = os.path.split(currentFilePath)[1]
            if ftype(currentFileType) == 1:
                l.write(
                    f"[{timeStr}] [PLAY] {title} - {artist} (name:{filename})\n"
                )
            elif ftype(currentFileType) == 2:
                l.write(f"[{timeStr}] [PLAY] {filename}\n")
        try:
            os.system(cmd)
        except Exception:
            print("ERROR!")
            continue


if __name__ == "__main__":
    main(sys.argv)