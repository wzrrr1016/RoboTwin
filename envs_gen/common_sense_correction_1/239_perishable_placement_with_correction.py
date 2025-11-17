from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 239_perishable_placement_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes the tray, perishable edible items, and non-edible items.
        Adds distractor objects to the environment.
        """
        # Add the tray as a container
        self.tray = self.add_actor("tray", "tray")
        
        # Add perishable edible items
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        
        # Add non-perishable items that need to be handled
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        
        # Add distractor objects to the environment
        distractors = ["screwdriver", "toycar", "alarm-clock", "book", "dumbbell"]
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the robot's actions in the simulation environment.
        The robot will:
        1. Pick and place apple on the tray
        2. Pick and place bread on the tray
        3. (Mistakenly) pick and place shampoo on the tray
        4. Recover by picking shampoo from tray and placing it on the table
        5. Pick and place cup_with_handle on the table
        """
        # Step 1: Pick apple and place on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple:", success)
        if not success:
            return self.info

        # Step 2: Pick bread and place on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread:", success)
        if not success:
            return self.info

        # Step 3: (Mistakenly) pick shampoo and place on tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover by picking shampoo from tray and placing on table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Recover shampoo:", success)
        if not success:
            return self.info

        # Step 5: Pick cup_with_handle and place on table
        success = self.pick_and_place(self.cup_with_handle, self.table)
        print("Pick cup_with_handle:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task was successfully completed.
        Success criteria:
        - Apple and bread are on the tray
        - Shampoo and cup_with_handle are not on the tray
        """
        # Check if apple and bread are on the tray
        apple_on_tray = self.check_on(self.apple, self.tray)
        bread_on_tray = self.check_on(self.bread, self.tray)
        
        # Check if shampoo and cup_with_handle are not on the tray
        shampoo_not_on_tray = not self.check_on(self.shampoo, self.tray)
        cup_not_on_tray = not self.check_on(self.cup_with_handle, self.tray)
        
        # Return True if all conditions are met
        return all([apple_on_tray, bread_on_tray, shampoo_not_on_tray, cup_not_on_tray])
