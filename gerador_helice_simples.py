
import matplotlib.pyplot as plt
from shapely.ops import unary_union
import geopandas as gpd
import shapely.affinity
from shapely.geometry import Point
import cv2
from moviepy.editor import VideoFileClip, concatenate_videoclips

#------ CONFIGURAÇÕES

fps = 30
frequencia_em_rps = 5
tempo = 5

#------ CÓDIGO

uma_volta_sao_frames = round(fps/frequencia_em_rps)
total_angulo = 360
acrescimo_por_frame = total_angulo/uma_volta_sao_frames

# Primeiro, criamos a nossa hélice

circle1 = Point(2, 2).buffer(1)
circle2 = Point(-8, -16).buffer(1)
circle3 = Point(12, -16).buffer(1)

ellipse1 = shapely.affinity.scale(circle1, 2, 10) 
ellipse2 = shapely.affinity.scale(circle2, 10, 2)
ellipse3 = shapely.affinity.scale(circle3, 10, 2)


ellipse2 = shapely.affinity.rotate(ellipse2, 30, 'center')
ellipse3 = shapely.affinity.rotate(ellipse3, -30, 'center')

fig, axs = plt.subplots()
new_shape = [ellipse1, ellipse2, ellipse3]
new_shape_2 = new_shape

mergedPolys = unary_union(new_shape)


# Agora, produzimos um vídeo de alta framerate para 1 volta.

frameSize = (640, 480)
out = cv2.VideoWriter('uma_volta.mp4',cv2.VideoWriter_fourcc(*'DIVX'), fps, frameSize)

for i in range (uma_volta_sao_frames-1):

    mergedPolys = shapely.affinity.rotate(mergedPolys, acrescimo_por_frame, origin=mergedPolys.centroid)
 
    gpd.GeoSeries([mergedPolys]).boundary.plot()

    plt.xlim([-50, 50])
    plt.ylim([-50, 50])
    plt.savefig('frame.png')
    img = cv2.imread('frame.png')
    out.write(img)
    plt.close('all')
    print("Quadro " + str(i) + "/" + str(uma_volta_sao_frames -1))

out.release()

# Finalmente, concatenamos o mesmo vídeo para múltiplas voltas.

clip_1 = VideoFileClip("uma_volta.mp4")
final_clip = clip_1

for i in range (round(tempo * frequencia_em_rps )- 1): 

    final_clip = concatenate_videoclips([final_clip,clip_1])

final_clip.write_videofile("fps" + str(fps) + "-rps" + str(frequencia_em_rps) + "-helice.mp4")

