# ====================== PROMPT =============================

BASIC_INFO = '''
In this environment, distance 1 indicates 1 meter long. Pose is representated as 7 dimention, [x, y, z, qw, qx, qy, qz].
For a 7-dimensional Pose object, you can use Pose.p to get the [x, y, z] coordinates and Pose.q to get the [qw, qx, qy, qz] quaternion orientation.
All functions which has parameter actor, and all of actor should be in the Actor object.
In the world coordinate system, the positive directions of the xyz coordinate axes are right, front, and upper respectively, so the direction vectors on the right, front,
and upper sides are [1,0,0], [0,1,0], [0,0,1] respectively. In the same way, we can get the unit vectors of the left side, back side and down side.
Each actor in the environment has one or more functional points, which are specific locations designed for interactions. 
Access functional points using actor.get_functional_point(point_id, return_type), where return_type can be "pose", "p", or "q".
'''

CODE_TEMPLATE = '''
from envs._base_task import Base_Task  
from envs.$TASK_NAME$ import $TASK_NAME$
from envs.utils import *
import sapien

class gpt_$TASK_NAME$($TASK_NAME$):
    def load_actors(self):
        pass
        
    def play_once(self):
        pass
    
    def check_success(self):
    pass
'''

AVAILABLE_ENV_FUNCTION_LOAD_ACTORS = {
    "add_actor":
    "def add_actor(self, actor_type:str, actor_name:str)\
        add an actor (eg. plate, bowl...) to the environment.\
        Args:\
        actor_type: The type of the actor to be added, eg. plate \
        actor_name: The name of the actor to be added, eg. plate_0\
        return: Actor object",
    "create_box_pose":
    "def create_box_pose(self,num, block_half_size=0.02)\
        create n=num box poses in the environment.\
        Args:\
        num: The number of box poses to be created\
        block_half_size: The half size of the box, default is 0.02\
        return: list of box poses",
    "create_block":
    "def create_block(self, block_pose, color, block_half_size=0.02)\
        create a block in the environment.\
        Args:\
        block_pose: The pose of the block\
        color: The color name of the block\
        block_half_size: The half size of the block, default is 0.02\
        return: Block object",
    "add_prohibit_area":
    "def add_prohibit_area(self, actor, padding=0.05)\
        add a prohibit area in the environment.\
        Args:\
        actor: The actor to be added\
        padding: The padding of the prohibit area, default is 0.05\
        return: None",
    "set_name":
    "def set_name(self, name)\
        set the name of the actor.\
        Args:\
        name: The name of the actor\
        return: None"
}

AVAILABLE_ENV_FUNCTION_PLAY_ONCE = {
    "pick_place_block":
    "def pick_place_block(self, block, container)\
        pick a block and place it in the container.\
        Args:\
        block: The block to be picked and placed\
        container: The container to be placed in\
        return success",
    "pick_block":
    "def pick_block(self, block)\
        pick a block.\
        Args:\
        block: The block to be picked\
        return success",
    "place_block":
    "def place_block(self, block, container)\
        place a block in the container.\
        Args:\
        block: The block to be placed\
        container: The container to be placed in\
        return success"
}

AVAILABLE_ENV_FUNCTION_CHECK_SUCCESS = {
    "check_grasp":
    "def check_grasp(self, actor)\
        check if the actor is grasped by the arm.\
        Args:\
        actor: The actor to be checked\
        return success",
    "check_on":
    "def check_on(self,actor,container)\
        check if the actor is on the container.\
        Args:\
        actor: The actor to be checked\
        container: The container to be checked\
        return success"
}

