from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 48_non_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Add containers: coaster and wooden_box
        - Add objects: book, shoe, apple, yellow_block
        - Add distractors as specified in the task
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")

        # Add objects to be placed in the wooden_box
        self.book = self.add_actor("book", "book")
        self.shoe = self.add_actor("shoe", "shoe")
        self.apple = self.add_actor("apple", "apple")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")

        # Add distractors as specified in the task
        distractor_list = ["calculator", "table-tennis", "hammer", "toycar", "pot-with-plant", "alarm-clock"]
        self.add_distractors(distractor_list)

        # Final check to ensure all actors are placed correctly
        self.check_scene()

    def play_once(self):
        """
        Define the sequence of actions for the robot arm to complete the task.
        - First, place the shoe into the coaster (wrong action)
        - Then, recover by placing the shoe into the wooden_box
        - Place the remaining objects (book, apple, yellow_block) directly into the wooden_box
        """
        # First wrong action: place shoe into coaster
        success = self.pick_and_place(self.shoe, self.coaster)
        print("Pick place shoe into coaster (wrong):", success)
        if not success:
            return self.info

        # Recovery: pick shoe from coaster and place into wooden_box
        success = self.pick_and_place(self.shoe, self.wooden_box)
        print("Pick place shoe into wooden_box (recovery):", success)
        if not success:
            return self.info

        # Place other objects into wooden_box
        success = self.pick_and_place(self.book, self.wooden_box)
        print("Pick place book:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.apple, self.wooden_box)
        print("Pick place apple:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.yellow_block, self.wooden_box)
        print("Pick place yellow_block:", success)
        if not success:
            return self.info

        # Mark the end of the task
        self.add_end()
        return self.info

    def check_success(self):
        """
        Check if all non-drinkware items are placed in the wooden_box.
        - Verifies that the shoe, book, apple, and yellow_block are all on the wooden_box
        """
        if (self.check_on(self.shoe, self.wooden_box) and
            self.check_on(self.book, self.wooden_box) and
            self.check_on(self.apple, self.wooden_box) and
            self.check_on(self.yellow_block, self.wooden_box)):
            return True
        return False
