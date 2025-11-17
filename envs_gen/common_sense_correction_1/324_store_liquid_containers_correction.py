from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 324_store_liquid_containers_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all required actors into the environment.
        - Containers: shoe_box
        - Objects: can, cup_without_handle, shampoo, green_block, book
        - Distractors: calculator, stapler, hammer, mouse, alarm-clock
        """
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add objects
        self.can = self.add_actor("can", "can")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.green_block = self.add_actor("green_block", "green_block")
        self.book = self.add_actor("book", "book")
        
        # Add distractors
        distractor_list = ['calculator', 'stapler', 'hammer', 'mouse', 'alarm-clock']
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Put can in shoe_box
        2. Put book in shoe_box (wrong action)
        3. Put book back on table (recovery)
        4. Put cup_without_handle in shoe_box
        5. Put shampoo in shoe_box
        6. Put green_block on table
        """
        # 1. Put can in shoe_box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Put can in shoe_box:", success)
        if not success:
            return self.info

        # 2. Put book in shoe_box (wrong action)
        success = self.pick_and_place(self.book, self.shoe_box)
        print("Put book in shoe_box (wrong):", success)
        if not success:
            return self.info

        # 3. Put book back on table (recovery)
        success = self.pick_and_place(self.book, self.table)
        print("Put book on table (recovery):", success)
        if not success:
            return self.info

        # 4. Put cup_without_handle in shoe_box
        success = self.pick_and_place(self.cup_without_handle, self.shoe_box)
        print("Put cup_without_handle in shoe_box:", success)
        if not success:
            return self.info

        # 5. Put shampoo in shoe_box
        success = self.pick_and_place(self.shampoo, self.shoe_box)
        print("Put shampoo in shoe_box:", success)
        if not success:
            return self.info

        # 6. Put green_block on table
        success = self.pick_and_place(self.green_block, self.table)
        print("Put green_block on table:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Verify if the task was completed successfully:
        - All liquid-containing items (can, cup_without_handle, shampoo) in shoe_box
        - Solid items (green_block, book) on the table
        """
        return (
            self.check_on(self.can, self.shoe_box) and
            self.check_on(self.cup_without_handle, self.shoe_box) and
            self.check_on(self.shampoo, self.shoe_box) and
            self.check_on(self.green_block, self.table) and
            self.check_on(self.book, self.table)
        )
