from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class organize_heavy_and_small_items_correction(Imagine_Task):
    def load_actors(self):
        """
        Load all necessary actors (objects and containers) into the environment.
        - Containers: coaster and fluted_block
        - Objects: hammer, drill, stapler, fork
        - Distractors: pot-with-plant, shoe, microphone, shampoo
        """
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        self.stapler = self.add_actor("stapler", "stapler")
        self.fork = self.add_actor("fork", "fork")
        
        # Add distractors
        distractor_list = ["pot-with-plant", "shoe", "microphone", "shampoo"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """
        Execute the robot's actions in the environment:
        1. Pick hammer and place it on fluted_block
        2. Pick stapler and place it on fluted_block (wrong action)
        3. Pick stapler from fluted_block and place it on coaster (recovery)
        4. Pick drill and place it on fluted_block
        5. Pick fork and place it on coaster
        """
        # Step 1: Place hammer on fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Pick hammer to fluted_block:", success)
        if not success:
            return self.info

        # Step 2: Place stapler on fluted_block (wrong action)
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Pick stapler to fluted_block (wrong):", success)
        if not success:
            return self.info

        # Step 3: Recovery - Place stapler on coaster
        success = self.pick_and_place(self.stapler, self.coaster)
        print("Pick stapler to coaster (recovery):", success)
        if not success:
            return self.info

        # Step 4: Place drill on fluted_block
        success = self.pick_and_place(self.drill, self.fluted_block)
        print("Pick drill to fluted_block:", success)
        if not success:
            return self.info

        # Step 5: Place fork on coaster
        success = self.pick_and_place(self.fork, self.coaster)
        print("Pick fork to coaster:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        """
        Check if the task is successfully completed:
        - Heavy repair tools (hammer, drill) are on fluted_block
        - Small office/eating utensils (stapler, fork) are on coaster
        """
        if (self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.drill, self.fluted_block) and
            self.check_on(self.stapler, self.coaster) and
            self.check_on(self.fork, self.coaster)):
            return True
        return False
