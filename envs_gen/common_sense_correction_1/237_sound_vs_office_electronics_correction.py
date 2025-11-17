from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 237_sound_vs_office_electronics_correction(Imagine_Task):
    def load_actors(self):
        # Create containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Create target objects
        self.alarm_clock = self.add_actor("alarm-clock", "alarm_clock")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.mouse = self.add_actor("mouse", "mouse")
        self.scanner = self.add_actor("scanner", "scanner")
        
        # Add distractors
        distractor_list = ["baguette", "apple", "pot-with-plant", "red_block", "tissue-box", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place alarm clock in shoe_box
        success = self.pick_and_place(self.alarm_clock, self.shoe_box)
        print("Place alarm clock in shoe_box:", success)
        if not success:
            return self.info

        # Wrongly place small speaker in wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Wrongly place small speaker in wooden_box:", success)
        if not success:
            return self.info

        # Recovery: move small speaker to shoe_box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Recover small speaker to shoe_box:", success)
        if not success:
            return self.info

        # Place mouse in wooden_box
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Place mouse in wooden_box:", success)
        if not success:
            return self.info

        # Place scanner in wooden_box
        success = self.pick_and_place(self.scanner, self.wooden_box)
        print("Place scanner in wooden_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in correct containers
        if (self.check_on(self.alarm_clock, self.shoe_box) and
            self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.mouse, self.wooden_box) and
            self.check_on(self.scanner, self.wooden_box)):
            return True
        return False
