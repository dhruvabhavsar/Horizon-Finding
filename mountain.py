#!/usr/local/bin/python3
#
# Authors: Dhruva Bhavsar(dbhavsar), Hely Modi(helymodi), Aneri Shah(annishah)
#
# Mountain ridge finder
#
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels

def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

# Calculate the emission probability for human input part:
def emis_prob1(edge_strength,row,col):
    emis_dist=zeros((edge_strength.shape[0],edge_strength.shape[1]))
#    b=argmax(edge_strength,axis=0)
    for i in range(0,edge_strength.shape[0]):
        for j in range(0,edge_strength.shape[1]):
            l=int(edge_strength.shape[0]/5)
            if i in range(row-l,row+l):
                if(j==col):
                    emis_dist[i][j]=1
                else:
                    emis_dist[i][j]=(edge_strength[i][j])**0.5
            else:
                emis_dist[i][j]=(edge_strength[i][j])**0.1
    return emis_dist
    
    
# Calculate emission probability for normal Viterbi:
def emis_prob(edge_strength):
    emis_dist=zeros((edge_strength.shape[0],edge_strength.shape[1]))
    b=argmax(edge_strength,axis=0)
    for i in range(0,edge_strength.shape[0]):
        for j in range(0,edge_strength.shape[1]):
            emis_dist[i][j]=(edge_strength[i][j])**0.1
    return emis_dist

# Calculate transition probability:
def trans_prob(a):

    trans_dist=zeros((a.shape[0],a.shape[0]))

    for i in range(0,a.shape[0]):
        for j in range(0,a.shape[0]):
            trans_dist[i][j]=a.shape[0]-abs(i-j)
    savetxt("foo1.csv",trans_dist,delimiter=",")
    return (trans_dist/a.shape[0])**2

# Implementing Viterbi algorithm:
def viterbi1(obs, trans, emis):
   
    min_nonzero = min(emis[nonzero(emis)])
    emis[emis == 0] = min_nonzero
    V = zeros((obs.shape[0], trans.shape[0]))

    V[0, :] = log(emis[:,0])

    prev = zeros((obs.shape[0] - 1, trans.shape[0]))
    
    for t in range(1, obs.shape[0]):
        for j in range(trans.shape[0]):
            
            prob = V[t - 1] + log(trans[:, j]) + log(emis[:, t])
            prev[t - 1, j] = argmax(prob)
            V[t, j] = max(prob)
                
     # Finding the last hidden state with maximum probability
    last_state = argmax(V[obs.shape[0] - 1, :])
    
    path = zeros(obs.shape[0])
    
    # Determining the path with most probability by back tracking
    path[0] = last_state
    index = 1
    for i in range(obs.shape[0] - 2, -1, -1):
        path[index] = prev[i, int(last_state)]
        last_state = prev[i, int(last_state)]
        index += 1

    path = flip(path, axis=0)
    return path

# Implementing Viterbi algorithm for human input part:
def viterbi2(obs, trans, emis, row, col):

    min_nonzero = min(emis[nonzero(emis)])
    emis[emis == 0] = min_nonzero
    V = zeros((obs.shape[0], trans.shape[0]))

    V[0, :] = log(emis[:,0])

    prev = zeros((obs.shape[0] - 1, trans.shape[0]))
    
    for t in range(1, obs.shape[0]):
        for j in range(trans.shape[0]):
            if t==row and j==col:
                V[t, j] = 1
            
            else:
                prob = V[t - 1] + log(trans[:, j]) + log(emis[:, t])
                prev[t - 1, j] = argmax(prob)
                V[t, j] = max(prob)
                
     # Finding the last hidden state with maximum probability
    last_state = argmax(V[obs.shape[0] - 1, :])
    
    path = zeros(obs.shape[0])
    
    # Determining the path with most probability by back tracking
    path[0] = last_state
    index = 1
    for i in range(obs.shape[0] - 2, -1, -1):
        path[index] = prev[i, int(last_state)]
        last_state = prev[i, int(last_state)]
        index += 1

    # Flip the path array since we were backtracking
    path = flip(path, axis=0)
    return path

# main program
#
(input_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image1 = Image.open(input_filename)
input_image2 = Image.open(input_filename)
input_image3 = Image.open(input_filename)
col=int(gt_col)
row=int(gt_row)

input_array=array(input_image1)

# compute edge strength mask
edge_strength = edge_strength(input_image1)

# Taking pixels with highest gradient as observed variables
observed=argmax(edge_strength,axis=0)

imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

# Part 1: Simple Bayes Net:

ridge1=observed

# output answer
imageio.imwrite("output_simple.jpg", draw_edge(input_image1, ridge1, (0, 0, 255), 5))

# Part 2: Viterbi:

emis=emis_prob(edge_strength)

trans=trans_prob(input_array)

ridge2=viterbi1(observed,trans,emis)

# output answer
imageio.imwrite("output_map.jpg", draw_edge(input_image2, ridge2, (255, 0, 0), 5))

# Part 3: Viterbi with human input:

emis1=emis_prob1(edge_strength,row,col)

ridge3=viterbi2(observed,trans,emis1,row,col)

# output answer
imageio.imwrite("output_human.jpg", draw_edge(input_image3, ridge3, (0, 255, 0), 5))
