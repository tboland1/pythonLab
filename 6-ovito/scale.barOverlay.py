from ovito.data import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Parameters:
bar_length = 40   # Simulation units (e.g. Angstroms)
bar_color = QColor(0,0,0)
label_text = "{} nm".format(bar_length/10)
label_color = QColor(255,255,255)

# This function is called by OVITO on every viewport update.
def render(painter, **args):
	if args['is_perspective']: 
		raise Exception("This only works with non-perspective viewports.")
		
	# Compute length of bar in screen space
	screen_length = 0.5 * bar_length * painter.window().height() / args['fov']

	# Define geometry of bar in screen space
	height = 0.07 * painter.window().height()
	margin = 0.02 * painter.window().height()
	rect = QRectF(margin, margin, screen_length, height)

	# Render bar
	painter.fillRect(rect, bar_color)

	# Render text label
	font = painter.font()
	font.setPixelSize(height)
	painter.setFont(font)
	painter.setPen(QPen(label_color))
	painter.drawText(rect, Qt.AlignCenter, label_text)
    
