from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 308_hot_drink_items_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects used for hot drinks and other relevant items
        self.mug = self.add_actor("mug", "mug")
        self.teanet = self.add_actor("teanet", "teanet")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractors
        distractor_list = ['screwdriver', 'toycar', 'book', 'shoe', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick mug and place it into shoe_box
        success = self.pick_and_place(self.mug, self.shoe_box)
        print("Pick mug:", success)
        if not success:
            return self.info

        # 2. Pick cup_without_handle and place it into shoe_box (wrong)
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Wrong place cup_without_handle:", success)
        if not success:
            return self.info

        # 3. Pick cup_without_handle from shoe_box and place it on table (recovery)
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("Recover cup_without_handle:", success)
        if not success:
            return self.info

        # 4. Pick teanet and place it into shoe_box
        success = self.pick_and_place(self.teanet, self.shoe_box)
        print("Pick teanet:", success)
        if not success:
            return self.info

        # 5. Pick bottle and place it on table
        success = self.pick_and_place(self.bottle, self.table)
        print("Place bottle on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if mug and teanet are in the shoe_box
        mug_in_box = self.check_on(self.mug, self.shoe_box)
        teanet_in_box = self.check_on(self.teanet, self.shoe_box)
        
        # Check if cup_without_handle is on the table (not in shoe_box)
        cup_on_table = self.check_on(self.cup_without_handle, self.table)
        
        # Check if bottle is on the table
        bottle_on_table = self.check_on(self.bottle, self.table)
        
        return mug_in_box and teanet_in_box and cup_on_table and bottle_on_table
