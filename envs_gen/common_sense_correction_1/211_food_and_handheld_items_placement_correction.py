from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 211_food_and_handheld_items_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add task objects
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add distractors from task description
        self.add_distractors(['pot-with-plant', 'alarm-clock', 'toycar', 'red_block', 'small-speaker'])

    def play_once(self):
        # 1. Put apple on plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple on plate:", success)
        if not success:
            return self.info
            
        # 2. Wrongly put markpen on plate (needs recovery)
        success = self.pick_and_place(self.markpen, self.plate)
        print("Wrongly place markpen on plate:", success)
        if not success:
            return self.info
            
        # 3. Recovery: Move markpen to shoe_box
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Recover markpen to shoe_box:", success)
        if not success:
            return self.info
            
        # 4. Put french_fries on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french fries on plate:", success)
        if not success:
            return self.info
            
        # 5. Put screwdriver in shoe_box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Place screwdriver in shoe_box:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Check all required placements
        return (
            self.check_on(self.apple, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.markpen, self.shoe_box)
        )
