from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 267_drinkware_and_heavy_tools_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: plate and coaster
        - Objects: cup_without_handle, shampoo, dumbbell, hammer
        - Distractors: toycar, book, tissue-box, shoe, red_block
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.hammer = self.add_actor("hammer", "hammer")

        # Add distractors
        distractor_list = ['toycar', 'book', 'tissue-box', 'shoe', 'red_block']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - Place cup_without_handle on coaster
        - Place shampoo on plate (wrong action)
        - Recover shampoo and place it on coaster
        - Place hammer and dumbbell on plate
        """
        # Step 1: Place cup_without_handle on coaster
        success = self.pick_and_place(self.cup_without_handle, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        # Step 2: Place shampoo on plate (wrong action)
        success = self.pick_and_place(self.shampoo, self.plate)
        print("Place shampoo on plate (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover shampoo and place it on coaster
        success = self.pick_and_place(self.shampoo, self.coaster)
        print("Recover shampoo to coaster:", success)
        if not success:
            return self.info

        # Step 4: Place hammer on plate
        success = self.pick_and_place(self.hammer, self.plate)
        print("Place hammer on plate:", success)
        if not success:
            return self.info

        # Step 5: Place dumbbell on plate
        success = self.pick_and_place(self.dumbbell, self.plate)
        print("Place dumbbell on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed.
        - Drinkware and liquid containers (cup_without_handle, shampoo) should be on the coaster
        - Heavy tools (hammer, dumbbell) should be on the plate
        """
        if (self.check_on(self.cup_without_handle, self.coaster) and
            self.check_on(self.shampoo, self.coaster) and
            self.check_on(self.hammer, self.plate) and
            self.check_on(self.dumbbell, self.plate)):
            return True
        return False
