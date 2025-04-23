"""
注意：背景必须为黑色
"""
import cv2
from imageio import *
img=cv2.imread('img.png')
def spin(im,v,t,fn,ctr=(0,0),fps=30):
    """
    旋转
    :param im: 图像
    :param v: 速度（°/s)
    :param t: 时间
    :param fn: 文件名
    :param ctr: 旋转中心
    :param fps: fps
    :return:
    """
    l=[]
    l.append(cv2.cvtColor(im,cv2.COLOR_BGR2RGB))
    a,b=im.shape[:2]
    for i in range(0,t*fps):
        mat=cv2.getRotationMatrix2D(ctr,v*t*i/(t*fps),1)
        rotimg=cv2.warpAffine(im,mat,(b,a))
        l.append(cv2.cvtColor(rotimg,cv2.COLOR_BGR2RGB))
    if fn.endswith('.gif'):
        mimwrite(fn,list(reversed(l)), duration=1000/fps)
    else:
        mimwrite(fn, list(reversed(l)), fps=fps)
def enlarge(im,t,fn,ctr=(0,0),fps=30):
    """
    放大
    :param im: 图像
    :param t: 时间
    :param ctr: 放大中心
    :param fn: 文件名
    :param fps: fps
    :return:
    """
    l=[]
    a,b=im.shape[:2]
    for i in range(0,t*fps):
        mat=cv2.getRotationMatrix2D(ctr,0,1/(t*fps)*(i+1))
        rotimg=cv2.warpAffine(im,mat,(b,a))
        l.append(cv2.cvtColor(rotimg,cv2.COLOR_BGR2RGB))
    l.append(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    if fn.endswith('.gif'):
        mimwrite(fn,l, duration=1000/fps)
    else:
        mimwrite(fn, list(reversed(l)), fps=fps)
