import numpy as np
from PIL import Image, ImageDraw
import cv2
import transforms3d as t3d
from copy import deepcopy

def get_pre_grasp_pose(grasp_pose, pre_grasp_dis):
    DIS_END_TO_GRIPPER = 0.1034
    # DIS_END_TO_GRIPPER = 0.08
    pre_grasp_pose = deepcopy(grasp_pose)
    # print("into get_pre_grasp_pose:", pre_grasp_pose)
    pre_grasp_pose = np.array(pre_grasp_pose)

    if pre_grasp_pose.shape == (7,):  # 3个位置 + 4个四元数
        quaternion = pre_grasp_pose[3:7]
        direction_mat = t3d.quaternions.quat2mat(quaternion)
    elif pre_grasp_pose.shape == (4, 4):  # 4x4变换矩阵
        position = pre_grasp_pose[:3, 3]
        direction_mat = pre_grasp_pose[:3, :3]
        quaternion = t3d.quaternions.mat2quat(direction_mat)
        pre_grasp_pose = position.tolist() + quaternion.tolist()
    else:
        raise ValueError(f"Unsupported pose shape: {pre_grasp_pose.shape}")
    
    pre_grasp_pose[:3] += [-DIS_END_TO_GRIPPER-pre_grasp_dis, 0, 0] @ np.linalg.inv(direction_mat)
    if type(pre_grasp_pose) == np.ndarray:
        pre_grasp_pose = pre_grasp_pose.tolist()
    return pre_grasp_pose

def rgb_to_P(img):
    if type(img) == np.ndarray or type(img) == list:
        img = Image.fromarray(img)
    img = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    return img



def world_to_pixel(point, cam2world_gl, instrinsic_cv):

    world2cam_gl = np.linalg.pinv(cam2world_gl)
    point = np.array(point)
    if len(point.shape) == 1:
        point = point.reshape(1, 3)
    # 转为齐次坐标
    point_h = np.hstack((point, np.ones((point.shape[0], 1))))
    

    axis_conversion = np.eye(4)
    # axis_conversion[0, 0] = -1  # 翻转X轴
    axis_conversion[1, 1] = -1  # 翻转Y轴
    axis_conversion[2, 2] = -1  # 翻转Z轴
    
    # # 应用坐标轴转换
    world2cam_cv = axis_conversion @ world2cam_gl
    
    # 变换到相机坐标系
    cam_point_h = (world2cam_cv @ point_h.T).T
    cam_point = cam_point_h[:, :3]

    # print("actor point in cam:",cam_point)
    
    # 投影到像素坐标
    pixel_point_h = (instrinsic_cv @ cam_point.T).T
    pixel_point = pixel_point_h[:, :2] / pixel_point_h[:, 2, np.newaxis]
    
    return pixel_point

def pixel_to_world(pixel_point, cam2world_gl, instrinsic_cv, depth_img):
    
    pixel_point = np.array(pixel_point)
    if pixel_point.ndim == 1:
        pixel_point = pixel_point.reshape(1, 2)
    N = pixel_point.shape[0]
    
    u = pixel_point[:, 0].astype(int)
    v = pixel_point[:, 1].astype(int)
    
    u = np.clip(u, 0, depth_img.shape[1] - 1)
    v = np.clip(v, 0, depth_img.shape[0] - 1)
    
    depth = depth_img[v, u] /1000.0 
    
    pixel_homo = np.hstack((pixel_point, np.ones((N, 1))))
    
    instrinsic_inv = np.linalg.inv(instrinsic_cv)
    
    camera_cv_homo = (instrinsic_inv @ pixel_homo.T).T
    camera_cv = camera_cv_homo * depth[:, np.newaxis]  # 乘以深度值
    
    camera_cv_homo = np.hstack((camera_cv, np.ones((N, 1))))
    
    axis_conversion = np.eye(4)
    axis_conversion[1, 1] = -1  # 翻转Y轴
    axis_conversion[2, 2] = -1  # 翻转Z轴
    
    camera_gl_homo = (axis_conversion @ camera_cv_homo.T).T
    world_homo = (cam2world_gl @ camera_gl_homo.T).T
    
    world_point = world_homo[:, :3]
    
    world_point[depth == 0] = 0
    
    return world_point

