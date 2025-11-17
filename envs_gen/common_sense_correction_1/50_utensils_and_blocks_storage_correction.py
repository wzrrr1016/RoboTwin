from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 50_utensils_and_blocks_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add objects
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.green_block = self.add_actor("green_block", "green_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add distractors
        distractors = ["calculator", "pet-collar", "alarm-clock", "book", "tissue-box", "pot-with-plant"]
        self.add_distractors(distractors)

    def play_once(self):
        # Wrong action: Place fork into shoe_box
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("Place fork into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery action: Move fork to plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Recover fork to plate:", success)
        if not success:
            return self.info

        # Place knife on plate
        success = self.pick_and_place(self.knife, self.plate)
        print("Place knife on plate:", success)
        if not success:
            return self.info

        # Place blocks into shoe_box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Place blue_block into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.green_block, self.shoe_box)
        print("Place green_block into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.shoe_box)
        print("Place yellow_block into shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if fork and knife are on the plate
        fork_on_plate = self.check_on(self.fork, self.plate)
        knife_on_plate = self.check_on(self.knife, self.plate)

        # Check if blocks are in shoe_box
        blue_in_shoe = self.check_on(self.blue_block, self.shoe_box)
        green_in_shoe = self.check_on(self.green_block, self.shoe_box)
        yellow_in_shoe = self.check_on(self.yellow_block, self.shoe_box)

        return fork_on_plate and knife_on_plate and blue_in_shoe and green_in_shoe and yellow_in_shoe
