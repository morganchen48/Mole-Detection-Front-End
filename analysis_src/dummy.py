import os
import numpy as np
import matplotlib.pyplot as plt

path = os.getcwd()
path = path+'/midterm_images/sorted_data/torso/high/mole1/satya/back'
points = np.load(path+"/blobs.npy")
points = points[:,0:2]
print(points)


fig, ax = plt.subplots(1,1)
ax.scatter(points[:,0], [points[:,1]], marker='o', s=100, facecolor='none', edgecolor='red', linewidths=2)
img = plt.imread(path+'/im_with_keypoints.png')
ax.imshow(img)
ax.set_axis_off()
plt.show()
