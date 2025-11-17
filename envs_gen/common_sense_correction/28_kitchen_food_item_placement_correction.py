from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 28_kitchen_food_item_placement_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects that need to be manipulated
        self.bread = self.add_actor("bread", "bread")
        self.teanet = self.add_actor("teanet", "teanet")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.scanner = self.add_actor("scanner", "scanner")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors to the environment
        distractor_list = ['pet-collar', 'table-tennis', 'pot-with-plant', 'shoe', 'dumbbell']
        self.add_distractors(distractor_list)
        
        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        """Execute the sequence of robot actions for the task"""
        # Wrong action: place small-speaker into plate
        success = self.pick_and_place(self.small_speaker, self.plate)
        print("Wrong action - place small-speaker into plate:", success)
        if not success:
            return self.info

        # Recovery: place small-speaker back on table
        success = self.pick_and_place(self.small_speaker, self.table)
        print("Recovery action - place small-speaker back on table:", success)
        if not success:
            return self.info

        # Correct actions
        success = self.pick_and_place(self.bread, self.plate)
        print("Place bread into plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.teanet, self.plate)
        print("Place teanet into plate:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if both correct food-related items are in the plate
        return self.check_on(self.bread, self.plate) and self.check_on(self.teanet, self.plate)
