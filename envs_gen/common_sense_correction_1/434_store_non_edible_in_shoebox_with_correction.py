from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 434_store_non_edible_in_shoebox_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Add the shoe_box as a container.
        - Add the task-specific objects: markpen, apple, teanet, cup_with_handle.
        - Add distractor objects to the environment.
        """
        # Add the shoe_box as a container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")

        # Add task-specific objects
        self.markpen = self.add_actor("markpen", "markpen")
        self.apple = self.add_actor("apple", "apple")
        self.teanet = self.add_actor("teanet", "teanet")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")

        # Add distractor objects
        distractor_list = ['toycar', 'book', 'alarm-clock', 'pot-with-plant', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation.
        - Place non-edible dry tools and drinkware into the shoe_box.
        - Place the apple (a perishable edible item) on top of the shoe_box.
        - Handle a wrong placement and recovery for the apple.
        """
        # 1. Place markpen (non-edible dry tool) into shoe_box
        success = self.pick_and_place(self.markpen, self.shoe_box)
        print("Place markpen into shoe_box:", success)
        if not success:
            return self.info

        # 2. Wrongly place apple into shoe_box (incorrect action)
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Wrongly place apple into shoe_box:", success)
        if not success:
            return self.info

        # 3. Recovery: Place apple on top of shoe_box (correct action)
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Recover: Place apple on top of shoe_box:", success)
        if not success:
            return self.info

        # 4. Place teanet (drinkware) into shoe_box
        success = self.pick_and_place(self.teanet, self.shoe_box)
        print("Place teanet into shoe_box:", success)
        if not success:
            return self.info

        # 5. Place cup_with_handle (drinkware) into shoe_box
        success = self.pick_and_place(self.cup_with_handle, self.shoe_box)
        print("Place cup_with_handle into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - Non-edible items (markpen, teanet, cup_with_handle) should be in the shoe_box.
        - Perishable edible item (apple) should be on top of the shoe_box.
        """
        # Check if all non-edible items are in the shoe_box
        non_edible_in_box = (
            self.check_on(self.markpen, self.shoe_box) and
            self.check_on(self.teanet, self.shoe_box) and
            self.check_on(self.cup_with_handle, self.shoe_box)
        )

        # Check if the apple is on top of the shoe_box
        apple_on_box = self.check_on(self.apple, self.shoe_box)

        # Return True if all conditions are met
        return non_edible_in_box and apple_on_box
