from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 266_organize_tableware_and_toys_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the simulation environment.
        - Containers: tray and dustbin
        - Objects: knife, fork, pink_block, toycar
        - Distractors: calculator, screwdriver, pot-with-plant, alarm-clock, shoe
        """
        # Add containers
        self.tray = self.add_actor("tray", "tray")
        self.dustbin = self.add_actor("dustbin", "dustbin")
        
        # Add objects
        self.knife = self.add_actor("knife", "knife")
        self.fork = self.add_actor("fork", "fork")
        self.pink_block = self.add_actor("pink_block", "pink_block")
        self.toycar = self.add_actor("toycar", "toycar")
        
        # Add distractors
        distractor_list = ["calculator", "screwdriver", "pot-with-plant", "alarm-clock", "shoe"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the sequence of actions for the robot arm:
        1. Place knife into dustbin (wrong action)
        2. Recover knife by placing it onto tray
        3. Place fork onto tray
        4. Place pink_block into dustbin
        5. Place toycar into dustbin
        """
        # Step 1: Wrong placement of knife into dustbin
        success = self.pick_and_place(self.knife, self.dustbin)
        print("Place knife into dustbin (wrong):", success)
        if not success:
            return self.info

        # Step 2: Recovery, move knife from dustbin to tray
        success = self.pick_and_place(self.knife, self.tray)
        print("Recover knife to tray:", success)
        if not success:
            return self.info

        # Step 3: Place fork on tray
        success = self.pick_and_place(self.fork, self.tray)
        print("Place fork on tray:", success)
        if not success:
            return self.info

        # Step 4: Place pink_block into dustbin
        success = self.pick_and_place(self.pink_block, self.dustbin)
        print("Place pink_block into dustbin:", success)
        if not success:
            return self.info

        # Step 5: Place toycar into dustbin
        success = self.pick_and_place(self.toycar, self.dustbin)
        print("Place toycar into dustbin:", success)
        if not success:
            return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Eating utensils (knife and fork) are on the tray
        - Small playthings (pink_block and toycar) are in the dustbin
        """
        if (self.check_on(self.knife, self.tray) and 
            self.check_on(self.fork, self.tray) and 
            self.check_on(self.pink_block, self.dustbin) and 
            self.check_on(self.toycar, self.dustbin)):
            return True
        return False
