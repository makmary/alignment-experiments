# Pixel-perfect-SfM experiments

This directory contains scripts needed to run PixSfM experiments for Sk3D or custom data.

With `pixsfm`, you can:

- reconstruct and refine a scene using hloc, from scratch or with given camera poses
- localize and refine new query images using hloc
- run the keypoint or bundle adjustments on a COLMAP database or 3D model
- evaluate the refinement with new dense or sparse features on the ETH3D dataset


### Building the image
You can run build the image, which is located in `docker/Dockerfile`, directly via 
```
docker build -t sk3d/pixsfm_experiments:latest -f Dockerfile .
```

### Usage

#### Working with data
To run PixSfM experiments using some sample data from Sk3D or custom dataset, you can 
* run script `scripts/copy_dataset.sh` (we can edit locations in this file, such as `$home_path`)
* copy custom dataset (just images) to `pixel-perfect-sfm/datasets/{scene_name}/mapping`
* copy ready reconstruction (COLMAP outputs) in `pixel-perfect-sfm/outputs/{scene_name}/exp_N` for required experiment


#### Running experiments
Run the PixSfM docker image

```(bash)
docker run \
    --gpus all --rm -it  \
    -v /home/user_name/workspace:/workspace \
    --name sk_pixsfm sk3d/pixsfm_experiments:latest /bin/bash
  
```

Then, run experiments in `pixsfm-experiments/experiments/` to obtain sparse SfM results. 


#### Getting the source data ready
* If you want to run reconstruction using some images, 
you should use the following format of dataset

```
pixel-perfect-sfm   
└── datasets
    └── {scene_name}    
       └── mapping
           ├── 0000.jpg       
           ├── 0001.jpg       
           └── ...  
       └── query
           ├── 0000.jpg       
           ├── 0001.jpg       
           └── ...  
       
```

* If you have ready reconstruction (COLMAP output), 
you should use the following format of data
```
pixel-perfect-sfm   
└── outputs
    └── {scene_name}                 
       └── exp        
           ├── images.txt
           ├── points3D.txt     
           └── cameras.txt 
```

### Code structure
Here is a rough explanation about what goes in `experimnets` folder:
 * `experiments/icp_coordinates.ipynb`: finds transition matrix from one coordinate system to another using the centers of cameras from `images.txt` files, saves updated camera poses to a new file.
 * `experiments/Query_Localizer.ipynb`: runs query localization and refinement for query images from `pixel-perfect-sfm/datasets/{scene_name}/query` by building SfM using images from `pixel-perfect-sfm/datasets/{scene_name}/mapping`

 * `experiments/Query_Localizer_known_camera_poses_sfm.ipynb*`:  
 * `experiments/run_1st_experiment.ipynb`: default pipeline with different configurations to obtain SfM sparse model from given images.
 * `experiments/run_2nd_experiment.ipynb`: reconstruct sparse model from known camera poses using hloc and PixSfM.
 * `experiments/run_3rd_experiment.ipynb`: substitute 3d points of given SfM reconstruction by another GT reconstruction, run feature-metric BA (Bundle Adjustment)


#### Resulting output for all experiments
```
TODO
```
