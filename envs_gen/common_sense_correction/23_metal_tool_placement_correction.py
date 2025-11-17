from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 23_metal_tool_placement_correction(Imagine_Task):
    def load_actors(self):
        # Add the container
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add the target objects
        self.stapler = self.add_actor("stapler", "stapler")
        self.hammer = self.add_actor("hammer", "hammer")
        self.fork = self.add_actor("fork", "fork")
        self.mouse = self.add_actor("mouse", "mouse")
        
        # Add distractor objects
        distractor_list = ['pet-collar', 'sand-clock', 'tissue-box', 'shampoo', 'dumbbell', 'book']
        self.add_distractors(distractor_list)
        
        # Final scene check
        self.check_scene()

    def play_once(self):
        # Wrong action: pick mouse and place into fluted_block
        success = self.pick_and_place(self.mouse, self.fluted_block)
        print("Pick mouse into fluted_block (wrong):", success)
        if not success:
            return self.info

        # Recovery: pick mouse from fluted_block and place back on table
        success = self.pick_and_place(self.mouse, self.table)
        print("Recover mouse to table:", success)
        if not success:
            return self.info

        # Correct actions for metal tools
        success = self.pick_and_place(self.stapler, self.fluted_block)
        print("Pick stapler into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Pick hammer into fluted_block:", success)
        if not success:
            return self.info

        success = self.pick_and_place(self.fork, self.fluted_block)
        print("Pick fork into fluted_block:", success)
        if not success:
            return self.info

        self.add_end()
        return self.info

    def check_success(self):
        # Verify all metal tools are in the fluted_block
        return (self.check_on(self.stapler, self.fluted_block) and
                self.check_on(self.hammer, self.fluted_block) and
                self.check_on(self.fork, self.fluted_block))
