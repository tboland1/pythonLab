import matplotlib
import matplotlib.pyplot as plt
import PyQt5.QtGui
from ovito.modifiers import *

# Activate 'agg' backend for off-screen plotting.
matplotlib.use('Agg')

def render(painter, **args):

	# Find the existing HistogramModifier in the pipeline 
	# and get its histogram data.
	for mod in ovito.dataset.selected_node.modifiers:
		if isinstance(mod, HistogramModifier):
			x = mod.histogram[:,0]
			y = mod.histogram[:,1]
			break
	if not 'x' in locals():
		raise RuntimeError('Histogram modifier not found.')
	
	# Get size of rendered viewport image in pixels.
	viewport_width = painter.window().width()
	viewport_height = painter.window().height()
	
	#  Compute plot size in inches (DPI determines label size)
	dpi = 80
	plot_width = 0.5 * viewport_width / dpi
	plot_height = 0.5 * viewport_height / dpi
	
	# Create figure
	fig, ax = plt.subplots(figsize=(plot_width,plot_height), dpi=dpi)
	fig.patch.set_alpha(0.5)
	plt.title('Coordination')
	
	# Plot histogram data
	ax.bar(x, y)
	plt.tight_layout()
	
	# Render figure to an in-memory buffer.
	buf = fig.canvas.print_to_buffer()
	
	# Create a QImage from the memory buffer
	res_x, res_y = buf[1]
	img = PyQt5.QtGui.QImage(buf[0], res_x, res_y, PyQt5.QtGui.QImage.Format_RGBA8888)
	
	# Paint QImage onto rendered viewport 
	painter.drawImage(0,0,img)