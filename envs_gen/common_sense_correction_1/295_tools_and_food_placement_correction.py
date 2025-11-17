from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 295_tools_and_food_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Adds the wooden_box and plate as containers, and the relevant objects.
        Adds distractors to the environment.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.plate = self.add_actor("plate", "plate")

        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.bottle = self.add_actor("bottle", "bottle")

        # Add distractors
        distractor_list = ['calculator', 'shoe', 'alarm-clock', 'toycar', 'microphone']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of pick-and-place actions for the robot arm.
        Includes a wrong placement and a recovery step.
        Returns self.info if any step fails.
        """
        # Step 1: Pick hammer and place into wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Hammer to wooden_box:", success)
        if not success:
            return self.info

        # Step 2: Pick drill and place into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Drill to wooden_box:", success)
        if not success:
            return self.info

        # Step 3: Wrong action - Pick bottle and place into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Bottle to wooden_box (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recovery - Pick bottle from wooden_box and place onto plate
        success = self.pick_and_place(self.bottle, self.plate)
        print("Bottle to plate (recovery):", success)
        if not success:
            return self.info

        # Step 5: Pick french_fries and place onto plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("French fries to plate:", success)
        if not success:
            return self.info

        # Step 6: Pick cup_with_handle and place onto plate
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Cup with handle to plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed.
        Verifies that:
        - Tools (hammer, drill) are in the wooden_box.
        - Edible items (french_fries) and drinkware (cup_with_handle, bottle) are on the plate.
        """
        if (
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.cup_with_handle, self.plate) and
            self.check_on(self.bottle, self.plate)
        ):
            return True
        return False
