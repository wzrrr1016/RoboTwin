from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 61_organize_toys_and_blocks_correction(Imagine_Task):
    def load_actors(self):
        """Load all required actors into the environment"""
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the objects to be manipulated
        self.green_block = self.add_actor("green_block", "green_block")
        self.blue_block = self.add_actor("blue_block", "blue_block")
        self.toycar = self.add_actor("toycar", "toycar")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractor objects
        distractor_list = ["calculator", "screwdriver", "pot-with-plant", "alarm-clock", "markpen"]
        self.add_distractors(distractor_list)

    def play_once(self):
        """Execute the sequence of actions for the task"""
        # Initial wrong action: put bread in organizer
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Pick bread and place into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery: put bread back on table
        success = self.pick_and_place(self.bread, self.table)
        print("Pick bread from fluted_block and place on table (recovery):", success)
        if not success:
            return self.info

        # Place solid blocks in organizer
        success = self.pick_and_place(self.green_block, self.fluted_block)
        print("Pick green_block and place into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.blue_block, self.fluted_block)
        print("Pick blue_block and place into fluted_block:", success)
        if not success:
            return self.info

        # Place durable play item in organizer
        success = self.pick_and_place(self.toycar, self.fluted_block)
        print("Pick toycar and place into fluted_block:", success)
        if not success:
            return self.info

    def check_success(self):
        """Verify if the task was completed successfully"""
        return (
            self.check_on(self.green_block, self.fluted_block) and
            self.check_on(self.blue_block, self.fluted_block) and
            self.check_on(self.toycar, self.fluted_block)
        )
