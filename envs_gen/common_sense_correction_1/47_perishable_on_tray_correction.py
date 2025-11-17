from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 47_perishable_on_tray_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: tray
        - Perishable edible items: apple, bread, hamburg
        - Non-perishable item: bottle
        - Distractors: calculator, battery, toycar, book, shoe
        """
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add perishable edible items
        self.apple = self.add_actor("apple", "apple")
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add non-perishable item
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractors to the environment
        distractor_list = ["calculator", "battery", "toycar", "book", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Pick apple and place it on tray
        2. Pick bottle and place it on tray (wrong action)
        3. Pick bottle from tray and place it back on table (recovery)
        4. Pick bread and place it on tray
        5. Pick hamburg and place it on tray
        """
        # Step 1: Pick apple and place on tray
        success = self.pick_and_place(self.apple, self.tray)
        print("Pick apple:", success)
        if not success:
            return self.info

        # Step 2: Pick bottle and place on tray (wrong action)
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick bottle (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recovery - Pick bottle from tray and place back on table
        success = self.pick_and_place(self.bottle, self.table)
        print("Recover bottle:", success)
        if not success:
            return self.info

        # Step 4: Pick bread and place on tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Pick bread:", success)
        if not success:
            return self.info

        # Step 5: Pick hamburg and place on tray
        success = self.pick_and_place(self.hamburg, self.tray)
        print("Pick hamburg:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was successfully completed by verifying:
        - Apple is on the tray
        - Bread is on the tray
        - Hamburg is on the tray
        """
        # Check if all perishable edible items are on the tray
        apple_on_tray = self.check_on(self.apple, self.tray)
        bread_on_tray = self.check_on(self.bread, self.tray)
        hamburg_on_tray = self.check_on(self.hamburg, self.tray)
        
        # Task is successful if all perishable items are on the tray
        return apple_on_tray and bread_on_tray and hamburg_on_tray
