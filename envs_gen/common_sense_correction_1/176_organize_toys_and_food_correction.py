from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 176_organize_toys_and_food_correction(Imagine_Task):
    def load_actors(self):
        # Add the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add solid toy blocks
        self.green_block = self.add_actor("green_block", "green_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        
        # Add food and drinkware
        self.apple = self.add_actor("apple", "apple")
        self.mug = self.add_actor("mug", "mug")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "pot-with-plant", "alarm-clock", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place solid toy blocks into the organizer
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.orange_block, self.fluted_block)
        print("Place orange_block:", success)
        if not success:
            return self.info

        # Wrong placement of apple into the organizer
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Wrong apple placement:", success)
        if not success:
            return self.info

        # Recovery: Move apple to the surface of the organizer
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Recover apple placement:", success)
        if not success:
            return self.info

        # Place mug on the organizer's surface
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all blocks are in the organizer
        blocks_in_organizer = (
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.orange_block, self.fluted_block)
        )
        
        # Check if food and drinkware are on the organizer's surface
        items_on_surface = (
            self.check_on(self.apple, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block)
        )
        
        return blocks_in_organizer and items_on_surface
```
