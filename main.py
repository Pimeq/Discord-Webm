import math
import os
import time

import ffmpeg

def concatFrames():
    os.system("ffmpeg -f concat -safe 0 -i list.txt -c:v 500k -c copy output.webm")
    os.system("ffmpeg -i output.webm -i input.webm -c copy -map 0:v:0 -map 1:a:0 -shortest final.webm")

    os.system('del frames\\*')
    os.system('del frame\\*')
    os.system('del list.txt')

def exportFrames():
    os.system("cd D:\\PyCharm Projects\\Webm trolling")
    frames = os.popen("ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames input.webm").read()
    frameCount = frames.split('\n')[1].split('=')[1]

    probe = ffmpeg.probe('input.webm')
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    width = int(video_stream['width'])
    height = int(video_stream['height'])
    (
        ffmpeg
            .input('input.webm')
            .output('frames\\frames%d.jpg', vframes=frameCount)
            .run()
    )
    amplitude = 0.01
    (
        ffmpeg
            .input('frames\\frames1.jpg')
            .output('frame\\frame1.webm', vcodec='vp8', crf=10)
            .run()
    )
    for x in range(2,int(frameCount)):
        sin = abs(round(math.sin(x * amplitude),2))
        cos = abs(round(math.cos(x * amplitude),2))
        (
            ffmpeg
            .input('frames\\frames{}.jpg'.format(x))
            .filter('scale',sin*width,cos*height)
            .output('frame\\frame{}.webm'.format(x), vcodec='vp8', crf=10)
            .run()
        )
        amplitude += 0.03


    f = open("list.txt",'a')
    for a in range(1,int(frameCount)):
        f.write("file 'frame\\frame{}.webm' \n".format(a))
    f.close()

    concatFrames()



exportFrames()




