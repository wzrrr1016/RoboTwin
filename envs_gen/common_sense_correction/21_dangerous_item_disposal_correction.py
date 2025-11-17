from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 21_dangerous_item_disposal_correction(Imagine_Task):
    def load_actors(self):
        # Load required objects
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.knife = self.add_actor("knife", "knife")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'table-tennis', 'roll-paper', 'baguette', 'apple']
        self.add_distractors(distractor_list)

        # Confirm scene setup
        self.check_scene()

    def play_once(self):
        # Step 1: Wrong action - place cup in dustbin
        success = self.pick_and_place(self.cup_without_handle, self.dustbin)
        print("Wrong action (cup in dustbin):", success)
        if not success:
            return self.info

        # Step 2: Recovery - place cup back on table
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("Recovery action (cup back to table):", success)
        if not success:
            return self.info

        # Step 3: Correct action - place knife in dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Correct action (knife in dustbin):", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Task is successful if knife is in dustbin and cup is on the table
        if self.check_on(self.knife, self.dustbin) and self.check_on(self.cup_without_handle, self.table):
            return True
        return False
