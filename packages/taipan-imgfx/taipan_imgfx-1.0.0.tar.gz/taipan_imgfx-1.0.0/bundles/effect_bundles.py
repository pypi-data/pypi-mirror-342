from taipan_imgfx.effects import image_effects as effects # type: ignore
from taipan_imgfx.post_effects import post_image_effects as post_effects # type: ignore
from taipan_imgfx import config # type: ignore


screen = config.screen
ScreenW = config.ScreenW
ScreenH = config.ScreenH



def BAW():
    effects.converge(1, 0, 0)
    effects.clear(254)
    effects.contrast(100, 755)


def CCS(typing=1):
    if typing == 1:
        effects.clear(220, 5)
        effects.converge(1, 0, 0, 150)
    if typing == 2:
        effects.clear(220, 5)
        effects.converge(0, 1, 0, 150)
    if typing == 3:
        effects.clear(220, 5)
        effects.converge(0, 0, 1, 150)

    effects.clear()
    effects.shift((0, 1, 0), (0, 1, 0), (0, 1, 0))
        


def BAWSC():
    BAW()
    effects.converge(1, 0, 0, 255)
    effects.contrast(100, 765, 0, 0, 1, (170, 30, 50), (100, 0, 0))
    effects.extractor(1, 0, 0, 1, 100, 0, 0, (70, 130, 200), (0, 1, 0))

def CREAMSPLICE():
    effects.splice_overlay()
    BAWSC()
    effects.old_edge(1, (170, 30, 80), (169, 169, 169), 0)

def OXPOP(step=2):
    effects.converge(1, 0, 0, 150)
    effects.shift((0, 1, 0), (1, 1, 1), (1, 1, 1), step, step, 50, 0)
    post_effects.exposure(1.6)

def GRIS():
    for x in range(1, ScreenW, 1):
        for y in range(1, ScreenW, 1):
            r, g, b, a = screen.get_at((x, y))
            grey = post_effects.greyscale(r, g, b)
            r = grey // 3
            g = grey // 3
            b = grey // 3

            screen.set_at((x,y), (r, g, b))

def PEASOUP(edge_power):
    effects.clear()
    OXPOP(1)
    effects.edge(edge_power, (120, 60, 113))
    effects.shift((1, 1, 2), (0, 1, 2), (1, 0, 1), 1, 1, 150)

def FREWM(strength=1):
    effects.clear(255, strength)
    GRIS()
    post_effects.exposure(1.8)

def GLAST(Xmov, Ymov):
    effects.clear(255, 2)
    effects.shift((1, 0, 0), (1, 1, 0), (1, 1, 0), 1, 1, Xmov, Ymov)
    effects.channelise((1, 50))

def GEM(strength=1):
    FREWM(strength)
    effects.shift((1, 0, 0), (1, 0, 0), (1, 0, 0))
    effects.invert(200, 200, 100)
    effects.extractor(1, 0, 0, 0, 100, 0, 0, (0, 0,0), (1, 0, 0), (1, 0, 0), (1, 0, 0))

def CAST(band_acc=150):
    effects.clear(255)
    GRIS()
    effects.banding(band_acc, (200, 50, 50), (50, 200, 50), (50, 50, 200))

def REBLUR(n):
    for i in range(n):
        effects.blur()
        print(f"Blur {i + 1}/{n} finished")

def CASCADE(clearflag=1):
    if clearflag:
        effects.clear()
    effects.shift((0, 1, 0), (0, 1, 0), (0, 1, 0))
    post_effects.exposure()

def SHARD(Hshift=50):
    effects.clear(255)
    effects.channelise((1, Hshift))
    post_effects.posterisation()
    effects.invert()
    effects.shift((1, 1, 0), (1, 1, 0), (1, 1, 0), 1, 1, 20, 40)
