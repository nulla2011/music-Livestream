import os
import sys
import random
import configparser
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.id3 import ID3

conf = configparser.ConfigParser()
conf.read("music-livestream.ini")
rtmp = conf.get('main', 'rtmp_url')
musicpath = conf.get('main', 'musicpath')
videopath = conf.get('main', 'videopath')
timercolor = conf.get('colors', 'timercolor')
infocolor = conf.get('colors', 'infocolor')
globalfont = conf.get('fonts', 'globalfont')
infofont = conf.get('fonts', 'infofont')

maxlength = 7 * 60 + 15
fileList = []

def getMusicFile(path):
    currentList = os.listdir(path)
    for eachF in currentList:
        tempPath = path + '/' + eachF
        if os.path.isfile(tempPath):
            if (tempPath.find('.flac') != -1):
                fileList.append([tempPath, 'flac'])
            elif (tempPath.find('.mp3') != -1):
                fileList.append([tempPath, 'mp3'])
            elif (tempPath.find('.m4a') != -1):
                fileList.append([tempPath, 'm4a'])
            else:
                continue
        else:
            getMusicFile(tempPath)

def getVideoFile(path):
    currentList = os.listdir(path)
    for eachF in currentList:
        tempPath = path + '/' + eachF
        if os.path.isfile(tempPath):
            if (tempPath.find('.flv') != -1):
                fileList.append([tempPath, 'flv'])
            elif (tempPath.find('.mp4') != -1):
                fileList.append([tempPath, 'mp4'])
            else:
                continue
        else:
            getVideoFile(tempPath)

def main(argv):
    while True:
        global fileList
        if argv[1]=="music":
            getMusicFile(musicpath)
        elif argv[1]=="video":
            pass
            #getVideoFile(videopath)
        elif argv[1]=="-s":
            if len(argv)<3:
                print("param ERROR!")
                return -1
            else:
                getMusicFile(musicpath)
                #getVideoFile(videopath)
                resultList=[]
                for f in fileList:
                    if (f[0].find(argv[2])!=-1):
                        resultList.append(f)
                if len(resultList)==0:
                    print("not fond!")
                    return -1
                else:
                    fileList.clear()
                    fileList=resultList.copy()                  
        else:
            getMusicFile(musicpath)
            getVideoFile(videopath)
        try:
            ran = random.randint(0, len(fileList) - 1)
        except ValueError:
            print("no file fond")
            continue
        title = ""
        artist = ""
        artistList = []
        if fileList[ran][1] == 'flac':
            audio = FLAC(fileList[ran][0])
            for meta in audio.tags:
                if (meta[0] == 'TITLE' or meta[0] == 'Title'):
                    title = meta[1].replace('\x00', '') #部分结尾有谜之字符
                if (meta[0] == 'ARTIST' or meta[0] == 'Artist'):
                    artistList.append(meta[1].replace('\x00', '')) #部分结尾有谜之字符
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
            ffmpegcmd = (
                "ffmpeg -y -threads 0 -re -i \"" + fileList[ran][0] +
                "\" -f lavfi -i color=size=1280x720:rate=15:color=random:d=" +
                str(musicLength) +
                " -vf \"colorlevels=rimin=0.2:gimin=0.2:bimin=0.2:romax=0.9:gomax=0.9:bomax=0.9,vignette,"
                " drawtext=text=\'%{pts\\:gmtime\\:0\\:%M\\\\\:%S}\':r=30:x=(w-tw)/2:y=(h-th)/2+h/8:fontsize=45:fontcolor="
                + timercolor + ":shadowcolor=0x482123ED:shadowx=2:shadowy=2,"
                " drawtext=fontfile=" + globalfont +
                ":text=*不支持点歌*:x=(w-tw)/2:y=h/25:fontsize=48:fontcolor=0xF84031:borderw=2:bordercolor=0xFDF1F6DD,"
                " drawtext=fontfile=" + globalfont +
                ":text=\'todo\\:背景，切歌不断流\':x=(w-tw)/3:y=(h-th)/12*11:fontsize=30:fontcolor=0xDDDDDD,"
                " drawtext=fontfile=" + globalfont +
                ":text=試\\\v試\\\v竖\\\v排:x=w/13*12:y=h/2:fontsize=40:fontcolor=0xAFAFAF,"
            )
            if title != "" and artist != "":  #信息非空
                if len(title) + len(artist) > 33:  #文字超长
                    ffmpegcmd += (
                        " drawtext=fontfile=" + infofont + ":text=\'" + title +
                        "\':x=(w-tw)/2:y=h/3:fontsize=32:fontcolor=" +
                        infocolor + ":borderw=2:bordercolor=0xFDF1F6DD,"
                        " drawtext=fontfile=" + infofont + ":text=\'" +
                        artist +
                        "\':x=(w-tw)/2:y=h/3+th*1.8:fontsize=32:fontcolor=" +
                        infocolor + ":borderw=2:bordercolor=0xFDF1F6DD,")
                else:
                    ffmpegcmd += (
                        " drawtext=fontfile=" + infofont + ":text=\'" + title +
                        " - " + artist +
                        "\':x=(w-tw)/2:y=h/3:fontsize=32:fontcolor=" +
                        infocolor + ":borderw=2:bordercolor=0xFDF1F6DD,")
            ffmpegcmd += " drawtext=fontfile=" + globalfont + ":text=\'%{localtime}\':x=w*8/10:y=h*11/12:fontsize=25:fontcolor=white:shadowcolor=0x6821C999:shadowx=2:shadowy=2\""
            if fileList[ran][1] == 'm4a':  #m4a直接拷贝音频流
                ffmpegcmd += (
                    " -vcodec libx264 -g 30 -maxrate 2500k -acodec copy -bufsize 1000k -preset ultrafast -f flv "
                    + rtmp)
            else:
                ffmpegcmd += (
                    " -vcodec libx264 -g 30 -maxrate 2500k -acodec aac -b:a 256k -bufsize 1000k -preset ultrafast -f flv "
                    + rtmp)
        except Exception:
            print("command ERROR!")
            continue
        print(ffmpegcmd)
        fileList.clear() #清空列表准备下次写入
        try:
            os.system(ffmpegcmd)
        except Exception:
            print("ERROR!")
            continue


if __name__ == "__main__":
    main(sys.argv)