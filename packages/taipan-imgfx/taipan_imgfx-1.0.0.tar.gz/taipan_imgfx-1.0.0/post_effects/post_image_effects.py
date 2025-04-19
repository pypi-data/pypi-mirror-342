import pygame, math
from taipan_imgfx import config # type: ignore

screen = config.screen
ScreenW = config.ScreenW
ScreenH = config.ScreenH

def exposure(intensity=1.2, Rcheck=1, Gcheck=1, Bcheck=1, step=(0, 0, 1)):
    pygame.display.update()

    list_fill = []

    if step[0]:
        step_flag = 0
        on = True

        for x in range(0, ScreenW, 1):
            if step_flag == step[1]:
                on = not on
                step_flag = 0
            
            else:
                step_flag += 1

            for y in range(0, ScreenH, 1):
                r, g, b, a = screen.get_at((x, y))

                if r + g + b != 0:
                    if on:
                        if Rcheck:
                            r = int(min(r * intensity, 255))

                        if Gcheck:
                            g = int(min(g * intensity, 255))

                        if Bcheck:
                            b = int(min(b * intensity, 255))

                    elif step[2] != 1 and step[2] > 0:
                        if step[2] < 1:
                            if Rcheck:
                                r = int(min(r * step[2], 255))

                            if Gcheck:
                                g = int(min(g * step[2], 255))

                            if Bcheck:
                                b = int(min(b * step[2], 255))
                        elif step[2] > 1:
                            if Rcheck:
                                r = int(min(r * step[2], 255))

                            if Gcheck:
                                g = int(min(g * step[2], 255))

                            if Bcheck:
                                b = int(min(b * step[2], 255))


                    list_fill.append(((x, y), (r, g, b)))

    else:
        for x in range(0, ScreenW, 1):
            for y in range(0, ScreenH, 1):
                r, g, b, a = screen.get_at((x, y))

                if r + g + b != 0:
                    if Rcheck:
                        r = int(min(r * intensity, 255))

                    if Gcheck:
                        g = int(min(g * intensity, 255))

                    if Bcheck:
                        b = int(min(b * intensity, 255))

                    list_fill.append(((x, y), (r, g, b)))

    
    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

    pygame.display.update()

def greyscale(r, g, b):
    r *= 0.3
    g *= 0.6
    b *= 0.1
    return r + g + b

def flattening(redfill=0, greenfill=0, bluefill=0, Rc=0, Gc=0, Bc=0):
    list_fill = []
    exposure(0.1, Rc, Gc, Bc)

    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            color = screen.get_at((x, y))

            r, g, b, a = color

            brightest = max(r, g, b)

            if brightest != 0 and (r, g, b) != (255, 255, 255):
                if brightest == r:
                    g = greenfill
                    b = bluefill
                
                elif brightest == g:
                    r = redfill
                    b = bluefill
                
                elif brightest == b:
                    r = redfill
                    g = greenfill

                color = (r, g, b)


                list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

def band_color_dist(color1, color2):
    distance = (color1[0] - color2[0]) ** 2
    distance += (color1[1] - color2[1]) ** 2
    distance += (color1[2] - color2[2]) ** 2
    distance = math.sqrt(distance)
    return distance

def banding(acceptance=10, initRband=(255, 0, 0), initGband=(0, 255, 0), initBband=(0, 0, 255)):
    list_fill = []
    bands = [initRband, initGband, initBband]

    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            r, g, b, _ = screen.get_at((x, y))
            origin = r, g, b

            if origin == (0, 0, 0):
                continue
            
            matched_flag = False
            for bandC in bands:
                if band_color_dist((r, g, b), (bandC)) < acceptance:
                    r, g, b = bandC
                    matched_flag = True
                    break

            if matched_flag != True:
                bands.append((origin))

            color = r, g, b
            list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

def grid(x, y):
    color_matrix = []
    color_matrix.append(screen.get_at((x - 1, y - 1)))
    color_matrix.append(screen.get_at((x, y - 1)))
    color_matrix.append(screen.get_at((x + 1, y - 1)))
    color_matrix.append(screen.get_at((x - 1, y)))
    color_matrix.append(screen.get_at((x, y)))
    color_matrix.append(screen.get_at((x + 1, y)))
    color_matrix.append(screen.get_at((x - 1, y + 1)))
    color_matrix.append(screen.get_at((x, y + 1)))
    color_matrix.append(screen.get_at((x + 1, y + 1)))
    return color_matrix

def blur():
    list_fill = []
    
    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            try:
                color_matrix = grid(x, y)
                avg_red = 0
                for i in range(9):
                    avg_red += color_matrix[i][0]

                avg_red //= len(color_matrix)

                avg_green = 0
                for i in range(9):
                    avg_green += color_matrix[i][1]

                avg_green //= len(color_matrix)

                avg_blue = 0
                for i in range(9):
                    avg_blue += color_matrix[i][2]

                avg_blue //= len(color_matrix)

                color = avg_red, avg_green, avg_blue
            
            except IndexError:
                color = screen.get_at((x, y))

            list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

def lighten(thresh, strength, Rcheck=(1, 1), Gcheck=(1, 1), Bcheck=(1, 1)):
    list_fill = []
    
    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            r, g, b, _ = screen.get_at((x, y))

            if Rcheck[1] == 1 and Gcheck[1] == 1 and Bcheck[1] == 1:
                brightness = r + g + b

            else:
                brightness = 0

                if Rcheck[1] == 1:
                    brightness += r

                if Gcheck[1] == 1:
                    brightness += g

                if Bcheck[1] == 1:
                    brightness += b

            if brightness < thresh and brightness != 0:
                if Rcheck[0]:
                    r = int(min(r * strength, 255))

                if Gcheck[0]:
                    g = int(min(g * strength, 255))

                if Bcheck[0]:
                    b = int(min(b * strength, 255))



            color = r, g, b

            list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)


def posterisation(initband=config.palette):

    list_fill = []

    for x in range(ScreenW):
        for y in range(ScreenH):
            r, g, b, _ = screen.get_at((x, y))

            if (r, g, b) != (0, 0, 0):
                shortest_dist = (float('inf'), 0)

                for band in initband:
                    dist = band_color_dist((r, g, b), (band))
                    if dist < shortest_dist[0]:
                        shortest_dist = (dist, band)
                    

                r, g, b = shortest_dist[1]

                color = r, g, b

                list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)


def delete(savecolors, fillcolor=(0, 0, 0)):

    list_fill = []

    for x in range(ScreenW):
        for y in range(ScreenH):
            r, g, b, _ = screen.get_at((x, y))
            
            if r + g + b == 0:
                if (r, g, b) not in savecolors:
                    color = fillcolor
                    list_fill.append(((x, y), color))

                else:
                    color = r, g, b
                    list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)


            

