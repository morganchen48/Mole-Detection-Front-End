import json
import numpy as np
import matplotlib.pyplot as plt
import itertools

with open('res2.json', 'r') as f:
    data = json.load(f)


def plot_confusion_matrix(data, classes, title='Confusion matrix', cmap=plt.cm.PuBu):
    cm = np.array([[data[0], data[3]], [data[1], data[2]]])
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    # plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


def get_metrics(conf_matrix):
    tp, fp, tn, fn = conf_matrix
    accuracy = (tp + tn) / (tn + fp + fn + tp)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    specificity = tn / (tn + fp)
    f1_score = 2 * precision * recall / (precision + recall)
    return accuracy, precision, recall, specificity, f1_score

datum = data['sorted_data']
a0_10 = [datum[0], datum[3]]
a0_10 = np.mean(a0_10, axis=0)
a10_45 = [datum[1], datum[4]]
a10_45 = np.mean(a10_45, axis=0)
a0_45 = [datum[2], datum[5]]
a0_45 = np.mean(a0_45, axis=0)
f1s = [get_metrics(a0_10)[4], get_metrics(a10_45)[4], get_metrics(a0_45)[4]]

def plot2(val_avg, titles):
    plt.figure(figsize=(5,5))
    plt.bar(range(len(val_avg)), val_avg, width=0.8,)
    plt.xticks(range(len(val_avg)), titles)
    plt.ylabel("F-Score")
    # plt.xlabel("Rotation Angle")
    plt.title(f"Mole Mapping\n", fontsize=18)
    plt.ylim(0, max(val_avg) * 1.1)
    for j, v in enumerate(val_avg):
        plt.text(j, v+0.01, str(v.round(2)), ha='center', fontsize=10)
    plt.tight_layout()
    plt.savefig('angles.png')

titles = ["0˚ to 10˚", "10˚ to 45˚", "0˚ to 45˚"]
plot2(f1s, titles)
