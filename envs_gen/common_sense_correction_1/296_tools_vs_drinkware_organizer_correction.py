from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 296_tools_vs_drinkware_organizer_correction(Imagine_Task):
    def load_actors(self):
        # Create containers and objects in the scene
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.mug = self.add_actor("mug", "mug")
        self.cup_without_handle = self.add_actor("cup_without_handle", "cup_without_handle")
        
        # Add distractor objects to the environment
        distractor_list = ["calculator", "toycar", "book", "alarm-clock"]
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place hammer in organizer
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Place hammer:", success)
        if not success:
            return self.info

        # Wrongly place cup_without_handle in organizer
        success = self.pick_and_place(self.cup_without_handle, self.fluted_block)
        print("Wrong place cup:", success)
        if not success:
            return self.info

        # Recovery: move cup_without_handle back to table
        success = self.pick_and_place(self.cup_without_handle, self.table)
        print("Recover cup:", success)
        if not success:
            return self.info

        # Place screwdriver in organizer
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Place screwdriver:", success)
        if not success:
            return self.info

        # Place mug on table
        success = self.pick_and_place(self.mug, self.table)
        print("Place mug:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify tools are in organizer and drinkware is on table
        tools_in_organizer = (self.check_on(self.hammer, self.fluted_block) and 
                             self.check_on(self.screwdriver, self.fluted_block))
        drinks_on_table = (self.check_on(self.mug, self.table) and 
                          self.check_on(self.cup_without_handle, self.table))
        return tools_in_organizer and drinks_on_table
