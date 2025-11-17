from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 371_toy_and_perishable_organization_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.book = self.add_actor("book", "book")
        self.red_block = self.add_actor("red_block", "red_block")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ["calculator", "mouse", "small-speaker", "stapler", "battery"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions"""
        # Step 1: Place red_block on fluted_block
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block on fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place yellow_block on fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Place yellow_block on fluted_block:", success)
        if not success:
            return self.info

        # Step 3: Place book on fluted_block (wrong placement)
        success = self.pick_and_place(self.book, self.fluted_block)
        print("Place book on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery - Move book to shoe_box
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Move book to shoe_box (recovery):", success)
        if not success:
            return self.info

        # Step 5: Place apple in shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Place apple in shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all objects are in their correct final positions"""
        return (
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.book, self.shoe_box) and
            self.check_on(self.apple, self.shoe_box)
        )
