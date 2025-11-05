from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 3_color_block_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add all required containers and objects
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.coaster = self.add_actor("coaster", "coaster")
        self.bottle = self.add_actor("bottle", "bottle")
        self.orange_block = self.add_actor("orange_block", "orange_block")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.french_fries = self.add_actor("french_fries", "french_fries")

    def play_once(self):
        # Pick orange_block from wooden_box and place into coaster
        success = self.pick_and_place(self.orange_block, self.coaster)
        print("pick place orange_block:", success)
        if not success:
            return self.info

        # Pick bottle and place into wooden_box
        success = self.pick_and_place(self.bottle, self.wooden_box)
        print("pick place bottle:", success)
        if not success:
            return self.info

        # Pick tissue-box and place into wooden_box
        success = self.pick_and_place(self.tissue_box, self.wooden_box)
        print("pick place tissue-box:", success)
        if not success:
            return self.info

        # Pick french_fries and place into wooden_box
        success = self.pick_and_place(self.french_fries, self.wooden_box)
        print("pick place french_fries:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if bottle is on wooden_box
        bottle_on_wooden = self.check_on(self.bottle, self.wooden_box)
        # Check if tissue-box is on wooden_box
        tissue_on_wooden = self.check_on(self.tissue_box, self.wooden_box)
        # Check if french_fries is on wooden_box
        fries_on_wooden = self.check_on(self.french_fries, self.wooden_box)
        # Check if orange_block is on coaster
        orange_on_coaster = self.check_on(self.orange_block, self.coaster)

        return bottle_on_wooden and tissue_on_wooden and fries_on_wooden and orange_on_coaster
