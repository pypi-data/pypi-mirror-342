# Python-Fiji-Pipeline
This Library includes code related Reticle pipeline workflow.


----- Reticle Pipeline -----

This pipeline includes the following steps:

1. Difference of Gauss. [32 bits] 
-> process_stack(file_path,sigma1,sigma2)  

2. Calculate Binary mask of the step 1 (DoG). [16 bits]
-> process_dog_stack(file_path) 

3. Remove Outliers.  [16 bits]
-> apply_median_filter(file_path, size) 

4. Normalize result of Binary Mask. [32 bits]
-> normalizar_stack(Binarymask_file_path,original_file_path)  

5. Calculate Regions of interest (ROIS), F0, log2(pixel/F0). 
In this step paralellism cpu code is added. [32 bits]
-> process_stack_rois(file_path,roi_size,frame_range)  




