from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 31_tool_separation_correction(Imagine_Task):
    def load_actors(self):
        # Add containers
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add task-specific objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.drill = self.add_actor("drill", "drill")
        self.pot_with_plant = self.add_actor("pot-with-plant", "pot-with-plant")
        self.hamburg = self.add_actor("hamburg", "hamburg")
        self.bread = self.add_actor("bread", "bread")
        
        # Add distractors
        distractor_list = ["calculator", "pet-collar", "table-tennis", "roll-paper", "battery", "scanner"]
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Place tools in wooden_box
        success = self.pick_and_place(self.hammer, self.wooden_box)
        print("Place hammer:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.drill, self.wooden_box)
        print("Place drill:", success)
        if not success:
            return self.info
            
        # Wrong placement of non-tool (recovery needed)
        success = self.pick_and_place(self.pot_with_plant, self.wooden_box)
        print("Wrong placement of pot-with-plant:", success)
        if not success:
            return self.info
            
        # Recovery: move non-tool to correct container
        success = self.pick_and_place(self.pot_with_plant, self.fluted_block)
        print("Recover pot-with-plant:", success)
        if not success:
            return self.info
            
        # Place remaining non-tools in fluted_block
        success = self.pick_and_place(self.hamburg, self.fluted_block)
        print("Place hamburg:", success)
        if not success:
            return self.info
            
        success = self.pick_and_place(self.bread, self.fluted_block)
        print("Place bread:", success)
        if not success:
            return self.info
            
        self.add_end()
        return self.info

    def check_success(self):
        # Verify all objects are in their correct containers
        return (
            self.check_on(self.hammer, self.wooden_box) and
            self.check_on(self.drill, self.wooden_box) and
            self.check_on(self.pot_with_plant, self.fluted_block) and
            self.check_on(self.hamburg, self.fluted_block) and
            self.check_on(self.bread, self.fluted_block)
        )
