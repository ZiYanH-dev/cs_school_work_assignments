import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x=['me','ss','zqq']
y=[1,3,5]

a=pd.Series([2,3,4],index=[1,3,5])

plt.plot(a)
plt.show()