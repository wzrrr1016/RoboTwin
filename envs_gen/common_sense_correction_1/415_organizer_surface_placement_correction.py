from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 415_organizer_surface_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.fork = self.add_actor("fork", "fork")
        self.red_block = self.add_actor("red_block", "red_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractors
        distractor_list = ['dumbbell', 'hammer', 'pot-with-plant', 'shoe', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place red_block on organizer
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info
            
        # Place blue_block on organizer
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Place blue_block:", success)
        if not success:
            return self.info
            
        # Wrong placement of tissue-box (disposable hygiene item)
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Wrong tissue-box placement:", success)
        if not success:
            return self.info
            
        # Recovery: Move tissue-box to table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Recover tissue-box:", success)
        if not success:
            return self.info
            
        # Place fork (lightweight reusable utensil) on organizer
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Place fork:", success)
        if not success:
            return self.info
            
        return self.info

    def check_success(self):
        # Verify small solid playthings and utensils are on organizer
        # and disposable items are not
        if (self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block) and
            not self.check_on(self.tissue_box, self.fluted_block)):
            return True
        return False
