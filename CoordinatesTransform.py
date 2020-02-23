import numpy as np


class CoordinatesTransform:

    def __init__(self, robot):

        # calibration markers robot TCP coordinates
        if robot == "UR1":
            self.manipulator_coords = np.array(
                                            [[249.30, -331.41, 1.0],
                                             [58.27, -315.65, 1.0],
                                             [-136.04, -298.05, 1.0],
                                             [-300.43, -287.97, 1.0],
                                             [257.87, -555.45, 1.0],
                                             [32.20, -536.59, 1.0],
                                             [-138.65, -509.47, 1.0],
                                             [-309.70, -500.67, 1.0],
                                             [238.51, -787.17, 1.0],
                                             [30.29, -773.24, 1.0],
                                             [-150.10, -756.81, 1.0],
                                             [-320.63, -760.86, 1.0]]
                                                )
        if robot == "UR2":
            self.manipulator_coords = np.array(
                                            [[-314.23, -743.52, 1.0],
                                             [-122.58, -745.47, 1.0],
                                             [76.11, -750.45, 1.0],
                                             [243.54, -751.36, 1.0],
                                             [-335.00, -521.99, 1.0],
                                             [-108.48, -527.24, 1.0],
                                             [64.47, -543.19, 1.0],
                                             [237.05, -542.36, 1.0],
                                             [-329.52, -293.06, 1.0],
                                             [-121.41, -293.40, 1.0],
                                             [59.73, -299.27, 1.0],
                                             [231.16, -286.80, 1.0]]
                                              )

        # calibration markers image coordinates
        self.image_coords = np.array(
                                [[1106, 829, 1.0],
                                 [1114, 630, 1.0],
                                 [1125, 423, 1.0],
                                 [1131, 246, 1.0],
                                 [876, 845, 1.0],
                                 [887, 610, 1.0],
                                 [909, 428, 1.0],
                                 [912, 245, 1.0],
                                 [633, 835, 1.0],
                                 [639, 617, 1.0],
                                 [650, 423, 1.0],
                                 [638, 240, 1.0]]
                                )

    def coords_conversion(self, coords): #conversion from image coordinates to robot coordinates

        coords = coords
        image_coords = np.transpose(self.image_coords)
        manipulator_coords = np.transpose(self.manipulator_coords)

        M = np.matmul(manipulator_coords, np.linalg.pinv(image_coords, rcond=1e-15)) #transformation matrix
        robot_coords = np.matmul(M, [coords[0], coords[1], 1])

        return (robot_coords[0],robot_coords[1])