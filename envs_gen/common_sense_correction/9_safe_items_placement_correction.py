from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 9_safe_items_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Add the objects to be sorted
        self.knife = self.add_actor("knife", "knife")
        self.fork = self.add_actor("fork", "fork")
        self.mouse = self.add_actor("mouse", "mouse")
        self.microphone = self.add_actor("microphone", "microphone")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        
        # Add distractor objects
        distractor_list = ['pet-collar', 'sand-clock', 'shoe', 'book', 'tissue-box', 'dumbbell']
        self.add_distractors(distractor_list)
        
        # Verify scene setup
        self.check_scene()

    def play_once(self):
        # Initial wrong placement of knife on plate
        success = self.pick_and_place(self.knife, self.plate)
        print("Pick and place knife into plate (wrong):", success)
        if not success:
            return self.info

        # Recovery: move knife to table
        success = self.pick_and_place(self.knife, self.table)
        print("Pick knife from plate and place on table (recovery):", success)
        if not success:
            return self.info

        # Place safe items on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Place fork on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.plate)
        print("Place mouse on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.microphone, self.plate)
        print("Place microphone on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.plate)
        print("Place blue_block on plate:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Verify all safe items are on the plate and dangerous items are on the table
        if (self.check_on(self.knife, self.table) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.mouse, self.plate) and
            self.check_on(self.microphone, self.plate) and
            self.check_on(self.blue_block, self.plate)):
            return True
        return False
