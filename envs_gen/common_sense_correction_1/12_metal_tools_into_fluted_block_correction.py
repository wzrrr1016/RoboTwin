from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 12_metal_tools_into_fluted_block_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the fluted_block container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add metal tools and toy blocks
        self.hammer = self.add_actor("hammer", "hammer")
        self.stapler = self.add_actor("stapler", "stapler")
        self.red_block = self.add_actor("red_block", "red_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add distractors to the environment
        distractor_list = ['apple', 'baguette', 'tissue-box', 'shoe', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        """
        # Place metal tools into the fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Hammer into fluted_block:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Stapler into fluted_block:", success)
        if not success:
            return self.info
        
        # Place lightweight toy blocks on the fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Red block on fluted_block:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Purple block on fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking object positions.
        """
        # Check if all required objects are on the fluted_block
        return (
            self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.stapler, self.fluted_block) and
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.purple_block, self.fluted_block)
        )
