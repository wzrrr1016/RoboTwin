from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 108_perishables_and_toys_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.toycar = self.add_actor("toycar", "toycar")
        self.red_block = self.add_actor("red_block", "red_block")
        self.apple = self.add_actor("apple", "apple")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'alarm-clock', 'book', 'tissue-box']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Wrongly place toycar on plate
        success = self.pick_and_place(self.toycar, self.plate)
        print("Pick toycar onto plate (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery - Move toycar to shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Recover toycar to shoe_box:", success)
        if not success:
            return self.info

        # Step 3: Place red_block into shoe_box
        success = self.pick_and_place(self.red_block, self.shoe_box)
        print("Place red_block into shoe_box:", success)
        if not success:
            return self.info

        # Step 4: Place apple onto plate
        success = self.pick_and_place(self.apple, self.plate)
        print("Place apple onto plate:", success)
        if not success:
            return self.info

        # Step 5: Place french_fries onto plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french_fries onto plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all objects are in their correct containers
        if (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.red_block, self.shoe_box) and
            self.check_on(self.apple, self.plate) and
            self.check_on(self.french_fries, self.plate)
        ):
            return True
        return False
