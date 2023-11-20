from hyper.transforms import PolarTransform
import numpy as np

ori = PolarTransform(0, 0, 0)
my_trans = PolarTransform(2*np.pi/5, 1.255, np.pi)
ori.step(my_trans.s)
# print(my_trans.to_string())
# print(np.arctan2(0, -1))
