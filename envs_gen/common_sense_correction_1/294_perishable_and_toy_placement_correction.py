from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 294_perishable_and_toy_placement_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment."""
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the main objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.red_block = self.add_actor("red_block", "red_block")
        
        # Add distractors as specified in the task
        distractor_list = ['screwdriver', 'stapler', 'pot-with-plant', 'alarm-clock', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions for the task."""
        # Place toycar (solid toy) onto fluted_block
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Place toycar:", success)
        if not success:
            return self.info
        
        # Place bread (perishable edible) into fluted_block
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread:", success)
        if not success:
            return self.info
        
        # Place hamburg (perishable edible) into fluted_block
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Place hamburg:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        """Verify if the task was completed successfully."""
        # Check if all required objects are in the correct positions
        toycar_on = self.check_on(self.toycar, self.fluted_block)
        bread_in = self.check_on(self.bread, self.fluted_block)
        hamburg_in = self.check_on(self.hamburg, self.fluted_block)
        
        # Ensure red_block is not in the container (wrong action not performed)
        red_block_not_in = not self.check_on(self.red_block, self.fluted_block)
        
        return toycar_on and bread_in and hamburg_in and red_block_not_in
