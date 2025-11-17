from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 245_serve_drinks_and_snack_with_heavy_item_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Tray as the container
        - Drinkware (cup_with_handle, cup_without_handle)
        - Ready-to-eat snack (french_fries)
        - Heavy exercise equipment (dumbbell)
        - Distractors as specified in the task
        """
        # Create the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Create drinkware and snack objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Create heavy exercise equipment
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        
        # Add distractors to the environment
        distractor_list = ['calculator', 'toycar', 'pot-with-plant', 'stapler', 'shoe']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of robot actions:
        1. Wrongly place dumbbell on tray
        2. Recover by placing dumbbell back on table
        3. Place drinkware and ready-to-eat snack on tray
        """
        # Wrong action: place dumbbell on tray
        success = self.pick_and_place(self.dumbbell, self.tray)
        print("Pick and place dumbbell (wrong):", success)
        if not success:
            return self.info

        # Recovery: place dumbbell back on table
        success = self.pick_and_place(self.dumbbell, self.table)
        print("Recover dumbbell to table:", success)
        if not success:
            return self.info

        # Place drinkware on tray
        success = self.pick_and_place(self.cup_with_handle, self.tray)
        print("Place cup with handle:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_without_handle, self.tray)
        print("Place cup without handle:", success)
        if not success:
            return self.info

        # Place ready-to-eat snack on tray
        success = self.pick_and_place(self.french_fries, self.tray)
        print("Place french fries:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Drinkware (both cups) and ready-to-eat snack (fries) are on the tray
        - Heavy exercise equipment (dumbbell) is NOT on the tray
        """
        if (self.check_on(self.cup_with_handle, self.tray) and
            self.check_on(self.cup_without_handle, self.tray) and
            self.check_on(self.french_fries, self.tray) and
            not self.check_on(self.dumbbell, self.tray)):
            return True
        return False
