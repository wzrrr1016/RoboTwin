from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 18_sound_related_item_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.microphone = self.add_actor("microphone", "microphone")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ["table-tennis", "roll-paper", "pot-with-plant", "dumbbell", "book"]
        self.add_distractors(distractor_list)
        
        # Check scene setup
        self.check_scene()

    def play_once(self):
        # Place sound-producing items in shoe_box
        success = self.pick_and_place(self.microphone, self.shoe_box)
        print("Microphone placed:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.alarm_clock, self.shoe_box)
        print("Alarm clock placed:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Small speaker placed:", success)
        if not success:
            return self.info
            
        # Wrong placement of sand-clock (then recovery)
        success = self.pick_and_place(self.sand_clock, self.shoe_box)
        print("Sand clock wrong placement:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Sand clock recovery:", success)
        if not success:
            return self.info
            
        # Place non-sound item in fluted_block
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Fork placed:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all sound items are in shoe_box
        sound_items_correct = (
            self.check_on(self.microphone, self.shoe_box) and
            self.check_on(self.alarm_clock, self.shoe_box) and
            self.check_on(self.small_speaker, self.shoe_box)
        )
        
        # Verify all non-sound items are in fluted_block
        non_sound_items_correct = (
            self.check_on(self.sand_clock, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block)
        )
        
        return sound_items_correct and non_sound_items_correct
