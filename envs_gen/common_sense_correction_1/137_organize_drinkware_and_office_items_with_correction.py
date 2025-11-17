from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 137_organize_drinkware_and_office_items_with_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the simulation environment"""
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.stapler = self.add_actor("stapler", "stapler")
        self.mouse = self.add_actor("mouse", "mouse")
        
        # Add distractors
        distractor_list = ['toycar', 'shoe', 'pot-with-plant', 'baguette', 'dumbbell']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of robot actions for the task"""
        # Initial wrong placement of stapler
        success = self.pick_and_place(self.stapler, self.plate)
        print("Pick stapler and place onto plate (wrong):", success)
        if not success:
            return self.info

        # Recovery action - move stapler to correct container
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Pick stapler from plate and place into fluted_block (recovery):", success)
        if not success:
            return self.info

        # Place drinkware items on plate
        success = self.pick_and_place(self.mug, self.plate)
        print("Pick mug and place onto plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_without_handle, self.plate)
        print("Pick cup_without_handle and place onto plate:", success)
        if not success:
            return self.info

        # Place office-related item in fluted_block
        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("Pick mouse and place into fluted_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if all drinkware items are on the plate
        drinkware_on_plate = (
            self.check_on(self.mug, self.plate) and 
            self.check_on(self.cup_without_handle, self.plate)
        )
        
        # Check if office items are in fluted_block
        office_in_fluted = (
            self.check_on(self.stapler, self.fluted_block) and 
            self.check_on(self.mouse, self.fluted_block)
        )
        
        return drinkware_on_plate and office_in_fluted
