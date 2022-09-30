#!/bin/bash

set -e

while getopts "n:" flag; do
    case "${flag}" in
        n) objectName=${OPTARG};;
	*) echo 'error' >&2
	   exit 1
    esac
done

echo "Object name: $objectName";

home_path='/home/m.makarova/workspace'

images_path=$home_path'/datasets/sk3d/dataset/'$objectName'/tis_right/rgb/'
calibrated_images_path=$home_path'/datasets/sk3d/dataset/calibration/tis_right/rgb/'

cameras_path=$home_path'/datasets/sk3d/dataset/calibration/tis_right/rgb/'
cleaned_mesh_path=$home_path'/datasets/sk3d/dataset/'$objectName'/stl/reconstruction/'
occlusion_mesh_path=$home_path'/datasets/sk3d/dataset/'$objectName'/stl/'
all_images_path=$home_path'/datasets/sk3d/dataset/'$objectName'/tis_right/rgb/undistorted/ambient@best/'

mkdir -p $images_path
cp -r /mnt/datasets/sk3d/dataset/$objectName/tis_right/rgb/images.txt $images_path
echo "Images.txt copied!" 

mkdir -p $calibrated_images_path
cp -r /mnt/datasets/sk3d/dataset/calibration/tis_right/rgb/images.txt $calibrated_images_path
echo "Calibrated images.txt copied!" 


mkdir -p $cameras_path
cp -r /mnt/datasets/sk3d/dataset/calibration/tis_right/rgb/cameras.txt $cameras_path
echo "Cameras.txt copied!" 


mkdir -p $cleaned_mesh_path
cp -r /mnt/datasets/sk3d/dataset/$objectName/stl/reconstruction/cleaned.ply $cleaned_mesh_path
echo "Cleaned.ply copied!" 

mkdir -p $occlusion_mesh_path
cp -r /mnt/datasets/sk3d/dataset/$objectName/stl/occluded_space.ply $occlusion_mesh_path
echo "Occluded_space.ply copied!" 

images='/mnt/datasets/sk3d/dataset/'$objectName'/tis_right/rgb/undistorted/ambient@best'
mkdir -p $all_images_path
cp -r $images/* $all_images_path
echo "All 100 images copied!"

