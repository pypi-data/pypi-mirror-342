import os, pygame, sys, ast, numpy
from taipan_imgfx import config # type: ignore

folder_name = config.filename

def save_file_naming(folder_name):
    """
    Finds available save file name within the given folder.
    Returns the next available by incrementing file number if needed.

    Args:
        folder_name (str): User's chosen folder to save file data to.

    Returns:
        str: Full path to the next available save file.
    """
    art_savefolder = os.path.expanduser(f"~/Desktop/{folder_name}")
    i = 1
    while os.path.exists(os.path.join(art_savefolder, f"save_list{i}.npy")):
        i += 1

    return os.path.join(art_savefolder, f"save_list{i}.npy")

def save(screen):
    """
    Saves an image pixel-by-pixel as a list of 5-item tuples.
    Each tuple contains RGB color data and x/y position, stored within a .txt file.
    These saved .npy files can be remade using taipan's load module.

    Args:
        screen (pygame.Surface): The pygame display surface.
    """
    save_arr = pygame.surfarray.array3d(screen)
    file_name = save_file_naming(folder_name)
    numpy.save(file_name, save_arr)

    print (f"Image saved file path {file_name}")



def load(screen, index=1):
    """
    Reconstructs the saved .npy file containing image data as an image under the filename + index name.
    Takes the newly reconstructed image and displays it on the pygame screen.

    Args:
        screen (pygame.Surface): The pygame display surface.
        index (int): The index value for which image to reconstruct. (default=1)
    """

    path = os.path.expanduser(f"~/Desktop/{folder_name}/save_list{index}.npy")

    if not os.path.exists(path):
        print(f"Err: File not found at {path}")

    image_arr = numpy.load(path)
    print(image_arr)

    image_load = pygame.surfarray.make_surface(image_arr)
    screen.blit(image_load, (0, 0))
    pygame.display.flip()

    print (f"Image loaded file path save_list{index}")
