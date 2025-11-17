from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 393_wear_and_play_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.plate = self.add_actor("plate", "plate")

        # Add required objects
        self.shoe = self.add_actor("shoe", "shoe")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.toycar = self.add_actor("toycar", "toycar")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")

        # Add distractors
        distractor_list = ['calculator', 'hammer', 'screwdriver', 'stapler', 'mouse']
        self.add_distractors(distractor_list)

    def play_once(self):
        # First wrong action: shoe to plate
        success = self.pick_and_place(self.shoe, self.plate)
        print("Wrong place shoe on plate:", success)
        if not success:
            return self.info

        # Recovery: shoe from plate to shoe_box
        success = self.pick_and_place(self.shoe, self.shoe_box)
        print("Recovery: shoe to shoe_box:", success)
        if not success:
            return self.info

        # Correct actions
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Shampoo to shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.toycar, self.plate)
        print("Toycar to plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.sand_clock, self.plate)
        print("Sand-clock to plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all required objects are in their correct containers
        if (self.check_on(self.shoe, self.shoe_box) and
            self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.toycar, self.plate) and
            self.check_on(self.sand_clock, self.plate)):
            return True
        return False
