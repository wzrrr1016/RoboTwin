from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 372_store_blocks_no_electronics_correction(Imagine_Task):
    def load_actors(self):
        # Add the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add the colorful toy blocks
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        
        # Add the electronic devices
        self.microphone = self.add_actor("microphone", "microphone")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm_clock")
        
        # Add distractor objects
        distractor_list = ['apple', 'baguette', 'jam-jar', 'pot-with-plant', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Step 1: Place blue block into shoe box
        success = self.pick_and_place(self.blue_block, self.shoe_box)
        print("Place blue_block:", success)
        if not success:
            return self.info

        # Step 2: Wrongly place alarm clock into shoe box
        success = self.pick_and_place(self.alarm_clock, self.shoe_box)
        print("Wrongly place alarm-clock:", success)
        if not success:
            return self.info

        # Step 3: Recovery - place alarm clock on shoe box (not inside)
        success = self.pick_and_place(self.alarm_clock, self.shoe_box)
        print("Recover alarm-clock:", success)
        if not success:
            return self.info

        # Step 4: Place purple block into shoe box
        success = self.pick_and_place(self.purple_block, self.shoe_box)
        print("Place purple_block:", success)
        if not success:
            return self.info

        # Step 5: Place microphone on shoe box (not inside)
        success = self.pick_and_place(self.microphone, self.shoe_box)
        print("Place microphone:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if both blocks are in the shoe box
        blocks_in_box = (self.check_on(self.blue_block, self.shoe_box) and 
                        self.check_on(self.purple_block, self.shoe_box))
        
        # Check if electronic devices are on the shoe box (not inside)
        electronics_on_box = (self.check_on(self.alarm_clock, self.shoe_box) and 
                             self.check_on(self.microphone, self.shoe_box))
        
        return blocks_in_box and electronics_on_box
