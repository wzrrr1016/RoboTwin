from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 303_store_nonperishables_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment"""
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.book = self.add_actor("book", "book")
        self.mug = self.add_actor("mug", "mug")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add distractor objects
        distractor_list = ["red_block", "green_block", "blue_block", "yellow_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions"""
        # Place durable non-perishable items in the wooden box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Place book in box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Place mug in box:", success)
        if not success:
            return self.info

        # Wrong action - place living item in box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Wrong: Place plant in box:", success)
        if not success:
            return self.info

        # Recovery - place living item on top of box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Recovery: Place plant on box:", success)
        if not success:
            return self.info

        # Place perishable item on top of box
        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("Place hamburger on box:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check durable non-perishable items are in the box
        book_in_box = self.check_on(self.book, self.wooden_box)
        mug_in_box = self.check_on(self.mug, self.wooden_box)
        
        # Check living and perishable items are on top of the box
        plant_on_box = self.check_on(self.pot_with_plant, self.wooden_box)
        hamburger_on_box = self.check_on(self.hamburg, self.wooden_box)
        
        return all([book_in_box, mug_in_box, plant_on_box, hamburger_on_box])
