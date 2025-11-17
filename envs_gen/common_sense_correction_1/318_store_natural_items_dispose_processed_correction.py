from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 318_store_natural_items_dispose_processed_correction(Imagine_Task):
    def load_actors(self):
        # Define containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Define objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")

        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'hammer', 'toycar', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place apple in wooden_box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Place apple:", success)
        if not success:
            return self.info

        # Place hamburg in dustbin
        success = self.pick_and_place(self.hamburg, self.dustbin)
        print("Place hamburg:", success)
        if not success:
            return self.info

        # Wrong placement of pot-with-plant into dustbin
        success = self.pick_and_place(self.pot_with_plant, self.dustbin)
        print("Wrong placement of pot-with-plant:", success)
        if not success:
            return self.info

        # Recovery: move pot-with-plant to wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Recover pot-with-plant:", success)
        if not success:
            return self.info

        # Place french_fries in dustbin
        success = self.pick_and_place(self.french_fries, self.dustbin)
        print("Place french_fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        return (
            self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.hamburg, self.dustbin) and
            self.check_on(self.pot_with_plant, self.wooden_box) and
            self.check_on(self.french_fries, self.dustbin)
        )
