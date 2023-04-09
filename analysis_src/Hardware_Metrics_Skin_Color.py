import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
import glob as glob
import scipy.stats as stats

path = os.getcwd()
def calculate_sharpness(img):
    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Calculate the maximum and minimum pixel values
    mean_pixel_value = np.mean(img)
    std_pixel_value = np.std(img)

    # Calculate the contrast
    sharpness = (mean_pixel_value - std_pixel_value) / (mean_pixel_value)

    return sharpness

def get_metric(blob_detect_info, image):
    mole_coord = blob_detect_info[:,3:7]
    mole_coord = mole_coord.astype(int)
    mole_IQI = []
    for i in range(len(mole_coord)):
        # Cropping the image
        cropped_image = image[mole_coord[i][2]:mole_coord[i][3], mole_coord[i][0]:mole_coord[i][1], :]
        mole_IQI.append(calculate_sharpness(cropped_image))
    return(np.mean(np.array(mole_IQI)))

vals_shaun = []
vals_satya = []
for tup in os.walk(path):
    fold = tup[0]
    chil = tup[1]
    files = (tup[2])
    files = [file for file in files if '.npy' in file and 'torso' in fold and 'front' in fold]
    if not len(files) == 0:
        points = np.load(fold+'/blobs.npy')
        image1 = plt.imread(fold+"/wf_orig_image.png")
        if 'satya' in fold:
            vals_satya.append(get_metric(points, image1))
        elif 'shaun' in fold:
            vals_shaun.append(get_metric(points, image1))

print(vals_satya)
print(vals_shaun)
val_avg = [np.mean(vals_shaun), np.mean(vals_satya)]
titles = ['Fitzpatrick 3', 'Fitzpatrick 5']
plt.figure(figsize=(5,5))
plt.bar(range(len(val_avg)), val_avg)
plt.xticks(range(len(val_avg)), titles)
plt.ylabel("Average Sharpness Value")
plt.xlabel("Rotation Angle")
plt.title(f"Image Quality\n", fontsize=18)
plt.ylim(0, max(val_avg) * 1.1)
for j, v in enumerate(val_avg):
    plt.text(j, v+0.01, str(v.round(2)), ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('angles.png')
plt.show()

_, p = stats.ttest_ind(vals_satya, vals_shaun)
print(p)
