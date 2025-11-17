from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 472_store_electronics_and_reading_materials_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add electronic devices and reading materials
        self.alarm_clock = self.add_actor("alarm-clock", "alarm_clock")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.book = self.add_actor("book", "book")
        
        # Add distractor objects
        distractor_list = ["apple", "shoe", "dumbbell", "pot-with-plant", "baguette"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the robot's actions in sequence"""
        # Pick and place alarm clock
        success = self.pick_and_place(self.alarm_clock, self.wooden_box)
        print("Pick alarm-clock:", success)
        if not success:
            return self.info
            
        # Pick and place small speaker
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Pick small-speaker:", success)
        if not success:
            return self.info
            
        # Pick and place book
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Pick book:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if all required objects are in the wooden box"""
        return (self.check_on(self.alarm_clock, self.wooden_box) and
                self.check_on(self.small_speaker, self.wooden_box) and
                self.check_on(self.book, self.wooden_box))
