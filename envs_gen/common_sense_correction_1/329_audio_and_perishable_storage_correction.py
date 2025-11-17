from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 329_audio_and_perishable_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        """
        # Create the shoe_box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create audio devices
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.microphone = self.add_actor("microphone", "microphone")
        
        # Create perishable foods
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.apple = self.add_actor("apple", "apple")
        
        # Add distractor objects to the environment
        distractor_list = ["screwdriver", "hammer", "dumbbell", "book", "toycar"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm to complete the task.
        """
        # Step 1: Place small-speaker into shoe_box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Place small-speaker into shoe_box:", success)
        if not success:
            return self.info

        # Step 2: Place french_fries into shoe_box (wrong action)
        success = self.pick_and_place(self.french_fries, self.shoe_box)
        print("Place french_fries into shoe_box (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recover by placing french_fries on shoe_box
        success = self.pick_and_place(self.french_fries, self.shoe_box)
        print("Place french_fries on shoe_box (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place microphone into shoe_box
        success = self.pick_and_place(self.microphone, self.shoe_box)
        print("Place microphone into shoe_box:", success)
        if not success:
            return self.info

        # Step 5: Place apple on shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Place apple on shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking object placements.
        """
        # Check if audio devices are in the shoe_box
        audio_devices_in = (
            self.check_on(self.small_speaker, self.shoe_box) and 
            self.check_on(self.microphone, self.shoe_box)
        )
        
        # Check if perishable foods are on the shoe_box
        perishables_on = (
            self.check_on(self.french_fries, self.shoe_box) and 
            self.check_on(self.apple, self.shoe_box)
        )
        
        # Return True if all conditions are met
        return audio_devices_in and perishables_on
