from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 192_place_food_and_nonfood_with_recovery(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Add objects used for eating/drinking and other categorized items
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.mug = self.add_actor("mug", "mug")
        self.knife = self.add_actor("knife", "knife")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "book", "shoe", "alarm-clock", "pot-with-plant"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions to complete the task.
        Includes a wrong action and recovery step as specified.
        """
        # Step 1: Place french fries on plate (eating item)
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Place french fries on plate:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place mug on tray (incorrect action)
        success = self.pick_and_place(self.mug, self.tray)
        print("Wrongly place mug on tray:", success)
        if not success:
            return self.info

        # Step 3: Recovery - move mug from tray to plate (correcting the error)
        success = self.pick_and_place(self.mug, self.plate)
        print("Recover mug to plate:", success)
        if not success:
            return self.info

        # Step 4: Place knife on tray (sharp tool)
        success = self.pick_and_place(self.knife, self.tray)
        print("Place knife on tray:", success)
        if not success:
            return self.info

        # Step 5: Place shampoo on tray (personal care item)
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Place shampoo on tray:", success)
        if not success:
            return self.info

        # Step 6: Place toycar on tray (toy)
        success = self.pick_and_place(self.toycar, self.tray)
        print("Place toycar on tray:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if all objects are placed in their correct containers.
        """
        # Check if eating/drinking items are on the plate
        eating_drinking_correct = (
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.mug, self.plate)
        )
        
        # Check if personal care items, toys, and sharp tools are on the tray
        safe_organization_correct = (
            self.check_on(self.knife, self.tray) and
            self.check_on(self.shampoo, self.tray) and
            self.check_on(self.toycar, self.tray)
        )
        
        # Return True only if all conditions are satisfied
        return eating_drinking_correct and safe_organization_correct