def camera_to_world(poses, cam2world_gl):

    axis_conversion = np.eye(4)
    # axis_conversion[0, 0] = -1  # 翻转X轴
    axis_conversion[1, 1] = -1  # 翻转Y轴
    axis_conversion[2, 2] = -1  # 翻转Z轴


    # # 应用坐标轴转换
    cam2world_cv = cam2world_gl @ axis_conversion

    R = cam2world_cv[:3, :3]
    T = cam2world_cv[:3, 3]
    def pose_to_matrix(pose_dict):
        # print("pose_dict:",pose_dict)  # 调试信息，打印姿态字典
        # 提取平移部分
        translation = pose_dict.translation
        # 提取旋转矩阵部分
        rotation = pose_dict.rotation_matrix        
        # 创建4x4齐次变换矩阵
        matrix = np.eye(4)  # 初始化为单位矩阵
        # 设置旋转部分
        matrix[:3, :3] = rotation
        # 设置平移部分
        matrix[:3, 3] = translation
        return matrix
    
    # 将所有pose转换为4x4矩阵
    # print("poses:",poses[0])
    pose_matrices = np.array([pose_to_matrix(pose) for pose in poses])
    
    # 坐标转换
    world_poses = np.zeros_like(pose_matrices)
    world_poses[:, :3, :3] = R @ pose_matrices[:, :3, :3].transpose(0, 2, 1)
    translations = pose_matrices[:, :3, 3]  # 形状为(N,3)
    world_translations = (R @ translations.T).T + T  # 先相乘再转置，然后加上T
    world_poses[:, :3, 3] = world_translations

    return world_poses


def choose_best_grasp(poses):
    target_direction = np.array([0, 0, -1])
    
    # 初始化最佳抓取姿态和最大点积
    best_grasp = np.eye(4)
    max_dot_product = -float('inf')  # 初始化为负无穷
            
    world2arm = np.array([[ 0, 1,  0],
                            [ 0,  0,  -1],
                            [-1,  0,  0]])
    # 遍历所有姿态
    for pose in poses:
        # 提取旋转矩阵
        R = pose[:3, :3]  # 假设pose是一个4x4的齐次变换矩阵
        R_arm = world2arm @ R
        # 提取当前姿态的Z轴方向
        grasp_direction = R_arm[:, 0]
        
        # 计算当前抓取方向与目标方向的点积
        dot_product = np.dot(grasp_direction, target_direction)
        
        # 检查是否更接近目标方向（点积越大，方向越接近）
        if dot_product > max_dot_product:
            max_dot_product = dot_product
            best_grasp[:3,:3] = R_arm
            best_grasp[:3,3] = pose[:3,3]
            if dot_product > 0.88:
                break

    return best_grasp


# def get_container_color_simple(seg_img, container_mask):
#     """
#     通过轮廓采样获取盘子颜色（最简便方法）
#     :param seg_img: 分割图像
#     :param container_mask: 盘子的二值掩码
#     :return: 盘子的主要颜色
#     """
#     # 直接找到盘子轮廓
#     contours, _ = cv2.findContours(container_mask.astype(np.uint8), 
#                                   cv2.RETR_EXTERNAL, 
#                                   cv2.CHAIN_APPROX_SIMPLE)
    
#     # 获取最大轮廓（应该是盘子）
#     largest_contour = max(contours, key=cv2.contourArea)
    
#     # 采样轮廓点上的颜色
#     edge_colors = []
#     for point in largest_contour:
#         x, y = point[0]
#         if 0 <= y < seg_img.shape[0] and 0 <= x < seg_img.shape[1]:
#             edge_colors.append(seg_img[y, x])
    
#     # 计算平均颜色
#     if edge_colors:
#         container_color = np.mean(edge_colors, axis=0).astype(int)
#         return container_color
#     else:
#         return None
    

