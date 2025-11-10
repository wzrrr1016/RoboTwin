
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class pick_place_anything_imagine(Imagine_Task):
    def load_actors(self):

        self.plate = self.add_actor("wooden_box","plate")
        self.object = self.add_actor("bottle","object")
        # self.apple = self.add_actor("apple","apple")
        # self.fruit = self.add_actor("fruit","fruit")
        # self.bottle = self.add_actor("bottle","bottle")
        # self.bowl = self.add_actor("bowl","bowl")
        # self.can = self.add_actor("can","can")
        # self.calculator = self.add_actor("calculator","calculator")
        distractor_list = ["apple","fruit","bowl","can","calculator","blue_block","red_block","green_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        self.save_camera_rgb("/home/wangzhuoran/RoboTwin/data/first_img.png",'front_camera')
        success = self.pick_and_place(self.object, self.plate)
        print("pick place object:", success)
        if not success:
            return self.info
        # success = self.pick_and_place(self.bottle, self.plate)
        # print("pick place bottle:", success)
        # if not success:
        #     return self.info

        # Pick and place two blue blocks
        # success = self.pick_and_place(self.can, self.plate)
        # print("pick place can:", success)
        # if not success:
        #     return self.info

        # success = self.pick_and_place(self.fruit, self.plate)
        # print("pick place fruit:", success)
        # if not success:
        #     return self.info
    def check_success(self):
        if self.check_on(self.object, self.plate):
            return True
        return False