#import os
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import LeaveOneOut
#from sklearn.model_selection import KFold
from itertools import product
from google.colab import drive

drive.mount('/content/drive')



num_of_features = 5
num_of_trees = 200


start_time = time.clock()

all_data_set = []
all_label_set = []

graph_file = open('/content/drive/My Drive/data_for_colab/unweighted-correlation-betweenness-matrix-6-0.500000.csv','r')

labels_universe = [0, 1, 2]
label_pots = {}

for line in graph_file:
    line = (line.rstrip()).split(',')
    patient_label = int(line[0][0]) 
    patient_data = []
    if patient_label not in labels_universe:
        pass
    else:
        for i in range(1,len(line)):
            patient_data.append(float(line[i]))
        all_data_set.append(patient_data)
        all_label_set.append(patient_label)
        if patient_label in label_pots.keys():
            label_pots[patient_label].append(len(all_data_set) - 1)
        else:
            label_pots[patient_label] = [len(all_data_set) - 1]

    
all_data_set = np.array(all_data_set)
all_label_set = np.array(all_label_set)


all_data_set_reduced = SelectKBest(k = num_of_features).fit_transform(all_data_set, all_label_set)




result_file = open ('result_file.txt','w')

label_pots_lists = []
label_pots_keys = label_pots.keys()
for x in label_pots_keys:
    label_pots_lists.append(label_pots[x])

prediction_count = {}
for x in labels_universe:
    prediction_count[x] = {}
    for y in labels_universe:
        prediction_count[x][y] = 0

loo = LeaveOneOut()
# kf = KFold(n_splits = 5)


for train_index, test_index in loo.split(all_data_set_reduced): # or kf.split(all_data_set_reduced)
    training_data_set, test_data_set = all_data_set_reduced[train_index], all_data_set_reduced[test_index]
    training_label_set, test_label_set = all_label_set[train_index], all_label_set[test_index]
    clf = RandomForestClassifier(n_estimators = num_of_trees, criterion = 'entropy')
    clf.fit(training_data_set, training_label_set)
    #print(test_label_set)
    prediction = clf.predict(test_data_set)
    result_file.write(str(test_label_set)+'\n'+str(prediction)+'\n'+'---\n')
    for i in range(0,len(test_label_set)):
        prediction_count[test_label_set[i]][prediction[i]] += 1
        
print(time.clock()-start_time)

print(label_pots)

print(label_pots_lists)

test_case_label = {}
test_case_prediction = {}

for i in labels_universe:
    test_case_label[i] = 0
    for j in labels_universe:
        test_case_label[i] += prediction_count[i][j]
    test_case_prediction[i] = 0
    for j in labels_universe:
        test_case_prediction[i] += prediction_count[j][i]

for i, j in product(labels_universe, labels_universe):
    print(i, j, prediction_count[i][j], float(prediction_count[i][j])/float(test_case_label[i]))
    
for i, j in product(labels_universe, labels_universe):
    print(j, i, prediction_count[j][i], float(prediction_count[j][i])/float(test_case_prediction[i]))
    
print('--End--')