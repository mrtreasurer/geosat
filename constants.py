import numpy as np


class MeerLicht:
    def __init__(self):
        # bloemen et al.
        self.fov = np.radians(2.7)  # rad
        self.pixels = 10560  # px

        self.fov_pp = 0.56 * np.pi/(180*3600)  # rad/px

        self.shutter_t = 60  # s
        self.shutter_dt = 1  # s

        self.coors = np.array([-32.379794, 20.811259])  # deg. ref: maps.google.com
        self.coors_rad = np.radians(self.coors)


class Earth:
    def __init__(self):
        # ocdm
        self.mu = 3.98600441e5  # km3s-2
        self.r = 6378.136  # km

        self.p_sidereal = 86164.1004  # s


    def vec_from_coors(self, coors):
        coors = np.radians(coors)
        sin_coors = np.sin(coors)
        cos_coors = np.cos(coors)

        pos = np.array([self.r * cos_coors[0] * cos_coors[1],
                        self.r * cos_coors[0] * sin_coors[1],
                        self.r * sin_coors[0]])

        return pos


telescope = MeerLicht()
earth = Earth()