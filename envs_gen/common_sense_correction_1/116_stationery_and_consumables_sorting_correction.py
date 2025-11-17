from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 116_stationery_and_consumables_sorting_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        Containers are added as actors to be used as placement targets.
        Objects are added for manipulation by the robot.
        Distractors are added to simulate irrelevant items in the scene.
        """
        # Add containers to the environment
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")

        # Add objects to the environment
        self.bread = self.add_actor("bread", "bread")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.markpen = self.add_actor("markpen", "markpen")

        # Add distractors to the environment
        distractor_list = ['pet-collar', 'table-tennis', 'toycar', 'dumbbell', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot to complete the task:
        1. Place the markpen on the fluted_block (writing tool).
        2. Place the cup_with_handle on the fluted_block (wrong placement).
        3. Correct the mistake by placing the cup_with_handle into the wooden_box (drinkware).
        4. Place the bread and french_fries into the wooden_box (edible items).
        """
        # Step 1: Place markpen on fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Place markpen on fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place cup_with_handle on fluted_block (wrong placement)
        success = self.pick_and_place(self.cup_with_handle, self.fluted_block)
        print("Place cup_with_handle on fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 3: Correct the mistake by placing cup_with_handle into wooden_box
        success = self.pick_and_place(self.cup_with_handle, self.wooden_box)
        print("Recover cup_with_handle to wooden_box:", success)
        if not success:
            return self.info

        # Step 4: Place bread into wooden_box
        success = self.pick_and_place(self.bread, self.wooden_box)
        print("Place bread into wooden_box:", success)
        if not success:
            return self.info

        # Step 5: Place french_fries into wooden_box
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("Place french_fries into wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking the final positions of all relevant objects.
        Returns True if all objects are in their correct target containers, False otherwise.
        """
        return (
            self.check_on(self.markpen, self.fluted_block) and
            self.check_on(self.cup_with_handle, self.wooden_box) and
            self.check_on(self.bread, self.wooden_box) and
            self.check_on(self.french_fries, self.wooden_box)
        )
