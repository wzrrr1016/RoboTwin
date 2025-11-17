from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 375_coaster_for_small_items_shoebox_for_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: shoe_box and coaster
        - Objects: bottle, mouse, hammer, drill
        - Distractors: baguette, apple, chips-tub, french_fries, hamburg
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box_0")
        self.coaster = self.add_actor("coaster", "coaster_0")

        # Add objects
        self.bottle = self.add_actor("bottle", "bottle_0")
        self.mouse = self.add_actor("mouse", "mouse_0")
        self.hammer = self.add_actor("hammer", "hammer_0")
        self.drill = self.add_actor("drill", "drill_0")

        # Add distractors
        distractors = ["baguette", "apple", "chips-tub", "french_fries", "hamburg"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Define the sequence of actions the robot should perform in the simulation.
        - First, place the mouse into the shoe_box (wrong action).
        - Then, recover by placing the mouse onto the coaster.
        - Place the bottle onto the coaster.
        - Place the hammer and drill into the shoe_box.
        """
        # Wrong action: place mouse into shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Place mouse into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Recovery: place mouse onto coaster
        success = self.pick_and_place(self.mouse, self.coaster)
        print("Recover mouse to coaster:", success)
        if not success:
            return self.info

        # Place bottle onto coaster
        success = self.pick_and_place(self.bottle, self.coaster)
        print("Place bottle on coaster:", success)
        if not success:
            return self.info

        # Place hammer into shoe_box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Place hammer into shoe_box:", success)
        if not success:
            return self.info

        # Place drill into shoe_box
        success = self.pick_and_place(self.drill, self.shoe_box)
        print("Place drill into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Mouse and bottle should be on the coaster.
        - Hammer and drill should be in the shoe_box.
        """
        if (self.check_on(self.mouse, self.coaster) and
            self.check_on(self.bottle, self.coaster) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.drill, self.shoe_box)):
            return True
        return False
