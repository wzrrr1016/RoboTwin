from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 3_repair_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add required containers and objects
        self.tray = self.add_actor("tray", "tray")
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        self.shampoo = self.add_actor("shampoo", "shampoo")
        self.tissue_box = self.add_actor("tissue-box", "tissue-box")
        
        # Add distractor objects
        distractor_list = ['calculator', 'pet-collar', 'table-tennis', 'stapler', 'scanner', 'mouse']
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Pick and place repair tools in tray
        success = self.pick_and_place(self.hammer, self.tray)
        print("Pick hammer:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.drill, self.tray)
        print("Pick drill:", success)
        if not success:
            return self.info
            
        # Wrong placement of shampoo in tray
        success = self.pick_and_place(self.shampoo, self.tray)
        print("Pick shampoo (wrong):", success)
        if not success:
            return self.info
            
        # Recovery - move shampoo to table
        success = self.pick_and_place(self.shampoo, self.table)
        print("Recover shampoo:", success)
        if not success:
            return self.info
            
        # Place tissue box on table
        success = self.pick_and_place(self.tissue_box, self.table)
        print("Pick tissue-box:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify final positions
        if (self.check_on(self.hammer, self.tray) and
            self.check_on(self.drill, self.tray) and
            self.check_on(self.shampoo, self.table) and
            self.check_on(self.tissue_box, self.table)):
            return True
        return False
