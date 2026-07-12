x_norm = (x - x.min()) / (x.max() - x.min())
y_norm = (y - y.min()) / (y.max() - y.min())
z_norm = (z - z.min()) / (z.max() - z.min())

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.invert_zaxis()
ax.scatter(x_norm, y_norm, z_norm, s=5)
plt.show()

