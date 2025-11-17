from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 202_organize_drinkware_and_perishable_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: fluted_block
        - Objects: mug, cup, apple, alarm-clock
        - Distractors: shoe, book, dumbbell, toycar, hammer
        """
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.mug = self.add_actor("mug", "mug")
        self.cup = self.add_actor("cup", "cup")
        self.apple = self.add_actor("apple", "apple")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm_clock")
        
        # Add distractors as specified in the task
        distractor_list = ['shoe', 'book', 'dumbbell', 'toycar', 'hammer']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the simulation:
        1. Wrongly place alarm-clock into fluted_block
        2. Recover by placing alarm-clock back on the table
        3. Place drinkware (mug, cup) and perishable food (apple) into fluted_block
        """
        # Step 1: Wrong placement of alarm-clock into fluted_block
        success = self.pick_and_place(self.alarm_clock, self.fluted_block)
        print("Wrong placement alarm-clock into fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Recovery - Place alarm-clock back on the table
        success = self.pick_and_place(self.alarm_clock, self.table)
        print("Recovery: alarm-clock to table:", success)
        if not success:
            return self.info

        # Step 3: Place drinkware and perishable food into fluted_block
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Place mug into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup, self.fluted_block)
        print("Place cup into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.fluted_block)
        print("Place apple into fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Drinkware (mug, cup) and perishable food (apple) are in fluted_block
        - Electronic device (alarm-clock) is NOT in fluted_block
        """
        # Check if all required items are in the organizer
        in_organizer = (
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.cup, self.fluted_block) and
            self.check_on(self.apple, self.fluted_block)
        )
        
        # Check if electronic device is NOT in the organizer
        no_electronics = not self.check_on(self.alarm_clock, self.fluted_block)
        
        return in_organizer and no_electronics
