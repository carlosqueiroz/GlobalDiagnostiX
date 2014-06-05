"""
based on code from http://www.frantzmartinache.com/blog/?p=84
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
#~ import time

plt.ion()


def add_lens(z, f, diam, lbl):
    # simply draws a thin-lens at the provided location parameters:
    # - z:    location along the optical axis (in mm)
    # - f:    focal length (in mm, can be negative if div. lens)
    # - diam: lens diameter in mm
    # - lbl:  label to identify the lens on the drawing
    ww, tw, rad = diam / 10.0, diam / 3.0, diam / 2.0
    plt.plot([z, z],    [-rad, rad],                'k', linewidth=2)
    #~ plt.plot([z, z + tw], [-rad, -rad + np.sign(f) * ww], 'y', linewidth=2)
    #~ plt.plot([z, z - tw], [-rad, -rad + np.sign(f) * ww], 'y', linewidth=2)
    #~ plt.plot([z, z + tw],  [rad,  rad - np.sign(f) * ww], 'y', linewidth=2)
    #~ plt.plot([z, z - tw],  [rad,  rad - np.sign(f) * ww], 'y', linewidth=2)
    plt.plot([z + f, z + f], [-ww, ww], 'y', linewidth=2)
    plt.plot([z - f, z - f], [-ww, ww], 'y', linewidth=2)
    lens = patches.Ellipse((z, 0), width=2 * f, height=diam,
                           facecolor='y', linewidth=2, alpha=0.125)
    plt.gcf().gca().add_patch(lens)
    plt.text(z, rad + 5.0, lbl, fontsize=12)
    plt.text(z, rad + 2.0, 'f=' + str(int(f)), fontsize=10)


def propagate_beam(p0, NA, nr, zl, ff, lbl='', col='b'):
    # geometrical propagation of light rays from given source parameters:
    # - p0:  location of the source (z0, x0) along and off axis (in mm)
    # - NA:  numerical aperture of the beam (in degrees)
    # - nr:  number of rays to trace
    # - zl:  array with the location of the lenses
    # - ff:  array with the focal length of lenses
    # - lbl: label for the nature of the source
    # - col: color of the rays on plot
    apa = NA * np.pi / 180.0
    z0 = p0[0]
    if (np.size(p0) == 2):
        x0 = p0[1]
    else:
        x0 = 0.0

    zl1, ff1 = zl[(z0 < zl)], ff[(z0 < zl)]
    nl = np.size(zl1)  # number of lenses

    zz, xx, tani = np.zeros(nl + 2), np.zeros(nl + 2), np.zeros(nl + 2)
    tan0 = np.tan(apa / 2.0) - np.tan(apa) * np.arange(nr) / (nr - 1)

    for i in range(nr):
        tani[0] = tan0[i]  # initial incidence angle
        zz[0], xx[0] = z0, x0
        for j in range(nl):
            zz[j + 1] = zl1[j]
            xx[j + 1] = xx[j] + (zz[j + 1] - zz[j]) * tani[j]
            tani[j + 1] = tani[j] - xx[j + 1] / ff1[j]

        zz[nl + 1] = zmax
        xx[nl + 1] = xx[nl] + (zz[nl + 1] - zz[nl]) * tani[nl]
        plt.plot(zz, xx, col)

FOVSize = np.array([430 / 3., 430 / 4.])

# AR130
# Full Resolution: 1280H x 960V (1.2Mp)
# Pixel Size: 3.75um x 3.75um

# AR132
# Full Resolution: 1280H x 960V (1.2Mp)
# Pixel Size: 3.75um x 3.75um

# MT9M001
# Active pixels: 1,280H x 1,024V
# Pixel size: 5.2um x 5.2um

pixelsize = 5.2 / 1000
CMOSSize = np.array([1280 * pixelsize, 1024 * pixelsize])

Magnification = FOVSize / CMOSSize

# Draw the different sizes.
figure1 = plt.figure()
plt.title("Sizes, head on")
plt.show()

Scintillator = patches.Rectangle((0, 0), 430, 430, facecolor='g', linewidth=2)
figure1.gca().add_patch(Scintillator)
for x in range(3):
    for y in range(4):
        # Draw rectangles: http://is.gd/rmDuV1
        FOV = patches.Rectangle((x * FOVSize[0], y * FOVSize[1]),
                                width=FOVSize[0], height=FOVSize[1],
                                facecolor='g', linewidth=2)
        figure1.gca().add_patch(FOV)
        Ellipse = patches.Ellipse((FOVSize[0] / 2 - CMOSSize[0] / 2 + x *
                                  FOVSize[0], FOVSize[1] / 2 -
                                  CMOSSize[1] / 2 + y * FOVSize[1]),
                                  width=FOVSize[0] / 0.618,
                                  height=FOVSize[1] / 0.618, color='k',
                                  alpha=0.125)
        figure1.gca().add_patch(Ellipse)
        CMOS = patches.Rectangle((FOVSize[0] / 2 - CMOSSize[0] / 2 + x *
                                  FOVSize[0], FOVSize[1] / 2 -
                                  CMOSSize[1] / 2 + y * FOVSize[1]),
                                 width=CMOSSize[0], height=CMOSSize[1],
                                 facecolor='b', linewidth=2)
        figure1.gca().add_patch(CMOS)
# Draw one more so we can get labels
FOV = patches.Rectangle((0, 0), FOVSize[0], FOVSize[1], facecolor='g',
                        linewidth=2, label='FOV')
figure1.gca().add_patch(FOV)
Ellipse = patches.Ellipse((FOVSize[0] / 2 - CMOSSize[0] / 2,
                           FOVSize[1] / 2 - CMOSSize[1] / 2),
                          width=FOVSize[0] / 0.618, height=FOVSize[1] / 0.618,
                          color='k', alpha=0.125, label='Opt. Circle')
figure1.gca().add_patch(Ellipse)
CMOS = patches.Rectangle((FOVSize[0] / 2 - CMOSSize[0] / 2,
                          FOVSize[1] / 2 - CMOSSize[1] / 2), CMOSSize[0],
                         CMOSSize[1], facecolor='b', linewidth=2, label='CMOS')
figure1.gca().add_patch(CMOS)
plt.legend()
plt.axis('scaled')
plt.xlabel('Length [mm]')
plt.ylabel('Length [mm]')
plt.savefig("lens_simulation_sizecomparison.png")

# www.physicsclassroom.com/class/refrn/Lesson-5/The-Mathematics-of-Lenses
# The magnification equation relates the ratio of the image distance and
# object distance to the ratio of the image height (hi) and object height
# (ho). The magnification equation is stated as follows:
# 1/f = 1/do + 1/di
# M = hi/ho = - di/do

CMOSPosition = 10.
FOVPosition = Magnification[0] * CMOSPosition
FocalLength = 1 / ((1 / CMOSPosition) + (1 / FOVPosition))


print 80 * '-'
print 'For a single FOV of', round(FOVSize[0], 2), 'x', \
    round(FOVSize[1], 2), 'mm and a CMOS size of', round(CMOSSize[0], 2), \
    'x', round(CMOSSize[1], 2), 'mm, we get a demagnification of', \
    round(Magnification[0], 2), 'x', round(Magnification[1], 2)
print 'If the CMOS is', CMOSPosition, 'mm away from the lens, the',\
    'Scintillator had to be', round(FOVPosition), 'mm away from the lens.'
print 'This means that the total optical length is', \
    round(CMOSPosition + FOVPosition), 'mm'
print 'Since the CMOS is', CMOSPosition, 'mm away from the lens we thus',\
    'get a focal length of of the lens of approximately', round(FocalLength, 2)

#~ Lens
# Draw the lens at the origin, to simplify things
LensPosition = np.array([0])
# Since we only draw *one* lens for the moment, we convert the focal length
# calculated above to a NumPy array, so we can use the drawing code
FocalLength = np.array([FocalLength])
#~ FNumber = FocalLength / LensDiameter
#~ FNumber = 1 / ( 2 * NumericalAperture)
#~ -> 1 / ( 2 * FNumber) = NumericalAperture
FNumber = 1.4
NumericalAperture = 1 / (2 * FNumber)

figure2 = plt.figure()
plt.show()
# Draw top view
plt.subplot(121)
plt.title("top view")
# Draw CMOS and Scintillator
plt.plot((-CMOSPosition, -CMOSPosition), (-CMOSSize[0] / 2, CMOSSize[0] / 2),
         color='b', linewidth=2)
plt.plot((FOVPosition, FOVPosition), (-FOVSize[0] / 2, FOVSize[0] / 2),
         color='g', linewidth=2)

# Draw Lens(es)
LensDiameter = 2.0
for i in range(np.size(LensPosition)):
    add_lens(LensPosition[i], FocalLength[i], LensDiameter, "L" + str(i))
zmin, zmax = -CMOSPosition, FOVPosition
NumberOfRays = 5
for NA in [45]:  # in range(10):
    propagate_beam((-CMOSPosition, 0), NA, NumberOfRays, LensPosition,
                   FocalLength, 'src1', 'r')
    propagate_beam((-CMOSPosition, CMOSSize[0]), NA, NumberOfRays,
                   LensPosition, FocalLength, 'src1', 'r')
    propagate_beam((-CMOSPosition, -CMOSSize[0]), NA, NumberOfRays,
                   LensPosition, FocalLength, 'src1', 'r')
    #~ propagate_beam((0, 10), NA, NumberOfRays, LensPosition, FocalLength,
                   #~ 'src1', 'b')
    plt.draw()
    plt.pause(0.1)
plt.savefig("lens_simulation_sideview.png")

# Draw top view
plt.subplot(122)
plt.title("side view")
# Draw CMOS and Scintillator
plt.plot((-CMOSPosition, -CMOSPosition), (-CMOSSize[1] / 2, CMOSSize[1] / 2),
         color='b', linewidth=2)
plt.plot((FOVPosition, FOVPosition), (-FOVSize[1] / 2, FOVSize[1] / 2),
         color='g', linewidth=2)

for i in range(np.size(LensPosition)):
    add_lens(LensPosition[i], FocalLength[i], LensDiameter, "L" + str(i))
zmin, zmax = -CMOSPosition, FOVPosition

for NA in [45]:  # in range(10):
    propagate_beam((-CMOSPosition, 0), NA, NumberOfRays, LensPosition,
                   FocalLength, 'src1', 'r')
    propagate_beam((-CMOSPosition, CMOSSize[1]), NA, NumberOfRays,
                   LensPosition, FocalLength, 'src1', 'r')
    propagate_beam((-CMOSPosition, -CMOSSize[1]), NA, NumberOfRays,
                   LensPosition, FocalLength, 'src1', 'r')
    #~ propagate_beam((0, 10), NA, NumberOfRays, LensPosition, FocalLength,
                   #~ 'src1', 'b')
    plt.draw()
    plt.pause(0.1)
#~ propagate_beam(srcpos,          4, 500, zl, ff, 'src1', 'b')
#~ propagate_beam((0.0, -2.),      4,  20, zl, ff, 'src1', 'r')
#~ propagate_beam((zpup,),    0.0005,  20, zl, ff, 'src1', 'g')
#~ propagate_beam((110,),          2,  40, zl, ff, 'DM',   'y')

plt.savefig("lens_simulation_sideview.png")
plt.ioff()
plt.show()
exit()

# Draw the light beams
xsrc, zsrc, zpup = 15.0, 15.0, -10  # position of src and pupil
srcpos = (zsrc, xsrc)

#  draw the different beams
# --------------------------
propagate_beam((0, CMOSSize[0]), NumericalAperture, 30, LensPosition,
                FocalLength, 'src1', 'b')
propagate_beam((0.0, 0), 6,  20, LensPosition, FocalLength, 'src1', 'r')
propagate_beam((zpup,), 0.0005,  20, LensPosition, FocalLength, 'src1', 'g')
propagate_beam((110,), 50,  40, LensPosition, FocalLength, 'DM',   'y')

#  print a couple labels
# --------------------------
plt.text(0, 20, 'src 1', bbox=dict(facecolor='blue', alpha=1), fontsize=10)
plt.text(0, 17, 'src 2', bbox=dict(facecolor='red',  alpha=1), fontsize=10)
plt.text(0, 14, 'pupil', bbox=dict(facecolor='green',  alpha=1), fontsize=10)
plt.text(0, 11, 'DM', bbox=dict(facecolor='yellow',  alpha=1), fontsize=10)
#~
#      add the lenses
# -------------------------
for i in range(np.size(LensPosition)):
    add_lens(LensPosition[i], FocalLength[i], 10, "L" + str(i))

#     plot optical axis
# -------------------------
#~ plt.plot([zmin,zmax], [0,0], 'k')
plt.plot()
#~ plt.axis([zmin,zmax, xmin, xmax])
plt.title("Example of brilliant optical design!")
plt.show()
