from __future__ import annotations

from typing import List, Tuple
from numpy.typing import NDArray
from numpy import uint32

from .industrial_robots import Frame3


class Crx:
    """
    Class representing a FANUC CRX robot.
    """
    @property
    def z0(self) -> float:
        """
        The height from the bottom of the robot mounting flange to the world origin (located at the intersection of
        J2 and J1). This value isn't used in the kinematics, but is a value from the datasheet that is useful when
        placing the robot in a scene.
        """
        ...

    @property
    def z1(self) -> float:
        """
        The height from the J2 axis to the J3 axis. This is the kinematic length of the second link of the robot.
        """
        ...

    @property
    def x1(self) -> float:
        """
        The length from the J3 axis to the J5 axis.
        """
        ...

    @property
    def x2(self) -> float:
        """
        The length from the J5 axis to the robot flange.
        """
        ...

    @property
    def y1(self) -> float:
        """
        The y offset from the J1 & J3 axes to the J6 axis. This is the sideways offset of the wrist.
        """
        ...


    @staticmethod
    def new_5ia() -> Crx:
        """
        Create a new FANUC CRX 5ia robot.
        :return: a new instance of the FANUC CRX 5ia robot
        """
        ...

    @staticmethod
    def new_10ia() -> Crx:
        """
        Create a new FANUC CRX 10ia robot.
        :return: a new instance of the FANUC CRX 10ia robot
        """
        ...

    @staticmethod
    def fk(joints: List[float]) -> Frame3:
        """
        Compute the forward kinematics of the FANUC CRX robot.
        :param joints: a list of 6 FANUC joint angles in degrees, the way they would be entered into the controller
        :return: a Frame3 object representing the end-effector pose
        """
        ...

    def get_meshes(self) -> List[Tuple[NDArray[float], NDArray[uint32]]]:
        """
        Get the meshes of the FANUC CRX robot.
        :return: a list of tuples, each containing a numpy array of vertices and a numpy array of faces
        """
        ...

    def fk_all(self, joints: List[float]) -> List[Frame3]:
        """
        Compute the forward kinematics of the FANUC CRX robot with all links.
        :param joints: a list of 6 FANUC joint angles in degrees, the way they would be entered into the controller
        :return: a list of Frame3 objects representing the pose of each link, including the end-effector
        """
        ...
    
    def ik(self, target: Frame3) -> List[List[float]]:
        """
        Compute the inverse kinematics of the FANUC CRX robot.
        :param target: a Frame3 object representing the desired end-effector pose
        :return: a list of lists, each containing a list of 6 joint angles in degrees
        """
        ...