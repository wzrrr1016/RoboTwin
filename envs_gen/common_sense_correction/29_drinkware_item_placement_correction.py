from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 29_drinkware_item_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.teanet = self.add_actor("teanet", "teanet")
        self.knife = self.add_actor("knife", "knife")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        
        # Add distractors
        distractor_list = ["calculator", "table-tennis", "toycar", "alarm-clock", "microphone", "dumbbell"]
        self.add_distractors(distractor_list)
        
        # Check scene setup
        self.check_scene()

    def play_once(self):
        # Place teanet in coaster
        success = self.pick_and_place(self.teanet, self.coaster)
        print("Place teanet:", success)
        if not success:
            return self.info

        # Wrongly place knife in coaster
        success = self.pick_and_place(self.knife, self.coaster)
        print("Wrong knife placement:", success)
        if not success:
            return self.info

        # Correct knife placement in shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Correct knife placement:", success)
        if not success:
            return self.info

        # Place purple block in shoe_box
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Place purple_block:", success)
        if not success:
            return self.info

        # Place orange block in shoe_box
        success = self.pick_and_place(self.orange_block, self.shoe_box)
        print("Place orange_block:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Verify correct placement of all objects
        if (self.check_on(self.teanet, self.coaster) and
            self.check_on(self.knife, self.shoe_box) and
            self.check_on(self.purple_block, self.shoe_box) and
            self.check_on(self.orange_block, self.shoe_box)):
            return True
        return False
