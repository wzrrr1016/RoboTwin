from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 462_coaster_safe_support_correction(Imagine_Task):
    def load_actors(self):
        # Add the coaster as a container
        self.coaster = self.add_actor("coaster", "coaster")

        # Add the main objects
        self.cup = self.add_actor("cup", "cup")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.hammer = self.add_actor("hammer", "hammer")
        self.french_fries = self.add_actor("french_fries", "french_fries")

        # Add distractors
        distractor_list = ["calculator", "pet-collar", "alarm-clock", "book", "small-speaker"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick cup and place it on the coaster
        success = self.pick_and_place(self.cup, self.coaster)
        print("Place cup on coaster:", success)
        if not success:
            return self.info

        # 2. Pick hammer and place it on the coaster (wrong action)
        success = self.pick_and_place(self.hammer, self.coaster)
        print("Place hammer on coaster (wrong):", success)
        if not success:
            return self.info

        # 3. Pick hammer from coaster and place it on the table (recovery)
        success = self.pick_and_place(self.hammer, self.table)
        print("Move hammer to table:", success)
        if not success:
            return self.info

        # 4. Pick french_fries and place it on the table
        success = self.pick_and_place(self.french_fries, self.table)
        print("Place french fries on table:", success)
        if not success:
            return self.info

        # 5. Pick blue_block and place it on the coaster
        success = self.pick_and_place(self.blue_block, self.coaster)
        print("Place blue block on coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if the correct items are on the coaster
        cup_on_coaster = self.check_on(self.cup, self.coaster)
        blue_block_on_coaster = self.check_on(self.blue_block, self.coaster)

        # Check if the incorrect items are NOT on the coaster (i.e., on the table)
        hammer_on_table = self.check_on(self.hammer, self.table)
        french_fries_on_table = self.check_on(self.french_fries, self.table)

        # All conditions must be satisfied
        return cup_on_coaster and blue_block_on_coaster and hammer_on_table and french_fries_on_table
