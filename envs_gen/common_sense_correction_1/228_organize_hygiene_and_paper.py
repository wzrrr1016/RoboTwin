from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 228_organize_hygiene_and_paper(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.hammer = self.add_actor("hammer", "hammer")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        
        # Add distractors
        distractor_list = ['small-speaker', 'dumbbell', 'pot-with-plant', 'red_block', 'battery']
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Pick shampoo and place it into fluted_block
        success = self.pick_and_place(self.shampoo, self.fluted_block)
        print("Pick shampoo:", success)
        if not success:
            return self.info

        # 2. Pick hammer and place it into fluted_block (wrong)
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Pick hammer (wrong):", success)
        if not success:
            return self.info

        # 3. Pick hammer from fluted_block and place it onto table (recovery)
        success = self.pick_and_place(self.hammer, self.table)
        print("Recover hammer:", success)
        if not success:
            return self.info

        # 4. Pick tissue-box and place it into fluted_block
        success = self.pick_and_place(self.tissue_box, self.fluted_block)
        print("Pick tissue-box:", success)
        if not success:
            return self.info

        # 5. Pick cup_without_handle and place it onto table
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("Pick cup:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if hygiene items are in the organizer
        shampoo_in = self.check_on(self.shampoo, self.fluted_block)
        tissue_in = self.check_on(self.tissue_box, self.fluted_block)
        
        # Check if non-hygiene items are not in the organizer
        hammer_not_in = not self.check_on(self.hammer, self.fluted_block)
        cup_not_in = not self.check_on(self.cup_without_handle, self.fluted_block)
        
        return shampoo_in and tissue_in and hammer_not_in and cup_not_in