def get_container_color_simple(seg_img, container_mask):
    """
    通过内缩轮廓获取盘子颜色，避免边缘混合
    :param seg_img: 分割图像
    :param container_mask: 盘子的二值掩码
    :return: 盘子的主要颜色
    """
    # 确保掩码是二值的
    container_mask = container_mask.astype(np.uint8)
    
    # 找到轮廓
    contours, _ = cv2.findContours(container_mask, 
                                  cv2.RETR_EXTERNAL, 
                                  cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None
    
    # 获取最大轮廓（应该是盘子）
    largest_contour = max(contours, key=cv2.contourArea)
    
    # 计算轮廓矩，获取质心
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    
    # 内缩轮廓点（向内偏移10%的距离）
    shrink_factor = 0.9
    inner_points = []
    for point in largest_contour:
        x, y = point[0]
        # 计算从质心到当前点的向量
        dx = x - cx
        dy = y - cy
        # 内缩点
        new_x = int(cx + dx * shrink_factor)
        new_y = int(cy + dy * shrink_factor)
        inner_points.append([new_x, new_y])
    
    # 采样内缩点的颜色
    inner_colors = []
    for x, y in inner_points:
        if 0 <= y < seg_img.shape[0] and 0 <= x < seg_img.shape[1]:
            inner_colors.append(seg_img[y, x])
    
    # 计算平均颜色
    if inner_colors:
        container_color = np.mean(inner_colors, axis=0).astype(int)
        return container_color
    else:
        return None

def find_mask_bounds(mask):
    # 找到mask中值为1或255的像素的坐标
    y_indices, x_indices = np.where(mask > 0)
    
    # 获取最左、最右、最高、最低的坐标
    left = np.min(x_indices)
    right = np.max(x_indices)
    top = np.min(y_indices)
    bottom = np.max(y_indices)
    
    return left, right, top, bottom

def find_inner_mask(mask):
    left, right, top, bottom = find_mask_bounds(mask)
    new_mask = np.zeros_like(mask, dtype=bool)
    
    bounded_mask = mask[top:bottom, left:right]
    
    row_indices, col_indices = np.where(bounded_mask == 1)
    
    # 对每一行进行处理
    for i in range(top, bottom):
        # 找到当前行中mask值为1的列索引
        current_row_ones = col_indices[row_indices == i - top]
        
        if len(current_row_ones) > 0:
            # 找到连续的1之间的0的部分
            for j in range(len(current_row_ones) - 1):
                start = current_row_ones[j] + 1
                end = current_row_ones[j + 1]
                if start < end:
                    # 将这些0的部分标记到new_mask中
                    new_mask[i, left + start:left + end] = True
    
    return new_mask
    

def get_blank_point(mask):
    left,right,top,bottom = find_mask_bounds(mask)
    # print("bound:",left,right,top,bottom)
    fill_mask = find_inner_mask(mask)

    fill_left, fill_right, fill_top, fill_bottom = find_mask_bounds(fill_mask)
    # print("fill bound:",fill_left,fill_right,fill_top,fill_bottom)

    if fill_left-left > right-fill_right:
        S_lr = (fill_left-left)*(bottom-top)
        centre_lr = ((fill_left+left)/2, (bottom+top)/2)
    else:
        S_lr = (right-fill_right)*(bottom-top)
        centre_lr = ((right+fill_right)/2, (bottom+top)/2)

    if fill_top-top > bottom-fill_bottom:
        S_tb = (right-left)*(fill_top-top)
        centre_tb = ((right+left)/2, (fill_top+top)/2)
    else:
        S_tb = (right-left)*(bottom-fill_bottom)
        centre_tb = ((right+left)/2, (bottom+fill_bottom)/2)


    if S_lr > S_tb:
        return centre_lr
    else:
        return centre_tb

def get_blank_point_grid(mask, grid_size=20):
    left,right,top,bottom = find_mask_bounds(mask)
    # print("bound:",left,right,top,bottom)
    # 遍历网格
    for y in range(top, bottom, grid_size):
        for x in range(left, right, grid_size):
            # 提取当前网格
            grid = mask[y:y+grid_size, x:x+grid_size]
            # 检查当前网格是否为空白区域
            if np.all(grid == 1):
                # 计算当前网格的中心点
                center_x = x + grid_size // 2
                center_y = y + grid_size // 2
                return (center_x, center_y)
    
    return None

def visualize_blankpoint(mask, blankpoint=None, grid_size=20):

    if mask.dtype == bool:
        mask = (mask * 255).astype(np.uint8)
    elif mask.dtype != np.uint8:
        mask = mask.astype(np.uint8)

    # 如果 mask 是单通道，转为 RGB 图像以便绘制彩色标记
    if len(mask.shape) == 2:
        pil_image = Image.fromarray(mask, mode='L').convert('RGB')
    else:
        pil_image = Image.fromarray(mask, mode='RGB')

    draw = ImageDraw.Draw(pil_image)
    width, height = pil_image.size
    left,right,top,bottom = find_mask_bounds(mask)
    for x in range(left, right, grid_size):
        draw.line([(x, 0), (x, height)], fill=(200, 200, 200), width=1)
    for y in range(top, bottom, grid_size):
        draw.line([(0, y), (width, y)], fill=(200, 200, 200), width=1)

    # 如果提供了 blankpoint，绘制一个红色圆点
    if blankpoint is not None:
        x, y = blankpoint[:2]
        radius = 5
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(255, 0, 0))

    # 显示图像
    # pil_image.show()

    # 可选：保存图像
    pil_image.save("output_visualization.png")



