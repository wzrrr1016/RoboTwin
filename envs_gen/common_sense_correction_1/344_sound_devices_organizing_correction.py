from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 344_sound_devices_organizing_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add sound-related objects
        self.bell = self.add_actor("bell", "bell")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.microphone = self.add_actor("microphone", "microphone")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        
        # Add distractors
        distractor_list = ["apple", "book", "pot-with-plant", "shoe", "tissue-box"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Correct placement: Bell
        success = self.pick_and_place(self.bell, self.fluted_block)
        print("Pick bell:", success)
        if not success:
            return self.info
            
        # Wrong placement: Screwdriver
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Pick screwdriver (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: Move screwdriver back to table
        success = self.pick_and_place(self.screwdriver, self.table)
        print("Recover screwdriver:", success)
        if not success:
            return self.info
            
        # Correct placements: Small speaker and microphone
        success = self.pick_and_place(self.small_speaker, self.fluted_block)
        print("Pick small speaker:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.microphone, self.fluted_block)
        print("Pick microphone:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all sound-related devices are on the organizer
        return (
            self.check_on(self.bell, self.fluted_block) and
            self.check_on(self.small_speaker, self.fluted_block) and
            self.check_on(self.microphone, self.fluted_block)
        )
