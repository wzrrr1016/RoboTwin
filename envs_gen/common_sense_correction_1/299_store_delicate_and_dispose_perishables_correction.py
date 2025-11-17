from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 299_store_delicate_and_dispose_perishables_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors and distractors into the environment.
        Containers: dustbin, wooden_box
        Objects: apple, bottle, small-speaker, sand-clock, bell
        Distractors: dumbbell, shoe, book
        """
        # Add containers to the environment
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add required objects to the environment
        self.apple = self.add_actor("apple", "apple")
        self.bottle = self.add_actor("bottle", "bottle")
        self.small_speaker = self.add_actor("small-speaker", "small_speaker")
        self.sand_clock = self.add_actor("sand-clock", "sand_clock")
        self.bell = self.add_actor("bell", "bell")
        
        # Add distractor objects to the environment
        self.add_distractors(['dumbbell', 'shoe', 'book'])

    def play_once(self):
        """
        Execute the sequence of actions for the robot:
        1. Wrongly place bottle in wooden_box
        2. Correct by moving bottle to dustbin
        3. Place apple in dustbin
        4. Place small-speaker in wooden_box
        5. Place sand-clock in wooden_box
        6. Place bell in wooden_box
        """
        # Step 1: Wrong placement of bottle in wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("Wrong placement of bottle:", success)
        if not success:
            return self.info

        # Step 2: Recovery - move bottle to dustbin
        success = self.pick_and_place(self.bottle, self.dustbin)
        print("Recovery of bottle:", success)
        if not success:
            return self.info

        # Step 3: Place apple in dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Place apple:", success)
        if not success:
            return self.info

        # Step 4: Place small-speaker in wooden_box
        success = self.pick_and_place(self.small_speaker, self.wooden_box)
        print("Place small speaker:", success)
        if not success:
            return self.info

        # Step 5: Place sand-clock in wooden_box
        success = self.pick_and_place(self.sand_clock, self.wooden_box)
        print("Place sand clock:", success)
        if not success:
            return self.info

        # Step 6: Place bell in wooden_box
        success = self.pick_and_place(self.bell, self.wooden_box)
        print("Place bell:", success)
        if not success:
            return self.info

        return self.info  # All steps completed successfully

    def check_success(self):
        """
        Verify that all objects are in their correct final locations:
        - Perishable edible (apple) and disposable drink (bottle) in dustbin
        - Small/delicate items (small-speaker, sand-clock, bell) in wooden_box
        """
        return (
            self.check_on(self.apple, self.dustbin) and
            self.check_on(self.bottle, self.dustbin) and
            self.check_on(self.small_speaker, self.wooden_box) and
            self.check_on(self.sand_clock, self.wooden_box) and
            self.check_on(self.bell, self.wooden_box)
        )
