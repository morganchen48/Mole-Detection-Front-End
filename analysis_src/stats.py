import json
import numpy as np
import matplotlib.pyplot as plt
import itertools

with open('res.json', 'r') as f:
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


conditions = np.insert(list(map(str, data.keys())), 0, 'overall')
comb = np.vstack(list(data.values()))
tot_confm = np.sum(comb, axis=0)
tot = get_metrics(tot_confm)
plt.subplot(231)
plot_confusion_matrix(tot_confm, ['Change', 'No Change'], title="Overall Confusion Matrix")
for i, key in enumerate(data):
    plt.subplot(2,3,i+2)
    datum = np.array(data[key])
    confusion_matrix = np.sum(datum, axis=0)
    plot_confusion_matrix(confusion_matrix, ['Change', 'No Change'], title=f'Confusion Matrix for {conditions[i+1]}')
    metrics = get_metrics(confusion_matrix)
    tot = np.vstack((tot, metrics))
plt.tight_layout()
plt.show()

titles = ["accuracy", "precision", "recall", "specificity", "f1_score"]
for i in range(len(data)):
    plt.subplot(2, 3, i+1)
    plt.bar(range(len(tot)), tot[:, i])
    plt.xticks(range(len(tot)), conditions, rotation=45)
    plt.title(f"{titles[i]}")
    plt.ylim(0, max(tot[:, i]) * 1.1)
    for j, v in enumerate(tot[:, i]):
        plt.text(j, v+0.01, str(v.round(2)), ha='center', fontsize=10)
plt.tight_layout()
# plt.show()

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
dice = tot[:,4]
plt.clf()
plot2([dice[4], dice[5]], ['Cool Light', 'Warm Light'])

plt.clf()
plot2([dice[3], dice[4]], ['No Diffuser', 'Diffuser'])

plt.clf()
plot2([dice[1], dice[2], dice[4]], ['High', 'Low', 'Dark'])

"""
tp, fp, tn, fn = [],[],[],[]
for key in data:
    pl = np.array(data[key])
    tp.append(pl[:, 0])
    fp.append(pl[:, 1])
    tn.append(pl[:, 2])
    fn.append(pl[:, 3])
f_value, p_value = stats.f_oneway(*tp)
print(stats.shapiro(tp[0]))
print(stats.shapiro(tp[1]))
print(stats.shapiro(tp[2]))
print(stats.shapiro(tp[3]))
print(stats.shapiro(tp[4]))
"""
