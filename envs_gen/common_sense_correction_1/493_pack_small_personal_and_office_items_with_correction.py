from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 493_pack_small_personal_and_office_items_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        - Add the wooden_box as a container.
        - Add the task-specific objects: dumbbell, shampoo, stapler, mouse.
        - Add distractor objects to the environment.
        """
        # Add the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the task-specific objects
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.stapler = self.add_actor("stapler", "stapler")
        self.mouse = self.add_actor("mouse", "mouse")
        
        # Add distractor objects
        distractor_list = ["chips-tub", "apple", "olive-oil", "french_fries"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the environment:
        1. Place the dumbbell into the wooden_box (wrong action).
        2. Recover by placing the dumbbell on the table.
        3. Place shampoo, stapler, and mouse into the wooden_box.
        """
        # Wrong action: place dumbbell into wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Pick dumbbell and place into wooden_box (wrong):", success)
        if not success:
            return self.info

        # Recovery action: place dumbbell on the table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Pick dumbbell from box and place on table (recovery):", success)
        if not success:
            return self.info

        # Place personal-care and office accessories into the wooden_box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Pick shampoo and place into wooden_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.stapler, self.wooden_box)
        print("Pick stapler and place into wooden_box:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Pick mouse and place into wooden_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully:
        - Shampoo, stapler, and mouse are in the wooden_box.
        - Dumbbell is NOT in the wooden_box.
        """
        # Check if required items are in the wooden_box
        shampoo_in_box = self.check_on(self.shampoo, self.wooden_box)
        stapler_in_box = self.check_on(self.stapler, self.wooden_box)
        mouse_in_box = self.check_on(self.mouse, self.wooden_box)
        
        # Check if dumbbell is NOT in the wooden_box
        dumbbell_not_in_box = not self.check_on(self.dumbbell, self.wooden_box)
        
        # Return True only if all conditions are met
        return shampoo_in_box and stapler_in_box and mouse_in_box and dumbbell_not_in_box
