from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 207_store_tools_and_electronics_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        """
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.green_block = self.add_actor("green_block", "green_block")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.mouse = self.add_actor("mouse", "mouse")
        self.small_speaker = self.add_actor("small-speaker", "small-speaker")
        
        # Add distractors
        distractor_list = ['apple', 'book', 'pot-with-plant', 'tissue-box', 'baguette']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of pick-and-place actions to complete the task.
        """
        # Place heavy tools and solid toys in wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Hammer to wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.green_block, self.wooden_box)
        print("Green block to wooden_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.orange_block, self.wooden_box)
        print("Orange block to wooden_box:", success)
        if not success:
            return self.info
        
        # Place portable electronic devices in shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Mouse to shoe_box:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.small_speaker, self.shoe_box)
        print("Small speaker to shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if all objects are placed in their correct containers.
        """
        return (
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.green_block, self.wooden_box) and
            self.check_on(self.orange_block, self.wooden_box) and
            self.check_on(self.mouse, self.shoe_box) and
            self.check_on(self.small_speaker, self.shoe_box)
        )
