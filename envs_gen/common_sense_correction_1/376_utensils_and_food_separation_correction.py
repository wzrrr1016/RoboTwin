from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 376_utensils_and_food_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers to the environment
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.tray = self.add_actor("tray", "tray")
        
        # Add required objects to the environment
        self.knife = self.add_actor("knife", "knife")
        self.fork = self.add_actor("fork", "fork")
        self.bread = self.add_actor("bread", "bread")
        self.bottle = self.add_actor("bottle", "bottle")
        
        # Add distractor objects to the environment
        distractor_list = ['calculator', 'pet-collar', 'book', 'shoe', 'tissue-box']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Initial wrong placement of bottle into fluted_block
        success = self.pick_and_place(self.bottle, self.fluted_block)
        print("Wrong placement of bottle:", success)
        if not success:
            return self.info

        # Recovery: move bottle to tray
        success = self.pick_and_place(self.bottle, self.tray)
        print("Recovery placement of bottle:", success)
        if not success:
            return self.info

        # Place metal utensils and sharp tools into fluted_block
        success = self.pick_and_place(self.knife, self.fluted_block)
        print("Place knife:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Place fork:", success)
        if not success:
            return self.info

        # Place edible food and drink container onto tray
        success = self.pick_and_place(self.bread, self.tray)
        print("Place bread:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all required objects are in their correct containers
        if (self.check_on(self.knife, self.fluted_block) and
            self.check_on(self.fork, self.fluted_block) and
            self.check_on(self.bread, self.tray) and
            self.check_on(self.bottle, self.tray)):
            return True
        return False
