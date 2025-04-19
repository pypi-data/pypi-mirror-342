import pygame
from taipan_imgfx import color_convert, config # type: ignore
from math import sqrt
from taipan_imgfx.post_effects import post_image_effects # type: ignore

screen = config.screen
ScreenW = config.ScreenW
ScreenH = config.ScreenH


def clear(strength=240, check_range=2, fill=(0, 0, 0)):
    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            color = screen.get_at((x, y))

            r, g, b, a = color

            brightness = r + g + b
            brightness = min(brightness, 255)

            if brightness != 0:
                if brightness > strength or r > g - check_range and r < g + check_range and r > b - check_range and r < b + check_range:
                    r, g, b = fill[0], fill[1], fill[2]

                color = r, g, b, a
                screen.set_at((x, y), color)


    return True

def invert(Rstrength = 255, Gstrength = 255, Bstrength = 255):
    pygame.display.update()
    list_fill = []

    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            color = screen.get_at((x, y))
            r, g, b, a = color
            
            if (r, g, b) > (0, 0, 0):
                r = (Rstrength - r) 
                if r >= 0:
                    pass
                else:
                    r = 0

                g = (Gstrength - g)
                if g >= 0:
                    pass
                else:
                    g = 0

                b = (Bstrength - b)
                if b >= 0:
                    pass
                else:
                    b = 0

                color = (r, g, b, a)
                list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

    


