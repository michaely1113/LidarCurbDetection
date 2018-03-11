import cv2
from laspy.file import File
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import pandas as pd
from PIL import Image
import scipy.interpolate

LIDAR_FILE = 'sample/raw_data/q47122e2104.las'
CONTOUR_FILE = 'sample/contour/contour_plot_levels_3.jpg'

def main():
    # Loading Lidar data, generating contour plots
    lidarFilePath = os.path.join(os.path.dirname(__file__), LIDAR_FILE)
    generateContourPlots(lidarFilePath)

    # Create curbs based on the generated contour plots
    contourFilePath = os.path.join(os.path.dirname(__file__), CONTOUR_FILE)

    BestHough(contourFilePath)
    HoughTransform(contourFilePath)
    ProbHough(contourFilePath)

def BestHough(filepath):
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    minLineLength=img.shape[1]-300
    lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, threshold=10,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)

    a, b, c = lines.shape
    for i in range(a):
        cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imshow('edges', edges)
    cv2.imshow('result', img)
    cv2.imwrite('curbs_optimized.jpg', img)

def HoughTransform(filepath):
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    lines = cv2.HoughLines(edges,1,np.pi/180,50)
    for line in lines:
        for rho,theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

    cv2.imwrite('curbs_regular.jpg', img)

def ProbHough(filepath):
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,100,350,apertureSize = 3)

    lines = cv2.HoughLinesP(edges,1,np.pi/180,25,100,1)
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img,(x1,y1),(x2,y2),(0,0,0),2)

    cv2.imwrite('curbs_probability_optimized.jpg',img)

def pngToJpg(file):
    im = Image.open(file)
    rgb_im = im.convert('RGB')
    rgb_im.save(file[:-3] + '.jpg')

def generateContourPlots(file, show_3D_plot=False, contour_levels=0):
    data = File(file, mode='r')

    # Extract X, Y, Z points from data
    d = {'X': data.X, 'Y': data.Y, 'Z': data.Z}
    datapoints = pd.DataFrame(d)
    print("total points:", len(datapoints))

    max_x = datapoints['X'].max()
    min_y = datapoints['Y'].min()

    segmentationBlock = datapoints.loc[(datapoints['X'] >= max_x - 50000) & (datapoints['Y'] <= min_y + 50000)]
    x = segmentationBlock.X
    y = segmentationBlock.Y
    z = segmentationBlock.Z
    print("points in segmentation block:", len(segmentationBlock))

    # Contour plot
    xi, yi = np.linspace(min(x), max(x), 500), np.linspace(min(y), max(y), 500)
    xi, yi = np.meshgrid(xi, yi)
    zi = scipy.interpolate.griddata((x, y), z, (xi, yi), method='linear')
    plt.axis('off')

    if contour_levels > 0:
        plt.contourf(xi, yi, zi, cmap=cm.jet, levels=np.linspace(min(z), max(z), contour_levels))
    else:
        plt.contourf(xi, yi, zi, cmap=cm.jet)
    plt.savefig('contour_plot_levels_3.png',transparent=True,bbox_inches='tight')

    # 3_D Plot
    if show_3D_plot:
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_axis_off()
        plt.show()

# Called at the bottom to avoid method definition, implementation is still at top for readability
main()
