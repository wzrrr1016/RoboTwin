from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 53_drinkware_and_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.can = self.add_actor("can", "can")
        self.teanet = self.add_actor("teanet", "teanet")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "alarm-clock", "dumbbell", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong action: can into shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Place can into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: can from shoe_box to coaster
        success = self.pick_and_place(self.can, self.coaster)
        print("Recover can to coaster:", success)
        if not success:
            return self.info

        # Place teanet onto coaster
        success = self.pick_and_place(self.teanet, self.coaster)
        print("Place teanet onto coaster:", success)
        if not success:
            return self.info

        # Place blue_block into shoe_box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Place blue_block into shoe_box:", success)
        if not success:
            return self.info

        # Place yellow_block into shoe_box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow_block into shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are in their correct locations
        can_on_coaster = self.check_on(self.can, self.coaster)
        teanet_on_coaster = self.check_on(self.teanet, self.coaster)
        blue_in_shoe = self.check_on(self.blue_block, self.shoe_box)
        yellow_in_shoe = self.check_on(self.yellow_block, self.shoe_box)
        
        return can_on_coaster and teanet_on_coaster and blue_in_shoe and yellow_in_shoe
