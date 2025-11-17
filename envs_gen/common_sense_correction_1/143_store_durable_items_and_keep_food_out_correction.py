from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 143_store_durable_items_and_keep_food_out_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the simulation environment.
        - Containers: shoe_box
        - Objects: toycar, hammer, can, apple, fork
        - Distractors: calculator, alarm-clock, book, microphone, small-speaker
        """
        # Create main container
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Create objects to be manipulated
        self.toycar = self.add_actor("toycar", "toycar")
        self.hammer = self.add_actor("hammer", "hammer")
        self.can = self.add_actor("can", "can")
        self.apple = self.add_actor("apple", "apple")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractor objects
        distractor_list = ["calculator", "alarm-clock", "book", "microphone", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of robot arm actions to complete the task:
        1. Place durable non-food items in shoe_box
        2. Place edible and tableware items on top of shoe_box
        3. Correct any misplaced items
        """
        # Place durable non-food items in shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Place toycar:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Place hammer:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.shoe_box)
        print("Place can:", success)
        if not success:
            return self.info

        # Place edible item on top of shoe_box
        success = self.pick_and_place(self.apple, self.shoe_box)
        print("Place apple:", success)
        if not success:
            return self.info

        # Place fork in shoe_box (wrong action)
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("Place fork (wrong):", success)
        if not success:
            return self.info

        # Recovery: Move fork from inside to on top of shoe_box
        success = self.pick_and_place(self.fork, self.shoe_box)
        print("Recover fork:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - Durable non-food items (toycar, hammer, can) are in shoe_box
        - Edible (apple) and tableware (fork) are on top of shoe_box
        """
        # Check all required objects are properly placed
        if (
            self.check_on(self.toycar, self.shoe_box) and
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.can, self.shoe_box) and
            self.check_on(self.apple, self.shoe_box) and
            self.check_on(self.fork, self.shoe_box)
        ):
            return True
        return False
