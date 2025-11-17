from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 286_store_tools_dispose_recyclables_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.dustbin = self.add_actor("dustbin", "dustbin")
        self.shoe_box = self.add_actor("shoe_box", "shoe_box")
        
        # Add required objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.dumbbell = self.add_actor("dumbbell", "dumbbell")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        self.can = self.add_actor("can", "can")
        
        # Add distractors
        distractor_list = ["calculator", "pot-with-plant", "book", "small-speaker", "apple"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # 1. Wrong action: Put can in shoe box
        success = self.pick_and_place(self.can, self.shoe_box)
        print("Put can in shoe_box (wrong):", success)
        if not success:
            return self.info

        # 2. Recovery: Move can to dustbin
        success = self.pick_and_place(self.can, self.dustbin)
        print("Move can to dustbin (recovery):", success)
        if not success:
            return self.info

        # 3. Put tissue box in dustbin
        success = self.pick_and_place(self.tissue_box, self.dustbin)
        print("Put tissue-box in dustbin:", success)
        if not success:
            return self.info

        # 4. Put hammer in shoe box
        success = self.pick_and_place(self.hammer, self.shoe_box)
        print("Put hammer in shoe_box:", success)
        if not success:
            return self.info

        # 5. Put screwdriver in shoe box
        success = self.pick_and_place(self.screwdriver, self.shoe_box)
        print("Put screwdriver in shoe_box:", success)
        if not success:
            return self.info

        # 6. Put dumbbell in shoe box
        success = self.pick_and_place(self.dumbbell, self.shoe_box)
        print("Put dumbbell in shoe_box:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Check if all tools and equipment are in shoe box
        tools_in_shoe = (
            self.check_on(self.hammer, self.shoe_box) and
            self.check_on(self.screwdriver, self.shoe_box) and
            self.check_on(self.dumbbell, self.shoe_box)
        )
        
        # Check if disposables are in dustbin
        disposables_in_dustbin = (
            self.check_on(self.can, self.dustbin) and
            self.check_on(self.tissue_box, self.dustbin)
        )
        
        return tools_in_shoe and disposables_in_dustbin
