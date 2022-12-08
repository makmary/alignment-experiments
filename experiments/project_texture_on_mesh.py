#!/usr/bin/python3 python3

import os
import argparse
import torch
os.environ["CUDA_VISIBLE_DEVICES"]="0"

import sys

from PIL import Image
import numpy as np
import open3d as o3d
import torch
from tqdm.auto import tqdm

sys.path.append('/workspace/dev.sk_robot_rgbd_data/src')
from skrgbd.calibration.camera_models import load_colmap_camera
from skrgbd.data.depth_utils.mesh_rendering_gl import MeshRenderer
from skrgbd.data.io.poses import Poses

sys.path.append('/workspace/dev.sk_robot_rgbd_data/misc/bits')
from check_projected_texture import get_pts_uv, occlude_pts
from pathlib import Path, PurePath


def project_texture(object_name, render_views_list):
    # Set the working device and dtype. Only float32 at GPUs are supported.
    dtype = torch.float32
    device = 'cuda:0'

    # Load mesh
    rec = f'/workspace/datasets/sk3d/dataset/{object_name}/stl/reconstruction/cleaned.ply'
    rec = o3d.io.read_triangle_mesh(rec)

    # Load occlusion mesh
    occ = f'/workspace/datasets/sk3d/dataset/{object_name}/stl/occluded_space.ply'
    occ = o3d.io.read_triangle_mesh(occ)

    # Load info from one of the experiments' outputs
    root = Path('/workspace')
    outputs = root / f'pixel-perfect-sfm/outputs/{object_name}'
    
    
    first_exp = outputs / 'experiment_1'
    second_exp = outputs / 'experiment_2'
    local_exp = outputs / 'query_localization_known_cameras'
    
    images_mesh =  outputs / 'projected_texture'
    images_mesh.mkdir(parents=True, exist_ok=True)
    
    pixsfm_1_single_ref = first_exp / f'ref_exp1_single_cam/hloc/model_txt/'
    pixsfm_1_single_ref_params =  first_exp / f'ref_exp1_single_cam_with_init_camera_params/hloc/model_txt/'
    

    ## exact and refined cam params
    
    pixsfm_2_bef_refined_ba = second_exp / 'refined/exp_refine_cam_params/hloc/model_txt/'
    pixsfm_2_aft_refined_ba = second_exp / 'refined/exp_refine_cam_params/hloc/model/model_txt/'
    pixsfm_2_after_new_coord_refined_ba = second_exp / 'refined/exp_refine_cam_params/hloc/model/model_txt/model_txt_new_coord/'
    
    ## exact and not refined cam params
    
    pixsfm_2_before_not_refined_ba = second_exp / 'refined/exp_not_refine_cam_params/hloc/model_txt/'
    pixsfm_2_after_not_refined_ba = second_exp / 'refined/exp_not_refine_cam_params/hloc/model/model_txt/'
    pixsfm_2_after_new_coord_not_refined_ba = second_exp / 'refined/exp_not_refine_cam_params/hloc/model/model_txt/model_txt_new_coord/'
     
    ## not exact and refined cam params
   
    pixsfm_2_calibr_before_ba_refined = second_exp / 'calibrated/exp_refine_cam_params/hloc/model_txt/'
    pixsfm_2_calibr_after_ba_refined = second_exp / 'calibrated/exp_refine_cam_params/hloc/model/model_txt/'
    pixsfm_2_calibr_after_ba_new_coord_refined = second_exp / 'calibrated/exp_refine_cam_params/hloc/model/model_txt/model_txt_new_coord/'

    ## not exact and not refined cam params
        
    pixsfm_2_calibr_before_not_refined_ba = second_exp / 'calibrated/exp_not_refine_cam_params/hloc/model_txt/'
    pixsfm_2_calibr_after_not_refined_ba = second_exp / 'calibrated/exp_not_refine_cam_params/hloc/model/model_txt/'
    pixsfm_2_calibr_after_new_coord_not_refined_ba = second_exp / 'calibrated/exp_not_refine_cam_params/hloc/model/model_txt/model_txt_new_coord/'
    
