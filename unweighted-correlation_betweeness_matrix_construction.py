#written in Python2.7

import os
import numpy as np
import nibabel as nib
from nibabel.testing import data_path
import time
import networkx as nx
        
        
atlasname = os.path.join(data_path, 'tcorr05_mean_all.nii')
atlas_img = nib.load(atlasname)
atlas_data = atlas_img.get_data()
# 46 x 55 x 46 for craddock
# 47 x 56 x 46 for tcorr05_mean_all.nii

atlas_x_max = atlas_data.shape[0]
atlas_y_max = atlas_data.shape[1]
atlas_z_max = atlas_data.shape[2]


region_voxel_count = {}

for x in range(0,atlas_x_max):
    for y in range(0,atlas_y_max):
        for z in range(0,atlas_z_max):
            current_region = atlas_data[x][y][z][30] #Map 30 - 313 regions up to label 350
            if current_region in region_voxel_count:
                region_voxel_count[current_region] += 1
            else:
                region_voxel_count[current_region] = 1
            
            

print atlas_x_max, atlas_y_max, atlas_z_max


region_asc_list = sorted(region_voxel_count.keys())
        
no_of_regions = len(region_asc_list)
print 'Number of Regions = ', no_of_regions    
print region_asc_list
print region_voxel_count


os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.getcwd())
print(data_path)

adjacency_threshold = 0.60

max_shift = 6

graph_file = open('sliding-weighted-graphs-%i-313.csv' % max_shift, 'r')

matrix_file = open('unweighted-correlation-betweenness-matrix-%i-%f.csv' % (max_shift, adjacency_threshold),'w')

comps = []

for line in graph_file:
    start_time = time.clock()
    G = nx.Graph()
    line = (line.rstrip()).split(',')
    for i in range(1,len(line)):
        edge = line[i].split('<>')
        if float(edge[3]) > adjacency_threshold:
            G.add_edge(int(edge[0]), int(edge[1]))
    bc = nx.betweenness_centrality(G, weight = None)
    print(line[0])
    comps.append(nx.number_connected_components(G))
    print comps[-1]
    matrix_file.write(line[0])
    for i in region_asc_list:
        if i in G.nodes():
            matrix_file.write(','+str(bc[i]))
        else:
            matrix_file.write(',0.0')
    matrix_file.write('\n')
    print time.clock()-start_time

print sum(comps)

print '--End--'


