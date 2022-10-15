import plotly.graph_objects as go
import open3d as o3d
import numpy as np
import copy

def modified_write_points3D_text(points3D, path):
    mean_track_length = 0
    HEADER = "# 3D point list with one line of data per point:\n" + \
             "#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)\n" + \
             "# Number of points: {}, mean track length: {}\n".format(len(points3D), mean_track_length)

    with open(path, "w") as fid:
        fid.write(HEADER)
        for _, pt in points3D.items():
            point_header = [pt.id, *pt.xyz, *pt.rgb, pt.error]
            fid.write(" ".join(map(str, point_header)) + " ")
            track_strings = []
#             for image_id, point2D in zip(pt.image_ids, pt.point2D_idxs):
#                 track_strings.append(" ".join(map(str, [image_id, point2D])))
            fid.write(" ".join(track_strings) + "\n")   
    
def modified_write_images_text(images, path):
    if len(images) == 0:
        mean_observations = 0
    else:
        mean_observations = sum((len(img.point3D_ids) for _, img in images.items()))/len(images)
    HEADER = "# Image list with two lines of data per image:\n" + \
             "#   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME\n" + \
             "#   POINTS2D[] as (X, Y, POINT3D_ID)\n" + \
             "# Number of images: {}, mean observations per image: {}\n".format(len(images), mean_observations)

    with open(path, "w") as fid:
        fid.write(HEADER)
        for _, img in images.items():
            image_header = [img.id, *img.qvec, *img.tvec, img.camera_id, img.name]
            first_line = " ".join(map(str, image_header))
            fid.write(first_line + "\n")

            points_strings = []
#             for xy, point3D_id in zip(img.xys, img.point3D_ids):
#                 points_strings.append(" ".join(map(str, [*xy, point3D_id])))
            fid.write(" ".join(points_strings) + "\n")    
    
    

def create_point_cloud(lst, filename):
    """
        Creates a point cloud from given list of points (x, y, z).
        Writes created point cloud to a file with given filename.
    """
    pts = o3d.geometry.PointCloud()
    pts.points.extend(lst)
    try:
        with open(filename, 'w') as f:
            o3d.io.write_point_cloud(filename, pts)
            print(f'File {filename} is created!')
    except FileNotFoundError:
        print('File does not exist')
        
        

def draw_geometries(geometries):
    """
    Extra function to draw geometries (a list of )
    """
    graph_objects = []

    for geometry in geometries:
        geometry_type = geometry.get_geometry_type()
        
        if geometry_type == o3d.geometry.Geometry.Type.PointCloud:
            points = np.asarray(geometry.points)
            colors = None
            if geometry.has_colors():
                colors = np.asarray(geometry.colors)
            elif geometry.has_normals():
                colors = (0.5, 0.5, 0.5) + np.asarray(geometry.normals) * 0.5
            else:
                geometry.paint_uniform_color((1.0, 0.0, 0.0))
                colors = np.asarray(geometry.colors)

            scatter_3d = go.Scatter3d(x=points[:,0], y=points[:,1], z=points[:,2], mode='markers', marker=dict(size=5, color=colors))
            graph_objects.append(scatter_3d)

        if geometry_type == o3d.geometry.Geometry.Type.TriangleMesh:
            triangles = np.asarray(geometry.triangles)
            vertices = np.asarray(geometry.vertices)
            colors = None
            if geometry.has_triangle_normals():
                colors = (0.5, 0.5, 0.5) + np.asarray(geometry.triangle_normals) * 0.5
                colors = tuple(map(tuple, colors))
            else:
                colors = (1.0, 0.0, 0.0)
            
            mesh_3d = go.Mesh3d(x=vertices[:,0], y=vertices[:,1], z=vertices[:,2], i=triangles[:,0], j=triangles[:,1], k=triangles[:,2], facecolor=colors, opacity=0.50)
            graph_objects.append(mesh_3d)
        
    fig = go.Figure(
        data=graph_objects,
        layout=dict(
            scene=dict(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False)
            )
        )
    )
    fig.show()
    
            

def draw_registration_result(source, target, transformation):
    source_temp = copy.deepcopy(source)
    target_temp = copy.deepcopy(target)
    source_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    source_temp.transform(transformation)
    o3d.visualization.draw_geometries = draw_geometries
    o3d.visualization.draw_geometries([source_temp, target_temp])           
    
    
    
    