FUNCTION_EXAMPLE = '''
First you need to complete the load_actors function, which is used to load the actors into the environment. 
You can use the following functions to load actors:

add_actor: Add an actor to the environment.
create_box_pose: Create n=num box poses in the environment.
create_block: Create a block in the environment.
add_prohibit_area: Add a prohibit area in the environment.
set_name: Set the name of the actor.

For example:
```python
    def load_actors(self):
        self.plate = self.add_actor("plate","plate")
        
        block_pose_lst = self.create_box_pose(num=3)

        self.red_block = self.create_block(block_pose_lst[0], "red")
        self.green_block = self.create_block(block_pose_lst[2], "green")
        self.blue_block = self.create_block(block_pose_lst[4], "blue")

        self.add_prohibit_area(self.red_block, padding=0.05)
        self.add_prohibit_area(self.blue_block, padding=0.05)
        self.add_prohibit_area(self.green_block, padding=0.05)


        self.red_block.set_name("red_block")
        self.blue_block.set_name("blue_block")
        self.green_block.set_name("green_block")
```

Next, you need to complete the play_once function, which is used to define the action of the robot arm. 

pick_place_block: Pick a block and place it in the container.
pick_block: Pick a block.
place_block: Place a block in the container.

For example:
```python
    def play_once(self):
        success = self.pick_place_block(self.red_block1,self.plate)
        print("pick place red_block1:",success)
        if not success:
            return self.info
        success = self.pick_place_block(self.red_block2,self.plate)
        print("pick place red_block2:",success)
        if not success:
            return self.info
        success = self.pick_place_block(self.blue_block1,self.plate)
        print("pick place blue_block1:",success)
        if not success:
            return self.info
        
        success = self.pick_place_block(self.green_block1,self.plate)
        print("pick place green_block1:",success)
        if not success:
            return self.info
```

Finally, you need to complete the check_success function, which is used to check the success of the action.

check_grasp: Check if the actor is grasped by the arm.
check_on: Check if the actor is on the container.

For example:
```python
    def check_success(self):
        if self.check_on(self.red_block, self.plate) and self.check_on(self.blue_block, self.plate) and self.check_on(self.green_block, self.plate):
            return True
        return False
```

The complete code is as follow:

```python

class gpt_{task_name}(Pick_Place_Task):

    def load_actors(self):

        self.plate = self.add_actor("plate","plate")
        
        block_pose_lst = self.create_box_pose(num=6)

        self.red_block1 = self.create_block(block_pose_lst[0], "red")
        self.red_block2 = self.create_block(block_pose_lst[1], "red")
        self.green_block1 = self.create_block(block_pose_lst[2], "green")
        self.green_block2 = self.create_block(block_pose_lst[3], "green")
        self.blue_block1 = self.create_block(block_pose_lst[4], "blue")
        self.blue_block2 = self.create_block(block_pose_lst[5], "blue")

        self.add_prohibit_area(self.red_block1, padding=0.05)
        self.add_prohibit_area(self.red_block2, padding=0.05)
        self.add_prohibit_area(self.blue_block1, padding=0.05)
        self.add_prohibit_area(self.blue_block2, padding=0.05)
        self.add_prohibit_area(self.green_block1, padding=0.05)
        self.add_prohibit_area(self.green_block2, padding=0.05)


        self.red_block1.set_name("red_block1")
        self.red_block2.set_name("red_block2")
        self.blue_block1.set_name("blue_block1")
        self.blue_block2.set_name("blue_block2")
        self.green_block1.set_name("green_block1")
        self.green_block2.set_name("green_block2")

    def play_once(self):
        success = self.pick_place_block(self.red_block1,self.plate)
        print("pick place red_block1:",success)
        if not success:
            return self.info
        success = self.pick_place_block(self.red_block2,self.plate)
        print("pick place red_block2:",success)
        if not success:
            return self.info
        success = self.pick_place_block(self.blue_block1,self.plate)
        print("pick place blue_block1:",success)
        if not success:
            return self.info
        
        success = self.pick_place_block(self.green_block1,self.plate)
        print("pick place green_block1:",success)
        if not success:
            return self.info
    
    def check_success(self):
        
        if self.check_on(self.red_block1, self.plate) and self.check_on(self.red_block2, self.plate) and self.check_on(self.blue_block1, self.plate) and self.check_on(self.green_block1, self.plate):
            return True
        return False

```


'''
