from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 422_store_play_pieces_and_place_delicate_accessory_on_top_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required actors in the simulation environment."""
        # Add the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add the small solid play pieces (blocks)
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add the delicate office accessory
        self.mouse = self.add_actor("mouse", "mouse")
        
        # Add distractor objects to the environment
        self.add_distractors(["baguette", "dumbbell", "hammer", "pot-with-plant", "olive-oil"])

    def play_once(self):
        """Execute the sequence of robotic actions to complete the task."""
        # Step 1: Place pink block into shoe box
        success = self.pick_and_place(self.pink_block, self.shoe_box)
        print("Place pink_block:", success)
        if not success:
            return self.info

        # Step 2: Place blue block into shoe box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Step 3: (Wrong action) Place mouse into shoe box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Place mouse (wrong):", success)
        if not success:
            return self.info

        # Step 4: (Recovery) Pick mouse from shoe box and place on top
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Recover mouse:", success)
        if not success:
            return self.info

        # Step 5: Place yellow block into shoe box
        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if all small solid play pieces are in the shoe box
        blocks_in_box = (
            self.check_on(self.pink_block, self.shoe_box) and
            self.check_on(self.blue_block, self.shoe_box) and
            self.check_on(self.yellow_block, self.shoe_box)
        )
        
        # Check if the delicate office accessory is on top of the shoe box
        mouse_on_box = self.check_on(self.mouse, self.shoe_box)
        
        # Return True only if all conditions are met
        return blocks_in_box and mouse_on_box
