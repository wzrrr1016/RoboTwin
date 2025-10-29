
from envs._imagine_task import Imagine_Task
from envs.utils import *
import sapien


class ensure_majority_in_wooden_box(Imagine_Task):
    def load_actors(self):
        # Container
        self.wooden_box = self.add_actor("wooden_box", "wooden_box")
        self.plate = self.add_actor("plate", "plate")

        # Items: 5 blocks, aim majority of blocks in wooden_box
        poses = self.create_box_pose(5)
        colors = ["red", "blue", "green", "yellow", "purple"]
        self.blocks = []
        for i, (pose, color) in enumerate(zip(poses, colors)):
            blk = self.create_block(pose, color)
            blk.set_name(f"block_{i}")
            self.blocks.append(blk)

    def play_once(self):
        # Mistake: place two blocks on plate first, then recover one to wooden_box
        mistake_cnt = 0
        for blk in self.blocks[:2]:
            success = self.pick_place_block(blk, self.plate)
            if not success:
                return self.info
            mistake_cnt += 1
        # Recover one block to wooden_box
        success = self.pick_place_block(self.blocks[0], self.wooden_box)
        if not success:
            return self.info
        # Place remaining blocks to wooden_box to ensure majority
        for blk in self.blocks[2:]:
            success = self.pick_place_block(blk, self.wooden_box)
            if not success:
                return self.info

    def check_success(self):
        in_box = sum(self.check_actors_contact(blk, self.wooden_box) for blk in self.blocks)
        return in_box >= 3

