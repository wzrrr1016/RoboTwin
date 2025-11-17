from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 288_handheld_foods_and_utensil_on_plate_with_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add the plate container
        self.plate = self.add_actor("plate", "plate")
        
        # Add required objects
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.french_fries = self.add_actor("french_fries", "french_fries")
        self.bread = self.add_actor("bread", "bread")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ['calculator', 'screwdriver', 'toycar', 'alarm-clock', 'pot-with-plant']
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of pick-and-place actions"""
        # Initial wrong action - place cup_with_handle on plate
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Wrong placement of cup_with_handle:", success)
        if not success:
            return self.info

        # Recovery action - move cup_with_handle back to table
        success = self.pick_and_place(self.cup_with_handle, self.table)
        print("Recovering cup_with_handle to table:", success)
        if not success:
            return self.info

        # Place hamburg on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Placing hamburg:", success)
        if not success:
            return self.info

        # Place french_fries on plate
        success = self.pick_and_place(self.french_fries, self.plate)
        print("Placing french_fries:", success)
        if not success:
            return self.info

        # Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Placing bread:", success)
        if not success:
            return self.info

        # Place fork on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Placing fork:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check that cup_with_handle is NOT on the plate
        if self.check_on(self.cup_with_handle, self.plate):
            return False
            
        # Check that all required items are on the plate
        return (
            self.check_on(self.hamburg, self.plate) and
            self.check_on(self.french_fries, self.plate) and
            self.check_on(self.bread, self.plate) and
            self.check_on(self.fork, self.plate)
        )
