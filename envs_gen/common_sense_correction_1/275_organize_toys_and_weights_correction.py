from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 275_organize_toys_and_weights_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Create the main container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create the objects to be manipulated
        self.green_block = self.add_actor("green_block", "green_block")
        self.red_block = self.add_actor("red_block", "red_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractor objects to the environment
        distractor_list = ["scanner", "sand-clock", "microphone", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions"""
        # 1. Place green_block into fluted_block
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green_block:", success)
        if not success:
            return self.info

        # 2. Place toycar into fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info

        # 3. (Wrong) Place dumbbell into fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Place dumbbell (wrong):", success)
        if not success:
            return self.info

        # 4. (Recovery) Place dumbbell on top of fluted_block
        success = self.pick_and_place(self.dumbbell, self.fluted_block)
        print("Place dumbbell (recovery):", success)
        if not success:
            return self.info

        # 5. Place red_block into fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all small items are in the container
        small_items_in = (
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block) and
            self.check_on(self.red_block, self.fluted_block)
        )
        
        # Check if the heavy item is on top of the container
        heavy_item_on_top = self.check_on(self.dumbbell, self.fluted_block)
        
        return small_items_in and heavy_item_on_top
