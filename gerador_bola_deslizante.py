
import matplotlib.pyplot as plt
from shapely.ops import unary_union
import geopandas as gpd
import shapely.affinity
from shapely.geometry import Point
import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy

#------ CONFIGURAÇÕES

fps = 10000
idas_por_segundo = 3
tempo = 2

distancia_x = 50

#------ CÓDIGO

uma_ida_sao_frames = round(fps/idas_por_segundo)
andar = distancia_x/uma_ida_sao_frames

# Primeiro, criamos a nossa primeira hélice

circle1 = Point(-20, 2).buffer(3)
circle2 = Point(-20, -16).buffer(3)

fig, axs = plt.subplots()


# Agora, produzimos um vídeo de alta framerate para 1 volta.

frameSize = (640, 480)
out = cv2.VideoWriter('uma_volta.mp4',cv2.VideoWriter_fourcc(*'DIVX'), fps, frameSize)

for i in range (uma_ida_sao_frames-1):

    circle1 = shapely.affinity.translate(circle1, andar, 0, 0)
    circle2 = shapely.affinity.translate(circle2, andar, 0, 0)
 
    gpd.GeoSeries([circle1, circle2]).boundary.plot()
    

    plt.xlim([-50, 80])
    plt.ylim([-30, 30])
    plt.savefig('frame.png')
    img = cv2.imread('frame.png')
    out.write(img)
    plt.close('all')
    print("Quadro " + str(i) + "/" + str(uma_ida_sao_frames -1))

out.release()

# Finalmente, concatenamos o mesmo vídeo para múltiplas voltas.

clip_1 = VideoFileClip("uma_volta.mp4")
final_clip = clip_1

paridade = 0

for i in range (round(tempo * idas_por_segundo)): 

    if paridade % 2 == 0:

        final_clip = concatenate_videoclips([final_clip,clip_1])
    else:
        final_clip = concatenate_videoclips([final_clip,moviepy.video.fx.all.time_mirror(clip_1)]) 

    paridade = paridade  + 1

final_clip = final_clip.cutout(0, 1/idas_por_segundo)

final_clip.write_videofile("fps" + str(fps) + "-rps" + str(idas_por_segundo) + "-boladeslz.mp4")

