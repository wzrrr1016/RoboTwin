from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 364_eating_vs_tools_and_decor_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.plate = self.add_actor("plate", "plate")
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        
        # Add required objects
        self.bottle = self.add_actor("bottle", "bottle")
        self.fork = self.add_actor("fork", "fork")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        
        # Add distractors
        distractor_list = ['calculator', 'pet-collar', 'toycar', 'alarm-clock', 'book']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place eating-related items on the plate
        success = self.pick_and_place(self.fork, self.plate)
        print("Pick and place fork:", success)
        if not success:
            return self.info
        
        success = self.pick_and_place(self.bottle, self.plate)
        print("Pick and place bottle:", success)
        if not success:
            return self.info
        
        # Wrong placement of pot-with-plant on plate
        success = self.pick_and_place(self.pot_with_plant, self.plate)
        print("Pick and place pot-with-plant (wrong):", success)
        if not success:
            return self.info
        
        # Recovery: Move pot-with-plant to wooden_box
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Pick and place pot-with-plant (recovery):", success)
        if not success:
            return self.info
        
        # Place tools into wooden_box
        success = self.pick_and_place(self.screwdriver, self.wooden_box)
        print("Pick and place screwdriver:", success)
        if not success:
            return self.info

    def check_success(self):
        # Verify all objects are in the correct containers
        if (self.check_on(self.fork, self.plate) and
            self.check_on(self.bottle, self.plate) and
            self.check_on(self.pot_with_plant, self.wooden_box) and
            self.check_on(self.screwdriver, self.wooden_box)):
            return True
        return False
