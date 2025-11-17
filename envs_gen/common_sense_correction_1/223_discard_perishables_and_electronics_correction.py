from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 223_discard_perishables_and_electronics_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors and distractors into the environment"""
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add required objects
        self.apple = self.add_actor("apple", "apple")
        self.mouse = self.add_actor("mouse", "mouse")
        self.book = self.add_actor("book", "book")
        self.hammer = self.add_actor("hammer", "hammer")
        
        # Add distractors from the task description
        distractors = ['pot-with-plant', 'toycar', 'dumbbell', 'shoe', 'purple_block']
        self.add_distractors(distractors)

    def play_once(self):
        """Execute the sequence of robot actions for the task"""
        # Place perishable food (apple) in dustbin
        success = self.pick_and_place(self.apple, self.dustbin)
        print("Place apple in dustbin:", success)
        if not success:
            return self.info

        # Place small office electronics (mouse) in dustbin
        success = self.pick_and_place(self.mouse, self.dustbin)
        print("Place mouse in dustbin:", success)
        if not success:
            return self.info

        # Wrong action: Place tool (hammer) in dustbin
        success = self.pick_and_place(self.hammer, self.dustbin)
        print("Wrong: Place hammer in dustbin:", success)
        if not success:
            return self.info

        # Recovery: Retrieve hammer from dustbin and place on table
        success = self.pick_and_place(self.hammer, self.table)
        print("Recover hammer to table:", success)
        if not success:
            return self.info

        # Place reading material (book) on table
        success = self.pick_and_place(self.book, self.table)
        print("Place book on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        # Check if perishables and electronics are in dustbin
        # and tools/reading materials are on the table
        return (
            self.check_on(self.apple, self.dustbin) and
            self.check_on(self.mouse, self.dustbin) and
            self.check_on(self.hammer, self.table) and
            self.check_on(self.book, self.table)
        )
