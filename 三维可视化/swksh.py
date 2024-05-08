import scipy.io

file_path = 'cy_walk_kinect_4.mat'
mat = scipy.io.loadmat(file_path)

# 输出读取的数据
x = mat['x_range'][0]
z = mat['z_range'][0]
depth = mat['depth'][0]

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 假设的x, y, z数据，你可以替换成你的具体数据
x = x[:61]
y = z[:61]
z = depth[:61]


fig = plt.figure(figsize=(16, 12))

# 三维散点图，占用左侧较大空间
ax1 = fig.add_subplot(2, 2, (1, 3), projection='3d')
ax1.scatter(x, y, z)
ax1.set_title('3D Scatter Plot')
ax1.set_xlabel('X axis')
ax1.set_ylabel('Y axis')
ax1.set_zlabel('Z axis')

# 二维散点图XY，占用右侧上方小部分空间
ax2 = fig.add_subplot(4, 2, 2)
ax2.scatter(x, y)
ax2.set_title('2D Scatter Plot XY')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')

# 二维散点图YZ，占用右侧中部小部分空间
ax3 = fig.add_subplot(4, 2, 4)
ax3.scatter(y, z)
ax3.set_title('2D Scatter Plot YZ')
ax3.set_xlabel('Y')
ax3.set_ylabel('Z')

# 二维散点图XZ，占用右侧下方小部分空间
ax4 = fig.add_subplot(4, 2, 6)
ax4.scatter(x, z)
ax4.set_title('2D Scatter Plot XZ')
ax4.set_xlabel('X')
ax4.set_ylabel('Z')

# 调整布局
plt.tight_layout()
plt.show()


