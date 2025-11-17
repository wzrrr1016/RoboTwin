from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 420_place_edibles_in_shoebox_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Add the shoe box as a container.
        - Add edible and non-edible objects.
        - Add distractor objects.
        """
        # Add the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add edible and non-edible objects
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")

        # Add distractor objects
        distractor_list = ["calculator", "alarm-clock", "toycar", "microphone", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform.
        - First, place the screwdriver into the shoe box (wrong action).
        - Then, recover by placing the screwdriver back on the table.
        - Place edible items (apple and hamburg) into the shoe box.
        - Place non-edible items (pot-with-plant) on the table.
        """
        # Wrong action: place screwdriver into shoe box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Put screwdriver into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: place screwdriver back on the table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Put screwdriver on table (recovery):", success)
        if not success:
            return self.info

        # Place edible items into the shoe box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Put apple into shoe_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hamburg, self.shoe_box)
        print("Put hamburg into shoe_box:", success)
        if not success:
            return self.info

        # Place non-edible item on the table
        success = self.pick_and_place(self.pot_with_plant, self.table)
        print("Put pot-with-plant on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Apple and hamburg should be in the shoe box.
        - Screwdriver and pot-with-plant should be on the table.
        """
        apple_in_shoe_box = self.check_on(self.apple, self.shoe_box)
        hamburg_in_shoe_box = self.check_on(self.hamburg, self.shoe_box)
        screwdriver_on_table = self.check_on(self.screwdriver, self.table)
        pot_on_table = self.check_on(self.pot_with_plant, self.table)

        return all([
            apple_in_shoe_box,
            hamburg_in_shoe_box,
            screwdriver_on_table,
            pot_on_table
        ])
