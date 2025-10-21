from ._GLOBAL_CONFIGS import *
from ._base_task import Base_Task
from .utils import *
from .utils.get_model import *
from .utils.grasp_pose import *
import sapien
import math
import numpy as np


class Pick_Place_Task(Base_Task):  

    def setup_demo(self, **kwags):
        super()._init_task_env_(**kwags)
    
    def add_actor(self, object_type, object_name, object_pose = None):
        modelname, model_type, scale = get_modelname(object_type)
        model_id = get_model_id(object_type)
        rotate_lim, rotate_rand, qpos, is_static, convex = get_args_from_modeltype(model_type, model_id)
        # print("create object:",object_name, " type:",object_type," model:",modelname," id:",model_id)
        if object_pose is None:
            object_pose = rand_pose(
                xlim=[-0.25, 0.25],
                ylim=[-0.25, 0.1],
                zlim=[0.743],
                rotate_rand=rotate_rand,
                rotate_lim=rotate_lim,
                qpos=qpos,
                prohibit_area=self.prohibited_area,
            )
        actor = create_actor(
            scene=self,
            pose=object_pose,
            modelname=modelname,
            convex=convex,
            is_static=is_static,
            scale=scale,
            model_id=model_id,
        )

        self.add_prohibit_area(actor,padding=0.02)
        actor.set_name(object_name)
        actor.set_object_type(object_type)
        return actor

    
    def create_box_pose(self,num, block_half_size=0.02):
        block_pose_lst = []
    
        for i in range(num):
            block_pose = rand_pose(
                xlim=[-0.25, 0.25],
                ylim=[-0.2, 0.15],
                zlim=[0.741 + block_half_size],
                qpos=[1, 0, 0, 0],
                ylim_prop=True,
                rotate_rand=True,
                rotate_lim=[0, 0, 0.75],
            )

            def check_block_pose(block_pose):
                for j in range(len(block_pose_lst)):
                    if (np.sum(pow(block_pose.p[:2] - block_pose_lst[j].p[:2], 2)) < 0.01):
                        return False
                return True

            while not check_block_pose(block_pose):

                block_pose = rand_pose(
                    xlim=[-0.2, 0.2],
                    ylim=[-0.1, 0.1],
                    zlim=[0.741 + block_half_size],
                    qpos=[1, 0, 0, 0],
                    ylim_prop=True,
                    rotate_rand=True,
                    rotate_lim=[0, 0, 0.75],
                )

            block_pose_lst.append(deepcopy(block_pose))

        return block_pose_lst

    def create_block(self, block_pose, color_name, block_half_size=0.02):
        color = get_color(color_name)
        return create_box(
            scene=self,
            pose=block_pose,
            half_size=(block_half_size, block_half_size, block_half_size),
            color=color,
            name="box",
        )

    def get_grasp_pose_from_zerograsp(
        self,
        actor: Actor,
        camera_name='front_camera',
    ):
        self._update_render()
        self.cameras.update_picture()
        rgb_img = self.cameras.get_rgb()[camera_name]['rgb']
        depth_img = self.cameras.get_depth()[camera_name]['depth']
        seg_img = self.cameras.get_segmentation(level='actor')[camera_name]['actor_segmentation']
        camera_config = self.cameras.get_config()[camera_name]
        instrinsic_cv = camera_config['intrinsic_cv']
        cam2world_gl = camera_config['cam2world_gl']
        # print("instrinsic_cv:", instrinsic_cv)
        # print("cam2world_gl:", cam2world_gl)

        actor_point = actor.get_pose().p
        try:
            contact_points = []
            contact_point = actor.get_contact_point(idx=0,ret='pose').p
            for i, contact_point in actor.iter_contact_points("pose"):
                contact_points.append(contact_point.p)
            contact_point = np.mean(contact_points, axis=0)
                
        except:
            contact_point = actor_point
        cam_point = world_to_pixel(contact_point, cam2world_gl, instrinsic_cv)[0]
        # self.last_point = cam_point
        if cam_point[0] > seg_img.shape[1] or cam_point[1] > seg_img.shape[0] or cam_point[0] < 0 or cam_point[1] < 0:
            print("actor out of sight!")
            return None,None
        pixel = [int(np.round(cam_point[0])), int(np.round(cam_point[1]))]
        seg_img = rgb_to_P(seg_img)
        actor_color = np.array(seg_img)[pixel[1],pixel[0]]

        grasp_poses_cam = self.grasp_getter.get_pose(rgb_img,depth_img,seg_img,instrinsic_cv, actor_color)
        grasp_poses_world = camera_to_world(grasp_poses_cam, cam2world_gl)
        best_pose = choose_best_grasp(grasp_poses_world)
        # print("zerograsp grasp pose: ",best_pose)
        return best_pose, cam_point
    

    def get_place_pose_from_container(self,container: Actor):

        self._update_render()
        self.cameras.update_picture()
        seg_img = self.cameras.get_segmentation(level='actor')['front_camera']['actor_segmentation']
        seg_img = rgb_to_P(seg_img)
        camera_config = self.cameras.get_config()['front_camera']
        instrinsic_cv = camera_config['intrinsic_cv']
        cam2world_gl = camera_config['cam2world_gl']
        pose = container.get_pose().p

        cam_point = world_to_pixel(pose,cam2world_gl,instrinsic_cv)[0]
        pixel = [int(np.round(cam_point[0])), int(np.round(cam_point[1]))]
        seg_img_origin = rgb_to_P(self.seg_img_origin)
        seg_array_origin = np.array(seg_img_origin)
        seg_array = np.array(seg_img)
        color_origin = seg_array_origin[pixel[1],pixel[0]]
        mask = seg_array_origin == color_origin

        cl_num = np.unique(seg_array[mask])
        if len(cl_num) == 1:
            container_pose = pose
        else:
            try:
                container_color = get_container_color_simple(seg_array,mask)
                new_mask = seg_array == container_color
                container_point = get_blank_point(new_mask)
                depth_img = self.cameras.get_depth()['front_camera']['depth']
                container_pose = pixel_to_world(container_point,cam2world_gl,instrinsic_cv,depth_img)[0]
            except Exception as e:
                container_pose = np.array([pose[0]-0.01,pose[1]+0.02,pose[2]])
        if np.all(abs(pose[:3] - container_pose[:3]) > np.array([0.1,0.1,0.15])):

            container_pose = np.array([pose[0]-0.01,pose[1]+0.02,pose[2]])

        point = world_to_pixel(container_pose,cam2world_gl,instrinsic_cv)[0]
        # print("container_pose:",container_pose)
        
        return container_pose.tolist()+[0.5312539375275843, -0.46665886518430555, 0.4666393704291426, 0.5312687223729883],point
 


    def pick(self, target, arm_tag=ArmTag('left')):
        # print("pick ",target.get_name())
        self.move(self.open_gripper(arm_tag=arm_tag))
        self.plan_success = True
        if get_grasp_type(target.get_object_type()) == "predict":
            grasp_pose, grasp_point = self.get_grasp_pose_from_zerograsp(target)
            use_contact_point = False
        else:
            use_contact_point = True
            grasp_pose = None
        # grasp_pose, grasp_point = self.get_grasp_pose_from_zerograsp(target)
        # grasp_point = target.get_pose().p
        # quat = GRASP_DIRECTION_DIC['down_right']
        # grasp_pose = [grasp_point[0],grasp_point[1],grasp_point[2],quat[0],quat[1],quat[2],quat[3]]
        frame_idx = self.FRAME_IDX
        action_str = "pick"
        self.add_subplan(action_str, frame_idx, [target.get_name()])
        self.move(
            self.grasp_actor(
                target, 
                arm_tag=arm_tag, 
                pre_grasp_dis=0.1, 
                grasp_dis=0.0,
                use_contact_point=use_contact_point,
                grasp_pose = grasp_pose
                ),  # arm_tag
        )
        # print('grasp done \n plan_success:',self.plan_success)

        if not self.plan_success:
            return False

        # print("pick move up")
        self.move(self.move_by_displacement(arm_tag=arm_tag, z=0.2,move_axis="world"))
        # self.get_scene_contact()
        is_grasp = self.check_grasp(target)

        # print("check grasp success:",is_grasp)
        return is_grasp
    

    
    def place(self, target, container, arm_tag=ArmTag('left')):
        # print("place ",target.get_name()," into ",container.get_name())
        self.plan_success = True
        place_pose, place_point = self.get_place_pose_from_container(container)
        frame_idx = self.FRAME_IDX
        action_str = "place"
        self.add_subplan(action_str, frame_idx, [target.get_name(),container.get_name()])
        self.move(
            self.place_actor(
                target,
                container,
                target_pose = place_pose,
                use_functional_point=False,
                arm_tag=arm_tag,
                pre_dis=0.23,
                dis=0.14,
            ))
        # print('place plan success: ',self.plan_success)
        
        if not self.plan_success:
            return False
        # print("place move up")
        self.move(self.move_by_displacement(arm_tag=arm_tag,z=0.15, move_axis="world"))  # arm_tag

        # print("check success")
        # target_pose = target.get_pose().p
        # container_pose = container.get_pose().p
        # eps = np.array([0.08, 0.08, 0.1])

        success = self.check_actors_contact(target, container)
        # print("place success:",success)
        return success

    def pick_and_place(self, target, container, arm_tag=ArmTag('left'), try_times=0):

        # success = self.check_actors_contact(target, container)
        success = self.check_on(target, container)
        if success:
            return True
        
        self.move(self.move_by_displacement(arm_tag=ArmTag("left"), z=0.1, move_axis="world"))
        
        target_pose = target.get_pose().p
        if target_pose[2] < 0.7:
            print("target is too low")
            return False

        ct = 0
        # action = "pick"
        success = False
        while not success:
            success = self.pick(target, arm_tag=arm_tag)
            # print("pick time:",ct)
            ct += 1
            if ct > 3:
                break

        if not success:
            # print("pick failed")
            return False
        
        success = self.place(target, container, arm_tag=arm_tag)

        if not success:
            # print("place failed")
            if try_times < 3:
                # print("try again")
                return self.pick_and_place(target, container, arm_tag=arm_tag, try_times=try_times+1)
            else:
                return False

        return success
    

    def pick_block(self,block):

        arm_tag = ArmTag("left")
        frame_idx = self.FRAME_IDX
        pose = block.get_pose().p
        camera_config = self.cameras.get_config()['front_camera']
        instrinsic_cv = camera_config['intrinsic_cv']
        cam2world_gl = camera_config['cam2world_gl']
        point = world_to_pixel(pose,cam2world_gl,instrinsic_cv)[0]
        action_str = "pick"
        self.add_subplan(action_str, frame_idx, [block.get_name()])
        self.move(self.grasp_actor(block, arm_tag=arm_tag, pre_grasp_dis=0.09))

        self.move(self.move_by_displacement(arm_tag=arm_tag, z=0.15, move_axis="world"))  

        is_grasp = self.check_grasp(block)   

        return is_grasp

    def place_block(self,block,container):
        arm_tag = ArmTag("left")
        
        self.plan_success = True
        place_pose, place_point = self.get_place_pose_from_container(container)
        frame_idx = self.FRAME_IDX
        action_str = "place"
        self.add_subplan(action_str, frame_idx, [block.get_name(),container.get_name()])
        self.move(
            self.place_actor(
                block,
                container,
                target_pose = place_pose,
                use_functional_point=False,
                arm_tag=arm_tag,
                pre_dis=0.1,
                dis=0.03,
            ))
        
        self.move(self.move_by_displacement(arm_tag=arm_tag, z=0.2, move_axis="world"))
        success = self.check_actors_contact(block, container)

        return success

    def pick_place_block(self, block, container):

        success = self.check_actors_contact(block, container)
        if success:
            return True

        target_pose = block.get_pose().p
        if target_pose[2] < 0.7:
            print("target is too low")
            return False

        ct = 0
        action = "pick"
        success = False
        while not success:
            success = self.pick_block(block)
            # print("pick time:",ct)
            ct += 1
            if ct > 3:
                break

        if not success:
            # print("pick failed")
            return False
        
        success = self.place_block(block, container)

        if not success:
            # print("place failed")
            return False

        return success
         

        