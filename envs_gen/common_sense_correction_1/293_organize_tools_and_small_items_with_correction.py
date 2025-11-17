from envs._base_task import Base_Task
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien

class 293_organize_tools_and_small_items_with_correction(Imagine_Task):
    def load_actors(self):
        # Add the organizer surface (container)
        self.fluted_block = self.add_actor("fluted_block", "fluted_block")
        
        # Add required objects
        self.hammer = self.add_actor("hammer", "hammer")
        self.screwdriver = self.add_actor("screwdriver", "screwdriver")
        self.yellow_block = self.add_actor("yellow_block", "yellow_block")
        self.purple_block = self.add_actor("purple_block", "purple_block")
        self.markpen = self.add_actor("markpen", "markpen")
        
        # Add distractors
        distractor_list = ['pot-with-plant', 'shoe', 'alarm-clock', 'baguette', 'tissue-box']
        self.add_distractors(distractor_list)

    def play_once(self):
        # Place hammer on fluted_block
        success = self.pick_and_place(self.hammer, self.fluted_block)
        print("Hammer placed:", success)
        if not success:
            return self.info

        # Place screwdriver on fluted_block
        success = self.pick_and_place(self.screwdriver, self.fluted_block)
        print("Screwdriver placed:", success)
        if not success:
            return self.info

        # Wrong placement: yellow_block on purple_block
        success = self.pick_and_place(self.yellow_block, self.purple_block)
        print("Yellow_block on purple_block (wrong):", success)
        if not success:
            return self.info

        # Recovery: move yellow_block to fluted_block
        success = self.pick_and_place(self.yellow_block, self.fluted_block)
        print("Yellow_block to fluted_block (recovery):", success)
        if not success:
            return self.info

        # Place purple_block on fluted_block
        success = self.pick_and_place(self.purple_block, self.fluted_block)
        print("Purple_block placed:", success)
        if not success:
            return self.info

        # Place markpen on fluted_block
        success = self.pick_and_place(self.markpen, self.fluted_block)
        print("Markpen placed:", success)
        if not success:
            return self.info

        return self.info

    def check_success(self):
        # Verify all required objects are on the fluted_block
        return (
            self.check_on(self.hammer, self.fluted_block) and
            self.check_on(self.screwdriver, self.fluted_block) and
            self.check_on(self.yellow_block, self.fluted_block) and
            self.check_on(self.purple_block, self.fluted_block) and
            self.check_on(self.markpen, self.fluted_block)
        )
