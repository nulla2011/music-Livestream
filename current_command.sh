ffmpeg -y -threads 0 -re -itsoffset 00:00:07 -i "D:/netease/高森奈津美,山下七海,上坂すみれ - Starry-Go-Round (M@STER VERSION).mp3" -ss 18 -i "C:/Users/n/Desktop/BG2.mp4" -t 344.21469387755104 -vf "movie=chi.mp4:loop=0,scale=192x108,setpts=N/FRAME_RATE/TB[gif];[0:v][gif]overlay=x=0:y=615:shortest=1:eof_action=pass,drawtext=text='%{pts\:gmtime\:0\:%M\\\:%S}':r=30:x=(w-tw)/2:y=h/4*3-th+h/16:fontfile=/root/font/SourceHanSansCN-Medium-2.otf:fontsize=45:fontcolor=0x5A66B4:shadowcolor=0xFDF1F6DD:shadowx=2:shadowy=2, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text=*不支持点歌*:x=(w-tw)/2:y=h/25:fontsize=48:fontcolor=0xF84031:borderw=2:bordercolor=0xFDF1F6DD, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='\• 使用vps+自制程序（已开源）随机播放库中的音乐':x=w/14:y=h/7:fontsize=32:fontcolor=0xFFFFFFEE, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='\• 几年前的歌曲库了，正在准备整理传新歌':x=w/14:y=h/7+th*1.5:fontsize=32:fontcolor=0xFFFFFFEE, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='\• 不支持点歌，因为没bu流hui量xie':x=w/14:y=h/7+th*1.5*2:fontsize=32:fontcolor=0xFFFFFFEE, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='\• 如果视频画面停住请刷新':x=w/14:y=h/7+th*1.5*3:fontsize=32:fontcolor=0xFFFFFFEE, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='todo\:切歌不断流':x=w/7:y=(h-th)/12*11:fontsize=30:fontcolor=0xDDDDDD, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text=試\試\竖\排:x=w/13*12:y=h/4:fontsize=40:fontcolor=0xAFAFAF, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='Starry-Go-Round (M@STER VERSION)':x=(w-tw)/2:y=h/19*10:fontsize=40:fontcolor=0xF8DC3D:borderw=2:bordercolor=0x100624DD, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='高森奈津美/山下七海/上坂すみれ/杜野まこ/青木志貴':x=(w-tw)/2:y=h/19*10+th*2:fontsize=32:fontcolor=0xF8DC3D:borderw=2:bordercolor=0x100624DD, drawtext=fontfile=/root/font/SourceHanSansCN-Medium-2.otf:text='%{localtime}':x=w*10/13:y=h*11/12:fontsize=25:fontcolor=white:shadowcolor=0x6821C999:shadowx=2:shadowy=2" -vcodec libx264 -acodec aac -b:a 256k -g 50 -b:v 1000k -bufsize 2000k -maxrate 1500k -preset ultrafast -f flv "c:/users/n/desktop/t.flv"