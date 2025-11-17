from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 316_serve_drinks_and_snacks_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Add drinkware and fast food items
        self.mug = self.add_actor("mug", "mug")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.bottle = self.add_actor("bottle", "bottle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractor objects
        distractor_list = ["calculator", "screwdriver", "shoe", "toycar", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robotic actions to complete the task"""
        # Step 1: Pick mug and place on tray
        success = self.pick_and_place(self.mug, self.tray)
        print("Pick and place mug:", success)
        if not success:
            return self.info

        # Step 2: Pick cup_with_handle and place on tray
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Pick and place cup_with_handle:", success)
        if not success:
            return self.info

        # Step 3: Attempt to place hamburg in mug (wrong action)
        success = self.pick_and_place(self.hamburg, self.mug)
        print("Pick and place hamburg into mug:", success)
        
        # If placement failed, check if object is still grasped
        if not success:
            if self.check_grasp(self.hamburg):
                # Step 4: Recovery - place hamburg on tray
                success = self.pick_and_place(self.hamburg, self.tray)
                print("Recovery: Place hamburg on tray:", success)
                if not success:
                    return self.info
            else:
                return self.info

        # Step 5: Pick bottle and place on tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("Pick and place bottle:", success)
        if not success:
            return self.info

        # Step 6: Pick french_fries and place on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Pick and place french_fries:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all required items are on the tray"""
        return (
            self.check_on(self.mug, self.tray) and
            self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.hamburg, self.tray) and
            self.check_on(self.bottle, self.tray) and
            self.check_on(self.french_fries, self.tray)
        )
