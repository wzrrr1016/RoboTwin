from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 265_store_reusable_vs_disposable_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors (objects and containers) into the environment.
        Containers: dustbin, shoe_box
        Objects: mouse, scanner, tissue-box, shampoo
        Distractors: apple, baguette, bread, hamburg, french_fries
        """
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.mouse = self.add_actor("mouse", "mouse")
        self.scanner = self.add_actor("scanner", "scanner")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractors
        distractor_list = ["apple", "baguette", "bread", "hamburg", "french_fries"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions to complete the task:
        1. Put durable reusable items in shoe_box
        2. Put single-use disposable items in dustbin
        3. Correct any misplacements
        """
        # Place mouse (electronic) in shoe_box
        success = self.pick_and_place(self.mouse, self.shoe_box)
        print("Pick mouse to shoe_box:", success)
        if not success:
            return self.info

        # Place tissue-box (disposable hygiene) in dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Pick tissue-box to dustbin:", success)
        if not success:
            return self.info

        # Wrong placement: scanner (electronic) in dustbin
        success = self.pick_and_place(self.scanner, self.dustbin)
        print("Pick scanner to dustbin (wrong):", success)
        if not success:
            return self.info

        # Recovery: move scanner from dustbin to shoe_box
        success = self.pick_and_place(self.scanner, self.shoe_box)
        print("Recover scanner to shoe_box:", success)
        if not success:
            return self.info

        # Place shampoo (reusable bottle) in shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Pick shampoo to shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if all objects are in their correct containers:
        - Durable reusable items in shoe_box
        - Single-use disposable items in dustbin
        """
        return (
            self.check_on(self.mouse, self.shoe_box) and
            self.check_on(self.scanner, self.shoe_box) and
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.shampoo, self.shoe_box)
        )
