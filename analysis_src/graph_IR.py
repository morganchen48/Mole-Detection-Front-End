import numpy as np
import glob as glob
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from sklearn.metrics.pairwise import euclidean_distances
from scipy.optimize import linear_sum_assignment
import os
import json
from collections import defaultdict

path = os.getcwd()
res = defaultdict(list)

def find_maps(keypoints1, keypoints2):
    # calculate the pairwise distances between the keypoints
    distances = euclidean_distances(keypoints1, keypoints2)

    # use the Hungarian algorithm to find the optimal mapping of keypoints
    row_ind, col_ind = linear_sum_assignment(distances)

    # map the keypoints onto each other
    mapped_keypoints = []
    for i, j in zip(row_ind, col_ind):
        mapped_keypoints.append((keypoints1[i], keypoints2[j]))
    return mapped_keypoints


def mapping(keypoints1, keypoints2, image1, image2, name):
    # map the keypoints onto each other
    mapped_keypoints = find_maps(keypoints1, keypoints2)
    # plot the keypoints and their connections
    fig, (ax1, ax2) = plt.subplots(1, 2)


    # plot the first image
    ax1.imshow(image1)
    # plot the keypoints in the first image
    for kp1 in keypoints1:
        ax1.plot(kp1[0], kp1[1], 'bo')
    # plot the second image
    ax2.imshow(image2)
    # plot the keypoints in the second image
    for kp2 in keypoints2:
        ax2.plot(kp2[0], kp2[1], 'ro')


    # create a ConnectionPatch object for each pair of keypoints
    for kp1, kp2 in mapped_keypoints:
        con = ConnectionPatch(xyA=(kp1[0], kp1[1]), xyB=(kp2[0], kp2[1]), coordsA="data", coordsB="data",
                              axesA=ax1, axesB=ax2)
        con.set_linestyle('-')
        con.set_color('k')
        ax2.add_artist(con)

    # show the plot
    ax1.set_axis_off()
    ax2.set_axis_off()
    plt.savefig(f"{path}/mapped/{'_'.join(name)}.png")
    plt.show()
    innie = input("TP FP TN FN")
    res[name[0]].append([int(x) for x in innie.split()])
    plt.close()

for tup in os.walk(path):
    fold = tup[0]
    chil = tup[1]
    files = (tup[2])
    files = [file for file in files if '.npy' in file]
    if len(files) > 0:
        if 'mole2' in fold and 'satya' not in fold:
            fold2 = fold[:]
            fold1 = fold.replace('mole2', 'mole1')
        elif 'mole1' in fold and 'satya' not in fold:
            fold2 = fold[:]
            fold1 = fold.replace('mole1/', '')
        else:
            continue
        try:
            points1 = np.load(fold1+'/blobs.npy')
            image1 = plt.imread(fold1 + '/wf_orig_image.png')
            points2 = np.load(fold2+'/blobs.npy')
            image2 = plt.imread(fold2 + '/wf_orig_image.png')
            if len(points1) == 0 or len(points2) == 0:
                continue
            ls = (fold2.split('/')[-4:])
            mapping(points1, points2, image1, image2, ls)
        except FileNotFoundError:
            continue
with open('res.json', 'w') as file:
    json.dump(res, file)
