from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 154_organize_kitchen_play_with_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add main objects to the environment
        self.teanet = self.add_actor("teanet", "teanet")
        self.bread = self.add_actor("bread", "bread")
        self.scanner = self.add_actor("scanner", "scanner")
        self.red_block = self.add_actor("red_block", "red_block")
        
        # Add distractor objects to the environment
        distractors = ['pet-collar', 'book', 'bell', 'tissue-box']
        self.add_distractors(distractors)

    def play_once(self):
        # 1. Place teanet on fluted_block (flat organizer)
        success = self.pick_and_place(self.teanet, self.fluted_block)
        print("Place teanet:", success)
        if not success:
            return self.info

        # 2. Place scanner on fluted_block (wrong placement)
        success = self.pick_and_place(self.scanner, self.fluted_block)
        print("Place scanner (wrong):", success)
        if not success:
            return self.info

        # 3. Recover by moving scanner to shoe_box (enclosed storage)
        success = self.pick_and_place(self.scanner, self.shoe_box)
        print("Recover scanner:", success)
        if not success:
            return self.info

        # 4. Place bread on fluted_block (flat organizer)
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread:", success)
        if not success:
            return self.info

        # 5. Place red_block on fluted_block (flat organizer)
        success = self.pick_and_place(self.red_block, self.fluted_block)
        print("Place red_block:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in their correct final positions
        return (
            self.check_on(self.teanet, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block) and
            self.check_on(self.red_block, self.fluted_block) and
            self.check_on(self.scanner, self.shoe_box)
        )
