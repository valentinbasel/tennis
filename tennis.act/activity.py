import os
import sys
#from pygame.locals import *

sys.path.insert(0, "lib")

import pygame
import pygame.camera
from pygame.locals import *
from olpcgames import activity
from gettext import gettext as _

class Activity(activity.PygameActivity):
    """Your Sugar activity"""
    
    game_name = 'run'
    game_title = _('tennis')
    game_size = None
