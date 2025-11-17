from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 120_dispose_and_set_aside_correction(Imagine_Task):
    def load_actors(self):
        """Initialize all required objects and distractors in the environment."""
        # Add the dustbin container
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.can = self.add_actor("can", "can")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.book = self.add_actor("book", "book")
        self.apple = self.add_actor("apple", "apple")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add distractor objects
        distractor_list = ["toycar", "hammer", "shoe", "pot-with-plant", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of object sorting actions."""
        # Place non-reusable items into dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Place can into dustbin:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Place shampoo into dustbin:", success)
        if not success:
            return self.info

        # Initial incorrect placement of book (into dustbin)
        success = self.pick_and_place(self.book, self.dustbin)
        print("Initial book placement (into dustbin):", success)
        if not success:
            return self.info

        # Recovery: Place book on dustbin (correct placement)
        success = self.pick_and_place(self.book, self.dustbin)
        print("Recovery: Place book on dustbin:", success)
        if not success:
            return self.info

        # Place food item into dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Place apple into dustbin:", success)
        if not success:
            return self.info

        # Place stationery item on dustbin
        success = self.pick_and_place(self.markpen, self.dustbin)
        print("Place markpen on dustbin:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if all objects are placed correctly according to task requirements."""
        # Check if all required objects are on the dustbin
        return (
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.shampoo, self.dustbin) and
            self.check_on(self.book, self.dustbin) and
            self.check_on(self.apple, self.dustbin) and
            self.check_on(self.markpen, self.dustbin)
        )