def shift(Ta=(1, 1, 0), Tb=(1, 1, 0), Tc=(1, 1, 0), xstep=1, ystep=1, x_mov=0, y_mov=0): 
    pygame.display.update()
    list_fill = []

    for x in range(0, ScreenW, xstep):
        for y in range(0, ScreenH, ystep):
            color = screen.get_at((x, y))
            r, g, b, a = color
            if r + g + b != 0:
                xP = x + x_mov
                yP = y + y_mov

                color_max = max(r, g, b)

                if color_max == r:
                    if Ta[0]:
                        g = 255 - g
                        b = 255 - b
                    if Ta[1]:
                        if Ta[2] == 0:
                            xP -= r

                        if Ta[2] == 1:
                            xP -= g

                        if Ta[2] == 2:
                            xP -= b

                elif color_max == g:
                    if Tb[0]:
                        r = 255 - g
                        b = 255 - b
                    if Tb[1]:
                        if Tb[2] == 0:
                            yP += r

                        if Tb[2] == 1:
                            yP += g

                        if Tb[2] == 2:
                            yP += b
                        

                elif color_max == b:
                    if Tc[0]:
                        r = 255 - g
                        g = 255 - b
                    if Tc[1]:
                        if Tc[2] == 0:
                            yP -= r

                        if Tc[2] == 1:
                            yP -= g

                        if Tc[2] == 2:
                            yP -= b
                        

                color = r, g, b, a

                list_fill.append(((xP, yP), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

def contrast(low_thresh=400, high_thresh=665, exr=0, exg=0, exb=0, coloriser=(255, 255, 255, 255), neg_coloriser=(0, 0, 0)):
    list_fill = []

    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            color = screen.get_at((x, y))

            r, g, b, a = color

            if exr:
                r = neg_coloriser[0]
            if exg:
                g = neg_coloriser[1]
            if exb:
                b = neg_coloriser[2]

 
            if (r + g + b) > low_thresh and (r + g + b) < high_thresh:
                color = coloriser

            elif (r + g + b) > 0:
                color = neg_coloriser

            list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

def edge(threshold=50, fillcolor=(255, 255, 255), endcolor=(0, 0, 0)):
    pygame.display.update()

    list_fill = []

    for x in range(1, ScreenW -1, 1):
        for y in range(1, ScreenH - 1, 1):
            
            Ucolor = screen.get_at((x, y - 1))
            Ur, Ug, Ub = Ucolor[:3]
            Uc = post_image_effects.greyscale(Ur, Ug, Ub)

            Dcolor = screen.get_at((x, y))
            Dr, Dg, Db = Dcolor[:3]
            Dc = post_image_effects.greyscale(Dr, Dg, Db)

            Lcolor = screen.get_at((x, y))
            Lr, Lg, Lb = Lcolor[:3]
            Lc = post_image_effects.greyscale(Lr, Lg, Lb)

            Rcolor = screen.get_at((x, y))
            Rr, Rg, Rb = Rcolor[:3]
            Rc = post_image_effects.greyscale(Rr, Rg, Rb)

            if Uc == 0 and Dc == 0 and Lc == 0 and Rc == 0:
                pass
            
            else:
                x_difference = Lc - Rc
                y_difference = Uc - Dc

                magnitude = sqrt(x_difference ** 2 + y_difference ** 2)
                
                if magnitude > threshold:
                    list_fill.append(((x,y), (fillcolor)))
                else:
                    list_fill.append(((x,y), (endcolor)))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

def old_edge(acceptance=1, fillcolor=(255, 255, 255), neg_fillcolor=(0, 0, 0), seperate_black=1):
    pygame.display.update()

    list_fill = []

    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            Mcolor = screen.get_at((x, y))
            correct = 0
            Mcolor = list(Mcolor)
            Mcolor = sum(Mcolor)

            try:
                Lcolor = screen.get_at((x - 1, y))
                Lcolor = list(Lcolor)
                Lcolor = sum(Lcolor)
                if Mcolor > (Lcolor - acceptance) and Mcolor < (Lcolor + acceptance):
                    correct += 1
            except IndexError:
                pass

            try:
                Rcolor = screen.get_at((x + 1, y))
                Rcolor = list(Rcolor)
                Rcolor = sum(Rcolor)
                if Mcolor > (Rcolor - acceptance) and Mcolor < (Rcolor + acceptance):
                    correct += 1
            except IndexError:
                pass
            
            try:
                Ucolor = screen.get_at((x, y + 1))
                Ucolor = list(Ucolor)
                Ucolor = sum(Ucolor)
                if Mcolor > (Ucolor - acceptance) and Mcolor < (Ucolor + acceptance):
                    correct += 1
            except IndexError:
                pass

            try:
                Dcolor = screen.get_at((x, y - 1))
                Dcolor = list(Dcolor)
                Dcolor = sum(Dcolor)
                if Mcolor > (Dcolor - acceptance) and Mcolor < (Dcolor + acceptance):
                    correct += 1
            except IndexError:
                pass
            

            if correct != 4 and correct != 0:
                if Mcolor == 255 and seperate_black:
                    list_fill.append(((x, y), (0, 0, 0)))
                else:
                    list_fill.append(((x, y), (fillcolor)))


            else:
                if Mcolor == 255 and seperate_black:
                    list_fill.append(((x, y), (0, 0, 0)))
                else:
                    list_fill.append(((x, y), (neg_fillcolor)))

    for pos, color in list_fill:
        screen.set_at(pos, color)

def channelise(Hrotate=(0, 0), Sclear=(0, 0, 0), Lclear=(0, 0, 0) ):

    fill_list = []
    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            red, green, blue, a = screen.get_at((x, y))

            if max(red, green, blue) != 0:
                h, s, l = color_convert.hsl_convert(red, green, blue)

                if Hrotate[0]:
                    h = (h + Hrotate[1]) % 360

                if Sclear[0]:
                    if Sclear[2]:
                        if s >= Sclear[1]:
                            s -= Sclear[1]
                        else:
                            s = 0
                    elif Sclear[2] == 2:
                        if (s + Sclear[1]) <= 100:
                            s += Sclear[1]
                        else:
                            s = 100


                if Lclear[0]:
                    if Lclear[2]:
                        if l >= Lclear[1]:
                            l -= Lclear[1]
                        else:
                            l = 0
                    elif Lclear[2] == 2:
                        if (l + Lclear[1]) <= 100:
                            l += Lclear[1]
                        else:
                            l = 100


                red, green, blue = color_convert.RGB_convert(h, s, l)

                fill_list.append(((x, y), (red, green, blue, a)))


    for position, color in fill_list:
        screen.set_at(position, color)

def extractor(Popr=0,Popg=0,Popb=0, typing=0, Rstrength=0, Gstrength=0, Bstrength=0, fill_color=(0, 0, 0), Rcheck=(1, 0, 0), Gcheck=(1, 0, 0), Bcheck=(1, 0, 0)):
    pygame.display.update()

    list_fill = []

    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            color = screen.get_at((x, y))
            r, g, b, a = color
            
            if typing == 0:
                if Popr and r > Rstrength:
                    r = fill_color[0]
                    
                if Popg and g > Gstrength:
                    g = fill_color[1]

                if Popb and b > Bstrength:
                    b = fill_color[2]

                color = r, g, b, a

            elif typing:
                if Popr:
                    if Rcheck[0]:
                        if r > Rstrength:
                            color = fill_color
                    
                    elif Rcheck[1]:
                        if r == Rstrength:
                            color = fill_color

                    elif Rcheck[2]:
                        if r < Rstrength and r > 0:
                            color = fill_color
                    
                if Popg:
                    if Gcheck[0]:
                        if g > Rstrength:
                            color = fill_color
                    
                    elif Gcheck[1]:
                        if g == Rstrength:
                            color = fill_color

                    elif Gcheck[2]:
                        if g < Rstrength and g > 0:
                            color = fill_color

                if Popb:
                    if Bcheck[0]:
                        if b > Rstrength:
                            color = fill_color
                    
                    elif Bcheck[1]:
                        if b == Rstrength:
                            color = fill_color

                    elif Bcheck[2]:
                        if b < Rstrength and b > 0:
                            color = fill_color


            list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)
        

def converge(Conr=0, Cong=0, Conb=0, strength=255):
    pygame.display.update()

    list_fill = []

    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenH, 1):
            color = screen.get_at((x, y))
            r, g, b, a = color

            brightness = r + g + b
            if brightness != 0:
                norm_brightness = min((brightness / strength), 1)
                norm_brightness *= strength
                norm_brightness = int(norm_brightness)
                
                if Conr == 1:
                    r = norm_brightness
                    g, b = 0, 0

                elif Cong == 1:
                    g = norm_brightness
                    r, b = 0, 0

                elif Conb == 1:
                    b = norm_brightness
                    r, g = 0, 0


            color = r, g, b, a

            list_fill.append(((x, y), (color)))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

    pygame.display.update()

