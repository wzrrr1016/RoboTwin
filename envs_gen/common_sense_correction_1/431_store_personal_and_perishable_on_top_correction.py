from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 431_store_personal_and_perishable_on_top_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        Adds the wooden_box container and the relevant objects (shampoo, mouse, apple, hamburg).
        Adds distractor objects to the environment.
        """
        # Create the wooden box container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Create the main objects for the task
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.mouse = self.add_actor("mouse", "mouse")
        self.apple = self.add_actor("apple", "apple")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        
        # Add distractor objects to the environment
        distractor_list = ["dumbbell", "shoe", "book", "pot-with-plant", "sand-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions to complete the task:
        1. Place shampoo and mouse into the wooden_box
        2. Place apple and hamburg on top of the wooden_box
        Returns early if any action fails.
        """
        # Place shampoo into the wooden box
        success = self.pick_and_place(self.shampoo, self.wooden_box)
        print("Shampoo placed:", success)
        if not success:
            return self.info
            
        # Place mouse into the wooden box
        success = self.pick_and_place(self.mouse, self.wooden_box)
        print("Mouse placed:", success)
        if not success:
            return self.info
            
        # Place apple on top of the wooden box
        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Apple placed:", success)
        if not success:
            return self.info
            
        # Place hamburg on top of the wooden box
        success = self.pick_and_place(self.hamburg, self.wooden_box)
        print("Hamburg placed:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully by checking:
        - Shampoo and mouse are in the wooden_box
        - Apple and hamburg are on top of the wooden_box
        Returns True if all conditions are met, False otherwise.
        """
        # Check if all required objects are on the wooden box
        if (self.check_on(self.shampoo, self.wooden_box) and
            self.check_on(self.mouse, self.wooden_box) and
            self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.hamburg, self.wooden_box)):
            return True
        return False
