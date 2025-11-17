from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 59_organize_drink_and_decor_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment."""
        # Create the organizer container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Create the main objects for the task
        self.fork = self.add_actor("fork", "fork")
        self.mug = self.add_actor("mug", "mug")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.teanet = self.add_actor("teanet", "teanet")
        
        # Add distractor objects
        distractor_list = ["calculator", "pet-collar", "toycar", "dumbbell", "book"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions for the task."""
        # Place small utensils and drink accessories inside the organizer
        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Pick place fork:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.mug, self.fluted_block)
        print("Pick place mug:", success)
        if not success:
            return self.info
            
        # Wrong placement of delicate decorative piece
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Pick place sand-clock (wrong):", success)
        if not success:
            return self.info
            
        # Recovery: place delicate decorative piece on top of the organizer
        success = self.pick_and_place(self.sand_clock, self.fluted_block)
        print("Pick place sand-clock (recovery):", success)
        if not success:
            return self.info
            
        # Place remaining drink accessory
        success = self.pick_and_place(self.teanet, self.fluted_block)
        print("Pick place teanet:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if all task requirements are successfully completed."""
        # Check if all utensils and accessories are in the organizer
        # and the delicate decorative piece is on top
        return (
            self.check_on(self.fork, self.fluted_block) and
            self.check_on(self.mug, self.fluted_block) and
            self.check_on(self.teanet, self.fluted_block) and
            self.check_on(self.sand_clock, self.fluted_block)
        )
