from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 350_store_sound_devices_and_place_hygiene_on_top_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        Includes containers, target objects, and distractors.
        """
        # Add the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add target objects
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects
        distractor_list = ['apple', 'hammer', 'pot-with-plant', 'red_block', 'baguette']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place sound-making devices in the shoe box
        2. Place hygiene/paper items on the shoe box
        """
        # Step 1: Place small speaker in shoe box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Place small speaker:", success)
        if not success:
            return self.info

        # Step 2: Place alarm clock in shoe box
        success = self.pick_and_place(self.alarm_clock, self.shoe_box)
        print("Place alarm clock:", success)
        if not success:
            return self.info

        # Step 3: Place shampoo in shoe box (wrong action)
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Place shampoo (wrong):", success)
        if not success:
            return self.info

        # Step 4: Recover by placing shampoo on shoe box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Recover shampoo placement:", success)
        if not success:
            return self.info

        # Step 5: Place tissue box on shoe box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("Place tissue box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Sound-making devices in shoe box
        - Hygiene/paper items on shoe box
        """
        # Check if all required objects are properly placed
        if (self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.alarm_clock, self.shoe_box) and
            self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.tissue_box, self.shoe_box)):
            return True
        return False
