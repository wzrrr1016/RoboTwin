from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 323_place_edible_and_safe_tableware_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        # Add edible items
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        # Add safe eating utensil
        self.fork = self.add_actor("fork", "fork")
        # Add unsafe utensil
        self.knife = self.add_actor("knife", "knife")
        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'toycar', 'pot-with-plant', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place edible items into fluted_block
        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Pick place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Pick place hamburg:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.french_fries, self.fluted_block)
        print("Pick place french_fries:", success)
        if not success:
            return self.info

        # Place safe utensil (fork) into fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Pick place fork:", success)
        if not success:
            return self.info

        # Wrong action: place knife into fluted_block
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Pick place knife (wrong):", success)
        if not success:
            return self.info

        # Recovery: place knife onto table
        success = self.pick_and_place(self.knife, self.table)
        print("Pick place knife (recovery):", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all edible items and safe utensils are in the fluted_block
        required_in_container = [self.apple, self.hamburg, self.french_fries, self.fork]
        for item in required_in_container:
            if not self.check_on(item, self.fluted_block):
                return False

        # Check if the knife is on the table (not in the fluted_block)
        if not self.check_on(self.knife, self.table):
            return False

        return True
