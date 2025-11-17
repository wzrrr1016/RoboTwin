from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 43_store_fragile_and_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the simulation environment.
        """
        # Add the wooden_box as a container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the required objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bottle = self.add_actor("bottle", "bottle")
        self.drill = self.add_actor("drill", "drill")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "toycar", "book", "shoe", "red_block"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        """
        # Step 1: Place mug into the wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Place mug:", success)
        if not success:
            return self.info

        # Step 2: Place cup_with_handle into the wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("Place cup_with_handle:", success)
        if not success:
            return self.info

        # Step 3: Place bottle into the wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Place bottle:", success)
        if not success:
            return self.info

        # Step 4: Wrong action - Place drill into the wooden_box (inside)
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Wrong place drill:", success)
        if not success:
            return self.info

        # Step 5: Recovery - Pick drill from wooden_box and place it on top of the wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Recover drill placement:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        - Drinkware (mug, cup_with_handle, bottle) are safely inside the wooden_box.
        - Drill is placed on top of the wooden_box.
        """
        # Check if drinkware are inside the wooden_box
        drinkware_in_box = (
            self.check_on(self.mug, self.wooden_box) and
            self.check_on(self.cup_with_handle, self.wooden_box) and
            self.check_on(self.bottle, self.wooden_box)
        )
        
        # Check if the drill is on top of the wooden_box
        drill_on_box = self.check_on(self.drill, self.wooden_box)
        
        # Return True only if all conditions are met
        return drinkware_in_box and drill_on_box