def splice_overlay(color2=(160, 80, 220), width=10):

    increment = 0
    on = True

    list_fill = []
    for x in range(0, ScreenW, 1):
        if increment == width:
            on = not on
            increment = 0

        else:
            increment += 1

        for y in range(0, ScreenH, 1):
            if on:
                    color = color2
            else:
                color = screen.get_at((x, y))

            if screen.get_at((x, y)) != (0, 0, 0, 255):
                list_fill.append(((x, y), (color)))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

    pygame.display.update()


def flatten(Rthresh=100, Gthresh=100, Bthresh=100, Rcheck=1, Gcheck=1, Bcheck=1, strength=10):
    list_fill = []
    for x in range(0, ScreenW, 1):
        for y in range(0, ScreenW, 1):
            r, g, b, _ = screen.get_at((x, y))

            if (r, g, b) != (0, 0, 0):
                if r < Rthresh and Rcheck:
                    r += strength

                if g < Gthresh and Gcheck:
                    g += strength

                if b < Bthresh and Bcheck:
                    b += strength

            if r > 255:
                r = 255

            elif r < 0:
                r = 0

            if g > 255:
                g = 255

            elif g < 0:
                g = 0

            if b > 255:
                b = 255

            elif b < 0:
                b = 0

                
            color = r, g, b
            list_fill.append(((x, y), color))

    screen.fill((0, 0, 0))
    for pos, color in list_fill:
        screen.set_at(pos, color)

    pygame.display.update()
