from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 82_place_perishables_and_drinkware_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.coaster = self.add_actor("coaster", "coaster")
        
        # Add required objects
        self.bread = self.add_actor("bread", "bread")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractors = ["calculator", "hammer", "toycar", "alarm-clock", "book"]
        self.add_distractors(distractors)

    def play_once(self):
        """Execute the sequence of pick-and-place actions"""
        # 1. Place bread on plate
        success = self.pick_and_place(self.bread, self.plate)
        print("Place bread on plate:", success)
        if not success:
            return self.info

        # 2. Place hamburg on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg on plate:", success)
        if not success:
            return self.info

        # 3. Place cup_with_handle on plate (wrong placement)
        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Place cup_with_handle on plate (wrong):", success)
        if not success:
            return self.info

        # 4. Correct placement - move cup_with_handle to coaster
        success = self.pick_and_place(self.cup_with_handle, self.coaster)
        print("Place cup_with_handle on coaster:", success)
        if not success:
            return self.info

        # 5. Place fork on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Place fork on plate:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all objects are in their correct final positions"""
        return (
            self.check_on(self.bread, self.plate) and
            self.check_on(self.hamburg, self.plate) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.cup_with_handle, self.coaster)
        )
