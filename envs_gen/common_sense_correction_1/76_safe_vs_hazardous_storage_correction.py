from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 76_safe_vs_hazardous_storage_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        self.coaster = self.add_actor("coaster", "coaster")

        # Add objects
        self.apple = self.add_actor("apple", "apple")
        self.toycar = self.add_actor("toycar", "toycar")
        self.knife = self.add_actor("knife", "knife")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")

        # Add distractors
        distractors = ['calculator', 'alarm-clock', 'microphone', 'pot-with-plant', 'book']
        self.add_distractors(distractors)

    def play_once(self):
        # 1. Place apple on coaster
        success = self.pick_and_place(self.apple, self.coaster)
        print("Place apple on coaster:", success)
        if not success:
            return self.info

        # 2. Wrongly place toycar into shoe_box
        success = self.pick_and_place(self.toycar, self.shoe_box)
        print("Wrongly place toycar into shoe_box:", success)
        if not success:
            return self.info

        # 3. Recovery: move toycar to coaster
        success = self.pick_and_place(self.toycar, self.coaster)
        print("Recover toycar to coaster:", success)
        if not success:
            return self.info

        # 4. Place knife into shoe_box
        success = self.pick_and_place(self.knife, self.shoe_box)
        print("Place knife into shoe_box:", success)
        if not success:
            return self.info

        # 5. Place tissue-box into shoe_box
        success = self.pick_and_place(self.tissue_box, self.shoe_box)
        print("Place tissue-box into shoe_box:", success)
        if not success:
            return self.info

    def check_success(self):
        # Check if all objects are in their correct final positions
        apple_on_coaster = self.check_on(self.apple, self.coaster)
        toycar_on_coaster = self.check_on(self.toycar, self.coaster)
        knife_in_shoe_box = self.check_on(self.knife, self.shoe_box)
        tissue_in_shoe_box = self.check_on(self.tissue_box, self.shoe_box)

        return all([
            apple_on_coaster,
            toycar_on_coaster,
            knife_in_shoe_box,
            tissue_in_shoe_box
        ])
