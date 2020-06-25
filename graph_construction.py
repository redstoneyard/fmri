import os
import numpy as np
import nibabel as nib
from nibabel.testing import data_path
import time

class CenTest:
    
    @staticmethod
    def f(fileindex_p, graph_file_p, adjacency_threshold_p, atlas_data_p, region_asc_list_p, region_voxel_count_p):

        start_time = time.clock()
        
        print('Start fetching data', fileindex_p)
            
        # 'P011_TargDM_StimiTBS_E16663_craddock_preprocessed.nii'
        # data_path = 'C:\Anaconda\lib\site-packages\nibabel\tests\data'
        filename = os.path.join('C:\mri_data_2015', fileindex_p)
        img = nib.load(filename)
        data = img.get_data()
    
        
        x_max = data.shape[0]
        y_max = data.shape[1]
        z_max = data.shape[2]
        time_max = data.shape[3]
        
        atlas_x_max = atlas_data_p.shape[0]
        atlas_y_max = atlas_data_p.shape[1]
        atlas_z_max = atlas_data_p.shape[2]
        
        if atlas_x_max != x_max or atlas_y_max != y_max or atlas_z_max != z_max:
            print('Voxel counts not equal.')
        else:
            print('Voxel counts OK.')
        
        
        total_data = {}
        for r in region_asc_list_p:
            total_data[r] = [0 for i in range(time_max)]
        
        print('Begin total_data', time.clock()-start_time)
        
        for x in range(0,x_max):
            for y in range(0,y_max):
                for z in range(0,z_max):
                    for t in range(0,time_max):
                        total_data[atlas_data_p[x][y][z][30]][t] += data[x][y][z][t]
                        
        print('End total_data', time.clock()-start_time)
        
        print('Begin rest', time.clock()-start_time)
                        
        avrg_data_dict = {}
        
        for r in region_asc_list_p:
            avrg_data_dict[r] = [0 for i in range(time_max)]
                        
        for t in range(time_max):
            for r in region_asc_list_p:
                avrg_data_dict[r][t]=(total_data[r][t])/(region_voxel_count_p[r])


        avrg_data = []
        for r in region_asc_list_p:
            avrg_data.append(avrg_data_dict[r])
                
        n_corr = np.corrcoef(avrg_data, bias=0)
        
        graph_file_p.write(fileindex_p)
        
        for i in range(len(region_asc_list_p)):
            for j in range(i+1, len(region_asc_list_p)):
                if n_corr[i][j] >= adjacency_threshold_p:
                    graph_file_p.write(',%i<>%i' % (region_asc_list_p[i], region_asc_list_p[j]))
        
        graph_file_p.write('\n')
        
        print('End rest', time.clock()-start_time)
        
        
    
        
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
            
            

print(atlas_x_max, atlas_y_max, atlas_z_max)


region_asc_list = sorted(region_voxel_count.keys())
        
no_of_regions = len(region_asc_list)
print('Number of Regions = ', no_of_regions) 
print(region_asc_list)
print(region_voxel_count)


os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.getcwd())
print(data_path)

adjacency_threshold = 0.65

graph_file = open('graphs-%f.csv' % adjacency_threshold,'w')



for patient_file in os.listdir('C:\mri_data_2015'):
    CenTest.f(patient_file, graph_file, adjacency_threshold, atlas_data, region_asc_list, region_voxel_count)
    #print patient_btwn_dict
    
    #patient_btwn_seq = patient_file
    #for i in region_asc_list:
        #patient_btwn_seq = patient_btwn_seq + ',' + str(patient_btwn_dict[i])
    #patient_btwn_seq = patient_btwn_seq + '\n'
    #btwn_file.write(patient_btwn_seq)
    

print('end')



