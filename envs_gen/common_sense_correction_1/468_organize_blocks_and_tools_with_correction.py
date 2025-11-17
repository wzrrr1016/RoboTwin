from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 468_organize_blocks_and_tools_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the lightweight square toy blocks
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add the metal office tool
        self.stapler = self.add_actor("stapler", "stapler")
        
        # Add distractors
        distractor_list = ['apple', 'baguette', 'pot-with-plant', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place each block into the organizer
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue block:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Place green block:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Place purple block:", success)
        if not success:
            return self.info
        
        # Wrong action: place stapler into the organizer
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Wrong stapler placement:", success)
        if not success:
            return self.info
        
        # Recovery action: place stapler on top of the organizer
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Recover stapler placement:", success)
        if not success:
            return self.info
        
        return self.info

    def check_success(self):
        # Check if all blocks are in the organizer
        blocks_in_organizer = (
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.purple_block, self.fluted_block)
        )
        
        # Check if the stapler is on top of the organizer
        stapler_on_top = self.check_on(self.stapler, self.fluted_block)
        
        return blocks_in_organizer and stapler_on_top
