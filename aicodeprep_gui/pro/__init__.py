"""Premium plugin loader."""
import os, sys
enabled = '--pro' in sys.argv or os.path.isfile('pro_enabled')
