from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 403_food_and_play_separation_with_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Containers: plate and tray
        Objects: hamburg (edible), fork (tableware), cup_with_handle (tableware), 
                 toycar (toy), pink_block (play block)
        Distractors: calculator, screwdriver, pot-with-plant, shoe, book
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.tray = self.add_actor("tray", "tray")
        
        # Add objects
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.fork = self.add_actor("fork", "fork")
        self.cup_with_handle = self.add_actor("cup_with_handle", "cup_with_handle")
        self.toycar = self.add_actor("toycar", "toycar")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        
        # Add distractors
        distractors = ['calculator', 'screwdriver', 'pot-with-plant', 'shoe', 'book']
        self.add_distractors(distractors)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task:
        - Place edible items and eating-related tableware on the plate
        - Place toys and play blocks on the tray
        """
        # Place edible item on plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Place hamburg on plate:", success)
        if not success:
            return self.info

        # Place eating-related tableware on plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Place fork on plate:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.cup_with_handle, self.plate)
        print("Place cup_with_handle on plate:", success)
        if not success:
            return self.info

        # Place toys and play blocks on tray
        success = self.pick_and_place(self.toycar, self.tray)
        print("Place toycar on tray:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.pink_block, self.tray)
        print("Place pink_block on tray:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in their correct containers:
        - hamburg, fork, and cup_with_handle on plate
        - toycar and pink_block on tray
        """
        return (
            self.check_on(self.hamburg, self.plate) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.cup_with_handle, self.plate) and
            self.check_on(self.toycar, self.tray) and
            self.check_on(self.pink_block, self.tray)
        )
