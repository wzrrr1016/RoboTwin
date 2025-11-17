from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 17_recyclable_nonrecyclable_sorting_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the scene
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add recyclable objects to the scene
        self.book = self.add_actor("book", "book")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects to the scene
        distractor_list = ['red_block', 'green_block', 'blue_block', 'yellow_block', 'purple_block']
        self.add_distractors(distractor_list)
        
        # Verify scene setup
        self.check_scene()

    def play_once(self):
        # Place recyclable items in dustbin
        success = self.pick_and_place(self.book, self.dustbin)
        print("Place book in dustbin:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Place tissue-box in dustbin:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.shampoo, self.dustbin)
        print("Place shampoo in dustbin:", success)
        if not success:
            return self.info

        # Wrong placement of non-recyclable item
        success = self.pick_and_place(self.bread, self.dustbin)
        print("Wrong placement of bread in dustbin:", success)
        if not success:
            return self.info

        # Recovery: Correct placement of non-recyclable item
        success = self.pick_and_place(self.bread, self.tray)
        print("Correct placement of bread in tray:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Verify all items are in their correct containers
        if (self.check_on(self.book, self.dustbin) and
            self.check_on(self.tissue_box, self.dustbin) and
            self.check_on(self.shampoo, self.dustbin) and
            self.check_on(self.bread, self.tray)):
            return True
        return False
