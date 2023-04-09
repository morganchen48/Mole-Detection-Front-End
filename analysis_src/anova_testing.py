import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
with open('res.json', 'r') as f:
    data = json.load(f)


def get_metrics(conf_matrix):
    tp, fp, tn, fn = conf_matrix
    if tp == 0:
        return None
    accuracy = (tp + tn) / (tn + fp + fn + tp)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    specificity = tn / (tn + fp)
    f1_score = 2 * precision * recall / (precision + recall)
    return f1_score


metrics = []
for i, key in enumerate(data):
    datum = np.array(data[key])
    metric = [get_metrics(x) for x in datum if not get_metrics(x) is None]
    metrics.append(metric)

f_value, p_value = stats.f_oneway(*metrics)
print(f_value)
print(p_value)

light_intensity = [metrics[0], metrics[1], metrics[3]]
f_value, p_value = stats.f_oneway(*light_intensity)
print(f_value)
print(p_value)
# for i in range(len(metrics)):
#     for j in range(i+1, len(metrics)):
#         _, p = stats.ttest_ind(metrics[i], metrics[j])
#         print(f'P-value for {conditions[i+1]} and {conditions[j+1]} - {p/2}')