if __name__ == '__main__':
    # seg_img = Image.open('/home/wangzhuoran/RoboTwin/front_camera_actor_segmentation.png')
    # seg_array = np.array(seg_img)  # 先转换为NumPy数组
    # cl_num = np.unique(seg_array)
    # # print(cl_num)
    # container_color = 10
    # plate_mask = (seg_array == container_color)  # 现在mask是布尔数组
    # mask_uint8 = (plate_mask * 255).astype(np.uint8)
    # mask_img = Image.fromarray(mask_uint8)
    # mask_img.save('mask.png')

    # fruit_color = 12
    # fruit_mask = (seg_array == fruit_color)  # 现在mask是布尔数组
    # fruit_and_plate_mask = fruit_mask | plate_mask
    
    # edge_color = get_container_color_simple(seg_array, fruit_and_plate_mask)
    # print("edge color:",edge_color)
    # new_mask = seg_array == edge_color
    # grid_size = 6
    # blank_point = get_blank_point(new_mask,grid_size=grid_size)
    # print("blank_point:",blank_point)
    # visualize_blankpoint(new_mask, blank_point,grid_size=grid_size)


    seg_img_origin = Image.open('/home/wangzhuoran/RoboTwin/front_camera_actor_segmentation_0.png')
    seg_img = Image.open('/home/wangzhuoran/RoboTwin/front_camera_actor_segmentation.png')
    depth_img = Image.open('/home/wangzhuoran/RoboTwin/front_camera_depth.png')

    cam2world_gl = np.array([[-1.0000002 , 0., 0., 0. ],
                [ 0., -0.7926241,  0.6097109, 0.2],
                [ 0.,  0.6097109, 0.79262394, 1.1],
                [ 0., 0., 0., 1. ]])
    instrinsic_cv = np.array([[120.,0.,160.],[  0., 120., 120.],[  0., 0., 1.]])
    cam_point = [210.80606881, 143.15099266]
    pixel = [int(np.round(cam_point[0])), int(np.round(cam_point[1]))]
    seg_img_origin = rgb_to_P(seg_img_origin)
    seg_array_origin = np.array(seg_img_origin)
    seg_array = np.array(seg_img)
    color_origin = seg_array_origin[pixel[1],pixel[0]]
    mask = seg_array_origin == color_origin

    cl_num = np.unique(seg_array[mask])
    print("cl_num:",len(cl_num))

    if len(cl_num) == 1:
        # container_pose = pose
        print("only one color in mask")
    else:
        container_color = get_container_color_simple(seg_array,mask)
        print("container_color:",container_color)
        new_mask = seg_array == container_color
        mask_uint8 = (new_mask * 255).astype(np.uint8)
        mask_img = Image.fromarray(mask_uint8)
        mask_img.save('mask.png')
        container_point = get_blank_point(new_mask)
        print("blank_point:",container_point)
        visualize_blankpoint(new_mask, container_point)
        
        # container_pose = pixel_to_world(container_point,cam2world_gl,instrinsic_cv,depth_img)[0]