#     pixsfm_3 = outputs / f'{object_name}/ref_exp3/thresh_0.09/model_txt'
#     pixsfm_3_calibr = outputs / f'{object_name}/calibrated/ref_exp3/thresh_0.09/model_txt/'
   
    pixsfm_localizer_known_calibr = local_exp / 'calibrated/result/'
    pixsfm_localizer_known_refined = local_exp / 'refined/result'
    
    pixsfm_localizer_known_refined_optimum = outputs / 'query_localizer_optimum/query_localizer_v1/result'

    all_experiments = {
#                  "exp1_ref" : pixsfm_1_single_ref,
#                  "exp1_ref_gt_intinsics": pixsfm_1_single_ref_params, 
        
#                 "exp2_bef_ba_ref" : pixsfm_2_bef_refined_ba,
#                 "exp2_aft_ba_ref" : pixsfm_2_aft_refined_ba,
#                 "exp2_aft_ba_new_coord_ref":  pixsfm_2_after_new_coord_refined_ba,

#                 "exp2_bef_ba_not_ref" : pixsfm_2_before_not_refined_ba,
# #                 "exp2_aft_ba_not_ref" : pixsfm_2_after_not_refined_ba,
#                 "exp2_aft_ba_new_coord_not_ref":  pixsfm_2_after_new_coord_not_refined_ba,
        
               # "exp3" : pixsfm_3,
        
 
        
#                 "exp2_calibr_bef_ba_ref": pixsfm_2_calibr_before_ba_refined,
#                 "exp2_calibr_aft_ba_ref": pixsfm_2_calibr_after_ba_refined,
#                 "exp2_calibr_aft_ba_new_coord_ref": pixsfm_2_calibr_after_ba_new_coord_refined,

#                 "exp2_calibr_bef_ba_not_ref": pixsfm_2_calibr_before_not_refined_ba,
#                 "exp2_calibr_aft_ba_not_ref": pixsfm_2_calibr_after_not_refined_ba,
#                 "exp2_calibr_aft_ba_new_coord_not_ref": pixsfm_2_calibr_after_new_coord_not_refined_ba,
        
#                  "query_localizer_known_calibr": pixsfm_localizer_known_calibr,
#                 "query_localizer_known_refined": pixsfm_localizer_known_refined,
     "query_localizer_known_optimum": pixsfm_localizer_known_refined_optimum,
                
    }
    
    
#     all_exps_paths = all_experiments.values()
#     #check if all paths exist
#     for path in all_exps_paths:
#         if not path.exists():
#             raise Exception("A path does not exist for this object!")
        
    
    for render_view in render_views_list:    
        render_view = int(render_view)
    
        for exp_name, experiment_path in all_experiments.items():
            print(f"Experiment in {experiment_path}")

            # Load intrinsic camera model    
            cam_model = experiment_path  / 'cameras.txt'

            # Load camera poses
            poses = str(experiment_path / 'images.txt')

            cam_model = load_colmap_camera(str(cam_model))
            cam_model = cam_model.to(device, dtype)

            poses = Poses.from_colmap(poses, dtype)
            world_to_cam = torch.empty(len(poses), 4, 4, device=device, dtype=dtype)

            view_ids = [render_view - 1, render_view, render_view + 1]
            for view_i in view_ids:
                img_i = view_i + 1  # COLMAP's image_id is one-based
                world_to_cam[view_i].copy_(poses[img_i])
            del poses

            # Load images
            imgs = {}
            for view_i in tqdm(view_ids):
                img = f'/workspace/datasets/sk3d/dataset/{object_name}/tis_right/rgb/undistorted/ambient@best/{view_i:04}.png'
                img = Image.open(img)
                img = np.asarray(img)
                img = torch.from_numpy(img).permute(2, 0, 1).to(dtype)  # [channels_n, height, width]
                imgs[view_i] = img; del img

            # Setup the renderer
            renderer = MeshRenderer(rec, device)
            renderer.init_mesh_data()

            renderer.set_cam_model(cam_model, near=.5, far=1.5)   # here we use camera model
            renderer.set_resolution(*imgs[render_view].shape[-2:])

            # Choose the view to render to
            render_view_i = render_view

            # Reproject images to the render view using the mesh as proxy
            rec_verts = np.asarray(rec.vertices)
            rec_verts = torch.from_numpy(rec_verts).to(device, dtype)

            reprojections = dict()
            for view_i in tqdm(view_ids):
                uv = get_pts_uv(rec_verts, cam_model, world_to_cam[view_i])
                vert_is_visible = occlude_pts(rec_verts, occ, world_to_cam[view_i], vis_threshold=1e-3)
                uv = uv.where(vert_is_visible.unsqueeze(1).expand_as(uv), uv.new_tensor(float('nan'))); del vert_is_visible

                rast = renderer.render_to_camera(world_to_cam[render_view_i])
                uv = renderer.interpolate(uv, rast); del rast

                img = imgs[view_i].to(device)
                reprojection = torch.nn.functional.grid_sample(img.unsqueeze(0), uv.unsqueeze(0), mode='bilinear').squeeze(0); del uv, img
                reprojection = reprojection.round_().clamp_(0, 255).permute(1, 2, 0).to('cpu', torch.uint8)
                reprojections[view_i] = reprojection; del reprojection

            
            for view_i in tqdm(view_ids):
                img = Image.fromarray(reprojections[view_i].numpy())
                new_dir = images_mesh / f'{exp_name}'
                new_dir.mkdir(parents=True, exist_ok=True)
                img.save(f'{new_dir}/{exp_name}_{view_i:04}.png'); del img    

    
if __name__ == "__main__":
    if torch.cuda.is_available() != True:
        raise Exception("Cuda is not available!") 
        
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", help="put name of your object")
    parser.add_argument('-l','--list', nargs='+', help='<Required> Set flag', required=True)
    
    args = parser.parse_args()
    object_name = args.name
    render_views_list = args.list
    project_texture(object_name, render_views_list)