from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 188_electronics_and_decor_storage_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the simulation environment.
        Adds the shoe box as a container and the relevant objects.
        Adds distractor objects to the environment.
        """
        # Add the shoe box container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add the target objects
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        self.mouse = self.add_actor("mouse", "mouse")
        self.sand_clock = self.add_actor("sand-clock", "sand-clock")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractor objects
        distractor_list = ["dumbbell", "baguette", "book", "bottle"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm to complete the task.
        The sequence includes:
        1. Place small-speaker into shoe_box
        2. Place hammer into shoe_box (wrong action)
        3. Place hammer onto shoe_box (recovery action)
        4. Place mouse into shoe_box
        5. Place sand-clock into shoe_box
        """
        # Place small-speaker into shoe_box
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Pick small-speaker:", success)
        if not success:
            return self.info

        # Place hammer into shoe_box (wrong action)
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Pick hammer (wrong):", success)
        if not success:
            return self.info

        # Place hammer onto shoe_box (recovery action)
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Recover hammer:", success)
        if not success:
            return self.info

        # Place mouse into shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Pick mouse:", success)
        if not success:
            return self.info

        # Place sand-clock into shoe_box
        success = self.pick_and_place(self.sand_clock, self.shoe_box)
        print("Pick sand-clock:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully.
        The task is considered successful if:
        - small-speaker is in the shoe_box
        - mouse is in the shoe_box
        - sand-clock is in the shoe_box
        """
        # Check if all required objects are in the shoe_box
        if (self.check_on(self.small_speaker, self.shoe_box) and
            self.check_on(self.mouse, self.shoe_box) and
            self.check_on(self.sand_clock, self.shoe_box)):
            return True
        return False
