ffmpeg -y -threads 0 -re -i "G:/Atarashii/[Nemuri] THE iDOLM@STER Shiny Colors (2018-2019) [FLAC]/[2019-2019] FR@GMENT WING/[2019.05.08] FR@GMENT WING 02 We can go now!/01. We can go now!.flac" -ss 123 -i "C:/Users/n/Desktop/BG.mp4" -t 224.88 -vf "drawtext=text='%{pts\:gmtime\:0\:%M\\\:%S}':r=30:x=(w-tw)/2:y=h/4*3:fontsize=45:fontcolor=0x7FDE92:shadowcolor=0xFDF1F6DD:shadowx=2:shadowy=2, drawtext=fontfile=/root/font/simhei.ttf:text=*不支持点歌*:x=(w-tw)/2:y=h/25:fontsize=48:fontcolor=0xF84031:borderw=2:bordercolor=0xFDF1F6DD, drawtext=fontfile=/root/font/simhei.ttf:text='\• 使用vps+自制程序随机播放库中的音乐':x=w/14:y=h/7:fontsize=32:fontcolor=white, drawtext=fontfile=/root/font/simhei.ttf:text='\• 几年前的歌曲库了，正在准备整理好传新歌':x=w/14:y=h/7+th*1.5:fontsize=32:fontcolor=white, drawtext=fontfile=/root/font/simhei.ttf:text='\• 不支持点歌，因为没bu流hui量xie':x=w/14:y=h/7+th*1.5*2:fontsize=32:fontcolor=white, drawtext=fontfile=/root/font/simhei.ttf:text='todo\:切歌不断流':x=w/7:y=(h-th)/12*11:fontsize=30:fontcolor=0xDDDDDD, drawtext=fontfile=/root/font/simhei.ttf:text=試\試\竖\排:x=w/13*12:y=h/4:fontsize=40:fontcolor=0xAFAFAF, drawtext=fontfile=/root/font/simhei.ttf:text='We can go now!':x=(w-tw)/2:y=h/19*10:fontsize=40:fontcolor=0x4BA1EF:borderw=2:bordercolor=0xFDF1F6DD, drawtext=fontfile=/root/font/simhei.ttf:text='イルミネーションスターズ (櫻木真乃、風野灯織、八宮めぐる)':x=(w-tw)/2:y=h/19*10+th*1.8:fontsize=32:fontcolor=0x4BA1EF:borderw=2:bordercolor=0xFDF1F6DD, drawtext=fontfile=/root/font/simhei.ttf:text='%{localtime}':x=w*8/11:y=h*11/12:fontsize=25:fontcolor=white:shadowcolor=0x6821C999:shadowx=2:shadowy=2" -vcodec libx264 -g 50 -b:v 700k -acodec aac -b:a 256k -bufsize 1000k -preset ultrafast -f flv "c:/users/n/desktop/t.flv"