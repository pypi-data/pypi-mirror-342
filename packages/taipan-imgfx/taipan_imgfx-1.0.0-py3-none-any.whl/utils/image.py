import pygame, os, sys
from taipan_imgfx.utils import fileman # type: ignore
from taipan_imgfx import config # type: ignore

screen = config.screen
ScreenW = config.ScreenW
ScreenH = config.ScreenH

def display(image_count):
    """
    Holds the pygame window open until user quits.
    Includes optional image saving behaviour using taipan's fileman module.

    Args:
        image_count (tuple): A tuple like (image_number, save_enabled)
            - image_number (int): An image counter. If >= 0, allows saving. if < 0, treated as admin/debug behavior.
            - save_enabled (bool): If True, prompts to save on exit.
        SW (int): Display window width in pixels.
        SH (int): Display window height in pixels.
        screen (pygame.Surface): The pygame display surface.
    """
    running = True

    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                if image_count[0] >= 0 and image_count[1] == 1:
                    if input("input (y) if you want to save this image.").lower() == "y":
                        fileman.save(screen)
                running = False

        pygame.display.update()

def preset_image_loading(image_index, screen):
    """
    Takes a user index to choose an image to display one of the image presets on the pygame display.
    Intended for taipan admin only.

    Args:
        image_index (int): The index at which the image to display is chosen.
        screen (pygame.Surface): The pygame display surface.
    """

    image_folder = [
    'SurfaceW1.webp', 'SurfaceW2.webp', 'SurfaceW3.webp', 'SurfaceW4.webp',
    'SurfaceW5.webp', 'SurfaceW6.jpg', 'SurfaceW7.webp', 'SurfaceW8.jpeg',
    'SurfaceW9.webp', 'SurfaceW10.webp', 'SurfaceW11.webp', 'SurfaceW12.jpg',
    'SurfaceW13.webp', 'SurfaceW14.webp', 'SurfaceW15.webp', 'SurfaceW16.webp',
    'SurfaceW17.png', 'SurfaceW18.jpg', 'SurfaceW19.jpeg', 'SurfaceW20.webp',
    'SurfaceW21.webp', 'SurfaceW22.webp', 'SurfaceW23.webp', 'SurfaceW24.webp',
    'SurfaceW25.webp', 'SurfaceW26.webp', 'SurfaceW27.webp', 'SurfaceW28.webp',
    'SurfaceW29.png'
    ]   
    
    special_positions = {
           7: (0, 0),
           16: (160, 40),
           28: (200, 20)
    }
    if image_index[0] >= 0 and image_index[0] < len(image_folder):
        try:
            background = pygame.image.load(f"/Users/home/Desktop/Python/taipan/images/{image_folder[image_index[0]]}").convert_alpha()
            pos = (200, 200) if image_index[0] not in special_positions else special_positions[image_index[0]]
            screen.blit(background, (pos))
            pygame.display.flip()

        except Exception as excepted:
            print (f"Image error ~/{excepted}, {image_index[0]}")

    
    else:
        print (f"Non-valid image index {image_index}")

    

