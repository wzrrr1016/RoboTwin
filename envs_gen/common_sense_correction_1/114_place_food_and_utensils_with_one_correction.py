from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 114_place_food_and_utensils_with_one_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: plate and dustbin
        - Objects: hamburg, fork, shampoo, pink_block
        - Distractors: calculator, screwdriver, pot-with-plant, book, alarm-clock, dumbbell
        """
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.dustbin = self.add_actor("dustbin", "dustbin")

        # Add objects
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.fork = self.add_actor("fork", "fork")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.pink_block = self.add_actor("pink_block", "pink_block")

        # Add distractors
        distractor_list = [
            "calculator", "screwdriver", "pot-with-plant", "book", "alarm-clock", "dumbbell"
        ]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        Actions:
        1. Pick hamburg and place it on the plate
        2. Pick fork and place it on the plate
        3. Pick shampoo and place it on the plate (wrong action)
        4. Pick shampoo from the plate and place it into the dustbin (recovery)
        5. Pick pink_block and place it into the dustbin
        """
        # Step 1: Place hamburg on the plate
        success = self.pick_and_place(self.hamburg, self.plate)
        print("Pick hamburg:", success)
        if not success:
            return self.info

        # Step 2: Place fork on the plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick fork:", success)
        if not success:
            return self.info

        # Step 3: Place shampoo on the plate (wrong action)
        success = self.pick_and_place(self.shampoo, self.plate)
        print("Pick shampoo (wrong):", success)
        if not success:
            return self.info

        # Step 4: Move shampoo from the plate to the dustbin (recovery)
        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Move shampoo to dustbin:", success)
        if not success:
            return self.info

        # Step 5: Place pink_block into the dustbin
        success = self.pick_and_place(self.pink_block, self.dustbin)
        print("Pick pink_block:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed by verifying the final positions of all objects.
        - hamburg and fork should be on the plate
        - shampoo and pink_block should be in the dustbin
        """
        if (
            self.check_on(self.hamburg, self.plate) and
            self.check_on(self.fork, self.plate) and
            self.check_on(self.shampoo, self.dustbin) and
            self.check_on(self.pink_block, self.dustbin)
        ):
            return True
        return False
