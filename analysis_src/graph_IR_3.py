import numpy as np
import glob as glob
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from sklearn.metrics.pairwise import euclidean_distances
from scipy.optimize import linear_sum_assignment
import os
import glob

path = os.getcwd()

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


def mapping(keypoints1, keypoints2, image1, image2, name, keypoints3=None, image3=None):
    if keypoints3 is  None:
        # map the keypoints onto each other
        mapped_keypoints = find_maps(keypoints1, keypoints2)
        # plot the keypoints and their connections
        fig, (ax1, ax2) = plt.subplots(1, 2)
    if keypoints3 is not None:
        mapped_keypoints = find_maps(keypoints1, keypoints2)
        mapped_keypoints2 = find_maps(keypoints2, keypoints3)
        # plot the keypoints and their connections
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)


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
    if image3 is not None:
        # plot the third image
        ax3.imshow(image3)
        # plot the keypoints in the third image
        for kp3 in keypoints3:
            ax3.plot(kp3[0], kp3[1], 'go')


    # create a ConnectionPatch object for each pair of keypoints
    for kp1, kp2 in mapped_keypoints:
        con = ConnectionPatch(xyA=(kp1[0], kp1[1]), xyB=(kp2[0], kp2[1]), coordsA="data", coordsB="data",
                              axesA=ax1, axesB=ax2)
        con.set_linestyle('-')
        con.set_color('k')
        ax2.add_artist(con)
    if keypoints3 is not None:
        for kp2, kp3 in mapped_keypoints2:
            con2 = ConnectionPatch(xyA=(kp2[0], kp2[1]), xyB=(kp3[0], kp3[1]), coordsA="data", coordsB="data",
                                  axesA=ax2, axesB=ax3)
            con2.set_linestyle('-')
            con2.set_color('k')
            ax3.add_artist(con2)
        ax3.set_axis_off()


    # show the plot
    ax1.set_axis_off()
    ax2.set_axis_off()
    plt.savefig(f"{path}/mapped/{name}.png")
    plt.close()

for tup in os.walk(path):
    fold = tup[0]
    chil = tup[1]
    files = (tup[2])
    fold1, fold2, fold3 = None, None, None
    files = [file for file in files if '.npy' in file]
    if len(files) > 0:
        if 'mole2' in fold and 'satya' not in fold:
            fold3 = fold[:]
            fold2 = fold.replace('mole2', 'mole1')
            fold1 = fold.replace('mole2/', '')
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
            if fold3 is not None:
                points3 = np.load(fold3+'/blobs.npy')
                image3 = plt.imread(fold3 + '/wf_orig_image.png')
            if len(points1) == 0 or len(points2) == 0 or len(points3) == 0:
                continue
            ls = (fold1.split('/')[-5:])
            if points3 is not None:
                mapping(points1, points2, image1, image2, "_".join(ls), points3, image3)
            else:
                mapping(points1, points2, image1, image2, "_".join(ls))
        except FileNotFoundError:
            continue
