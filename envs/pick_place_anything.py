
from envs._base_task import Base_Task
from envs._pick_place_task import Pick_Place_Task
from envs.utils import *
import sapien

class pick_place_anything(Pick_Place_Task):
    def load_actors(self):

        self.plate = self.create_object("plate","plate")
        self.apple = self.create_object("apple","apple")
        self.fruit = self.create_object("fruit","fruit")
        self.bottle = self.create_object("bottle","bottle")
        # self.bowl = self.create_object("bowl","bowl")
        self.can = self.create_object("can","can")
        # self.calculator = self.create_object("calculator","calculator")

    def play_once(self):
        self.save_camera_rgb("/home/wangzhuoran/RoboTwin/data/first_img.png",'front_camera')
        # success = self.pick_place(self.apple, self.plate)
        # print("pick place apple:", success)
        # if not success:
        #     return self.info
        success = self.pick_and_place(self.bottle, self.plate)
        print("pick place bottle:", success)
        if not success:
            return self.info

        # Pick and place two blue blocks
        success = self.pick_and_place(self.can, self.plate)
        print("pick place can:", success)
        if not success:
            return self.info
    def check_success(self):
        if self.check_on(self.bottle, self.plate) and self.check_on(self.can, self.plate):
            return True
        return False