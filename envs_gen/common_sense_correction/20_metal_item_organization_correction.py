from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 20_metal_item_organization_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers and objects to the scene
        self.tray = self.add_actor("tray", "tray")
        self.fork = self.add_actor("fork", "fork")
        self.knife = self.add_actor("knife", "knife")
        self.can = self.add_actor("can", "can")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        
        # Add distractor objects to the scene
        distractor_list = ['calculator', 'cup-with-liquid', 'pet-collar', 'table-tennis', 'roll-paper']
        self.add_distractors(distractor_list)
        
        # Finalize scene setup
        self.check_scene()

    def play_once(self):
        # Pick and place metal items into the tray
        success = self.pick_and_place(self.fork, self.tray)
        print("pick place fork:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.knife, self.tray)
        print("pick place knife:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.can, self.tray)
        print("pick place can:", success)
        if not success:
            return self.info

        # Attempt to place shampoo in tray (wrong action)
        success = self.pick_and_place(self.shampoo, self.tray)
        print("pick place shampoo (wrong):", success)
        if not success:
            return self.info

        # Recovery: Place shampoo back on the table
        success = self.pick_and_place(self.shampoo, self.table)
        print("pick place shampoo (recovery):", success)
        if not success:
            return self.info

        # Mark task completion
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all metal items are in the tray and shampoo is not
        if (self.check_on(self.fork, self.tray) and
            self.check_on(self.knife, self.tray) and
            self.check_on(self.can, self.tray) and
            not self.check_on(self.shampoo, self.tray)):
            return True
        return False
