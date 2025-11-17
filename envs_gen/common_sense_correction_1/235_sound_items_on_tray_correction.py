from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 235_sound_items_on_tray_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Create the tray container
        self.tray = self.add_actor("tray", "tray")
        
        # Create objects that produce sound (bell, alarm-clock)
        self.bell = self.add_actor("bell", "bell")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        
        # Create other objects (shampoo, french_fries)
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        
        # Add distractor objects
        distractor_list = ['calculator', 'pot-with-plant', 'screwdriver', 'tissue-box', 'mug']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions in sequence"""
        # 1. Pick bell and place it onto tray
        success = self.pick_and_place(self.bell, self.tray)
        print("Pick bell and place on tray:", success)
        if not success:
            return self.info

        # 2. Pick shampoo and place it onto tray (wrong action)
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo and place on tray (wrong):", success)
        if not success:
            return self.info

        # 3. Pick shampoo from tray and place it on table (recovery)
        success = self.pick_and_place(self.shampoo, self.table)
        print("Recover shampoo to table:", success)
        if not success:
            return self.info

        # 4. Pick alarm-clock and place it onto tray
        success = self.pick_and_place(self.alarm_clock, self.tray)
        print("Pick alarm-clock and place on tray:", success)
        if not success:
            return self.info

        return self.info  # All actions completed successfully

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if bell and alarm-clock are on the tray
        bell_on_tray = self.check_on(self.bell, self.tray)
        alarm_clock_on_tray = self.check_on(self.alarm_clock, self.tray)
        
        # Check if shampoo is NOT on the tray (it should be on the table)
        shampoo_on_tray = self.check_on(self.shampoo, self.tray)
        
        # Task is successful if both sound-producing items are on tray 
        # and shampoo is not on tray
        if bell_on_tray and alarm_clock_on_tray and not shampoo_on_tray:
            return True
        return False
