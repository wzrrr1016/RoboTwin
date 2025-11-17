from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 40_electronic_non_electronic_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add target objects
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.alarm_clock = self.add_actor("alarm-clock", "alarm-clock")
        self.microphone = self.add_actor("microphone", "microphone")
        self.bell = self.add_actor("bell", "bell")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractors
        distractor_list = ["red_block", "green_block", "blue_block", "yellow_block", "purple_block"]
        self.add_distractors(distractor_list)
        
        # Check scene setup
        self.check_scene()

    def play_once(self):
        # Place electronic items in fluted_block
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Place small-speaker:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.alarm_clock, self.fluted_block)
        print("Place alarm-clock:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("Place microphone:", success)
        if not success:
            return self.info
            
        # Wrong placement of bell (needs recovery)
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Wrong placement of bell:", success)
        if not success:
            return self.info
            
        # Recovery - move bell to correct container
        success = self.pick_and_place(self.bell, self.plate)
        print("Recover bell:", success)
        if not success:
            return self.info
            
        # Place non-electronic bread in plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Place bread:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all items are in correct containers
        return (self.check_on(self.small_speaker, self.fluted_block) and
                self.check_on(self.alarm_clock, self.fluted_block) and
                self.check_on(self.microphone, self.fluted_block) and
                self.check_on(self.bell, self.plate) and
                self.check_on(self.bread, self.plate))
