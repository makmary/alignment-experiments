import sys

sys.path.append('/workspace/sk3d/dev.sk_robot_rgbd_data/src')

from skrgbd.data.io import imgio
from skrgbd.calibration.camera_models import load_colmap_camera
from skrgbd.data.io.poses import load_poses

from skrgbd.data.processing.depth_utils.occluded_mesh_rendering import MeshRenderer


def perform_ray_casting(reconstruction,
                       keypoints,
                       cam_model,
                       dtype
                       
                       ):
    
    found_3d_points = {}

    for image_id, image in reconstruction.images.items():

        key_pts = torch.tensor(keypoints[image.name], dtype=dtype)

        ray_dirs_in_cam_space = cam_model.unproject(key_pts.T.to(device, dtype))  # shape is 3, pts_n
        pts_n = ray_dirs_in_cam_space.shape[1]

        cam_to_world = world_to_cam[view_i].inverse()  # 4, 4
        cam_center_in_world_space = cam_to_world[:3, 3]  # 3
        ray_origins_in_world_space = cam_center_in_world_space.unsqueeze(0).expand(pts_n, -1)  # pts_n, 3
        cam_to_world_rot = cam_to_world[:3, :3]
        ray_dirs_in_world_space = ray_dirs_in_cam_space.T @ cam_to_world_rot.T  # pts_n, 3

        casted_rays = torch.cat([ray_origins_in_world_space, ray_dirs_in_world_space], 1)  # pts_n, 6
        renderer.occ_threshold = 1e-3

        hit_depth = renderer.render_rays(casted_rays, cull_back_faces=True)['ray_hit_depth']

        did_hit = hit_depth.isfinite()
        idxs_with_inf = (did_hit==False).nonzero().squeeze()

        pts_3d = (ray_dirs_in_world_space * hit_depth.unsqueeze(1) + ray_origins_in_world_space) 
        inf_array = np.asarray([np.inf, np.inf, np.inf])

        pts_3d[idxs_with_inf] = torch.from_numpy(inf_array).to(pts_3d) 
        found_3d_points[image.name] = list(pts_3d.numpy()) 
        
        return found_3d_points