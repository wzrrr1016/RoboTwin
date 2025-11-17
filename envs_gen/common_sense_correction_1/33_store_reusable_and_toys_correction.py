from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 33_store_reusable_and_toys_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment"""
        # Add containers
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects to be manipulated
        self.fork = self.add_actor("fork", "fork")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects
        distractor_list = ['apple', 'baguette', 'chips-tub', 'french_fries', 'hamburg']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # 1. Pick fork and place it into fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Pick fork:", success)
        if not success:
            return self.info

        # 2. Pick tissue-box and place it into fluted_block (wrong action)
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Place tissue-box wrong:", success)
        if not success:
            return self.info

        # 3. Pick tissue-box and place it on table (recovery)
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Recover tissue-box:", success)
        if not success:
            return self.info

        # 4. Pick pink_block and place it into fluted_block
        success = self.pick_and_place(self.pink_block, self.fluted_block)
        print("Pink block:", success)
        if not success:
            return self.info

        # 5. Pick blue_block and place it into fluted_block
        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Blue block:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all durable/reusable items and toys are in the fluted_block
        if (self.check_on(self.fork, self.fluted_block) and
            self.check_on(self.pink_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block)):
            return True
        return False
