from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 19_drinkware_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.coaster = self.add_actor("coaster", "coaster")
        self.plate = self.add_actor("plate", "plate")
        
        # Add objects
        self.mug = self.add_actor("mug", "mug")
        self.can = self.add_actor("can", "can")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        
        # Add distractors
        distractor_list = ["calculator", "pet-collar", "table-tennis", "shoe", "book", "dumbbell"]
        self.add_distractors(distractor_list)
        
        # Check scene setup
        self.check_scene()

    def play_once(self):
        # Place drinkware items on coaster
        success = self.pick_and_place(self.mug, self.coaster)
        print("Pick mug to coaster:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.can, self.coaster)
        print("Pick can to coaster:", success)
        if not success:
            return self.info
            
        # Wrong placement and recovery
        success = self.pick_and_place(self.pot_with_plant, self.coaster)
        print("Pick pot-with-plant to coaster (wrong):", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.pot_with_plant, self.plate)
        print("Pick pot-with-plant to plate (recovery):", success)
        if not success:
            return self.info
            
        # Place non-drinkware items on plate
        success = self.pick_and_place(self.screwdriver, self.plate)
        print("Pick screwdriver to plate:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.yellow_block, self.plate)
        print("Pick yellow_block to plate:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all objects are in their correct final positions
        if (
            self.check_on(self.mug, self.coaster) and
            self.check_on(self.can, self.coaster) and
            self.check_on(self.pot_with_plant, self.plate) and
            self.check_on(self.screwdriver, self.plate) and
            self.check_on(self.yellow_block, self.plate)
        ):
            return True
        return False
