from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 81_store_heavy_keep_delicate_out_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Creates the wooden box container and the objects to be manipulated.
        Adds distractor objects to the environment.
        """
        # Create the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add the required objects
        self.drill = self.add_actor("drill", "drill")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.mug = self.add_actor("mug", "mug")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        
        # Add distractor objects
        distractor_list = ["red_block", "green_block", "blue_block", "toycar", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation.
        1. Place drill into wooden_box
        2. Place mug into wooden_box (wrong action)
        3. Recover by placing mug on wooden_box
        4. Place dumbbell into wooden_box
        5. Place pot-with-plant on wooden_box
        """
        # Place drill into wooden_box
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill:", success)
        if not success:
            return self.info

        # Wrongly place mug into wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Wrongly place mug:", success)
        if not success:
            return self.info

        # Recovery: pick mug and place on wooden_box
        success = self.pick_and_place(self.mug, self.wooden_box)
        print("Recover mug:", success)
        if not success:
            return self.info

        # Place dumbbell into wooden_box
        success = self.pick_and_place(self.dumbbell, self.wooden_box)
        print("Place dumbbell:", success)
        if not success:
            return self.info

        # Place pot-with-plant on wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Place pot:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        Checks if:
        - Drill and dumbbell are in the wooden_box
        - Mug and pot-with-plant are on the wooden_box (not inside)
        """
        # Check if sturdy items are in the box
        sturdy_items_in_box = (
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.dumbbell, self.wooden_box)
        )
        
        # Check if fragile/living items are on the box (not inside)
        fragile_items_on_box = (
            self.check_on(self.mug, self.wooden_box) and
            self.check_on(self.pot_with_plant, self.wooden_box)
        )
        
        return sturdy_items_in_box and fragile_items_on_box
