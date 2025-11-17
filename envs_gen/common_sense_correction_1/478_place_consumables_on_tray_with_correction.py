from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 478_place_consumables_on_tray_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors into the simulation environment.
        - Tray is the target container.
        - Apple, can, and bottle are the edible/drinking items to be placed on the tray.
        - Sand-clock is a distractor object that should not be placed on the tray.
        - Additional distractors are added to the environment.
        """
        # Add the tray as the target container
        self.tray = self.add_actor("tray", "tray")
        
        # Add edible and drink container objects
        self.apple = self.add_actor("apple", "apple")
        self.can = self.add_actor("can", "can")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add a distractor object that should not be placed on the tray
        self.sand_clock = self.add_actor("sand-clock", "sand_clock")
        
        # Add other distractors to the environment
        distractor_list = ['calculator', 'toycar', 'dumbbell', 'book', 'pot-with-plant']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm.
        - First, the robot mistakenly places the sand-clock on the tray.
        - Then, it recovers by picking the sand-clock from the tray and placing it on the table.
        - Finally, it places the edible and drink container objects on the tray.
        """
        # Mistaken action: place sand-clock on the tray
        success = self.pick_and_place(self.sand_clock, self.tray)
        print("pick place sand-clock (wrong):", success)
        if not success:
            return self.info

        # Recovery action: pick sand-clock from tray and place it on the table
        success = self.pick_and_place(self.sand_clock, self.table)
        print("recovery sand-clock:", success)
        if not success:
            return self.info

        # Place edible and drink container objects on the tray
        success = self.pick_and_place(self.apple, self.tray)
        print("pick place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.tray)
        print("pick place can:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.bottle, self.tray)
        print("pick place bottle:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task was completed successfully.
        - All edible and drink container objects (apple, can, bottle) must be on the tray.
        - The sand-clock must not be on the tray.
        """
        if (self.check_on(self.apple, self.tray) and
            self.check_on(self.can, self.tray) and
            self.check_on(self.bottle, self.tray) and
            not self.check_on(self.sand_clock, self.tray)):
            return True
        return False
