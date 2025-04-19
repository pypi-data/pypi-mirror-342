import pygame, tkinter
from taipan_imgfx import config

pygame.init()

user_choice = 0
if user_choice:
    image_index = int(input("Pick an image type, -1 if you wan't to load saved images.")), int(input("Pick 0 for non saving or 1 for saving."))
else:
    image_index = 11, 0

config.ScreenW, config.ScreenH = 800, 800
config.screen = pygame.display.set_mode((config.ScreenW, config.ScreenH))

from taipan_imgfx.utils import fileman, image
from taipan_imgfx.bundles import effect_bundles as bundles
from taipan_imgfx.effects import image_effects as effects
from taipan_imgx.post_effects import post_image_effects as post_effects

if image_index[0] == -1:
    fileman.load(config.screen, int(input("Pick an available save path index.\n>")))

image.preset_image_loading(image_index, config.screen)
    
'''-----Running image effects-----'''
effects.clear(255)
bundles.CASCADE(0)
'''-----Running image effects-----'''

'''-----Image display-----'''
image.display(image_index)
'''-----Image display-----'''
