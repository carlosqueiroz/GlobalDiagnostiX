"""
Script to read and display the experiments done with the iAi electronics
prototype
"""

import glob
import os
import numpy
import matplotlib.pylab as plt
import platform

import lineprofiler

# CameraSize
CameraWidth = 1280
CameraHeight = 1024

# Get images
if platform.node() == 'anomalocaris':
    RootPath = '/Volumes/slslc/EssentialMed/Images/DetectorElectronicsTests'
else:
    RootPath = '/afs/psi.ch/project/EssentialMed/Images' \
               '/DetectorElectronicsTests'

MyColors = ["#95C5B5", "#BF55C4", "#BC4E35", "#7FCE56", "#51364A", "#CDB151", "#7D81C2", "#576239", "#CA6787"]

# Get Folders
Folder = '*Gain-Se*'

Radiographies = sorted(glob.glob(os.path.join(RootPath, Folder, '*1-44.gray')))
Darks = sorted(glob.glob(os.path.join(RootPath, Folder, '*0-44.gray')))

Mean = numpy.zeros(len(Radiographies))
Max = numpy.zeros(len(Radiographies))
STD = numpy.zeros(len(Radiographies))

CorrectedMean = numpy.zeros(len(Radiographies))
CorrectedMax = numpy.zeros(len(Radiographies))
CorrectedSTD = numpy.zeros(len(Radiographies))

ZoomedMean = numpy.zeros(len(Radiographies))
ZoomedMax = numpy.zeros(len(Radiographies))
ZoomedSTD = numpy.zeros(len(Radiographies))

LineProfile = []
Coordinates = [(30, 310), (35, 10)]

# Display difference
plt.figure(1, figsize=(18, 12))

for counter in range(len(Radiographies)):
    # Inform user
    print str(counter + 1) + '/' + str(len(Radiographies)) + ': Reading Images'

    # Grab data
    ImageData = numpy.fromfile(Radiographies[counter],
                               dtype=numpy.int16).reshape(CameraHeight,
                                                          CameraWidth)
    DarkData = numpy.fromfile(Darks[counter], dtype=numpy.int16).reshape(
        CameraHeight, CameraWidth)
    CorrectedData = ImageData - DarkData
    ZoomedData = CorrectedData[445:775, 510:615]

    tmp, LineProfile= lineprofiler.lineprofile(ZoomedData, Coordinates)

    Mean[counter] = numpy.mean(ImageData)
    Max[counter] = numpy.max(ImageData)
    STD[counter] = numpy.std(ImageData)

    CorrectedMean[counter] = numpy.mean(CorrectedData)
    CorrectedMax[counter] = numpy.max(CorrectedData)
    CorrectedSTD[counter] = numpy.std(CorrectedData)

    ZoomedMean[counter] = numpy.mean(ZoomedData)
    ZoomedMax[counter] = numpy.max(ZoomedData)
    ZoomedSTD[counter] = numpy.std(ZoomedData)

    ExposureTime = os.path.basename(Radiographies[counter]).split('-e')[
        1].split('-g')[0]
    Gain = os.path.basename(Radiographies[counter]).split('-g')[1].split(
        '-i')[0]

    # Display data
    plt.subplot(5, len(Radiographies), counter + 1)
    plt.imshow(ImageData, cmap='bone', vmin=0, vmax=2 ** 10,
               interpolation='bicubic')
    plt.axis('off')
    plt.title('Gain ' + Gain)
    plt.subplots_adjust(hspace=0.025)
    plt.subplots_adjust(wspace=0.025)

    plt.subplot(5, len(Radiographies), counter + 1 + len(Radiographies))
    plt.imshow(CorrectedData, cmap='bone', interpolation='bicubic',
               vmax=CorrectedMean[counter] + 3 * CorrectedSTD[counter])
    plt.axis('off')
    plt.title('Mean+3xSTD')
    plt.subplots_adjust(hspace=0.025)
    plt.subplots_adjust(wspace=0.025)

    plt.subplot(5, len(Radiographies), counter + 1 + 3 * len(Radiographies))
    plt.imshow(ZoomedData, cmap='bone', interpolation='bicubic',
               vmax=CorrectedMean[counter] + 3 * CorrectedSTD[counter])
    plt.axis('off')
    #~ plt.title('Zoom')

    plt.plot((Coordinates[0][0], Coordinates[1][0]), (Coordinates[0][1], Coordinates[1][1]), color=MyColors[counter])
    plt.plot(Coordinates[0][0], Coordinates[0][1], color='yellow', marker='o')
    plt.plot(Coordinates[1][0], Coordinates[1][1], color='black', marker='o')

    #~ plt.subplots_adjust(hspace=0.025)
    #~ plt.subplots_adjust(wspace=0.025)

    ShowHistograms = False
    if ShowHistograms:
        plt.hist(ImageData.flatten(), log=True, bins=32, fc='y', ec='y',
                 alpha=0.25)
        plt.hist(CorrectedData.flatten(), bins=32, fc='k', ec='k', alpha=0.5)
        # turn off tick labels of histogram
        plt.gca().get_xaxis().set_ticks([])
        plt.gca().get_yaxis().set_ticks([])

    plt.subplot(515)
    plt.plot(LineProfile + 20 * counter, label=Gain, color=MyColors[counter])
    plt.xlim([0, len(LineProfile)])
    plt.ylabel('[a. u.]')
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))


# Plot max, mean and standard deviation of images
plt.subplot(513)
plt.plot(Max, '-', label='Max')
plt.plot(Mean, '-', label='Mean')
plt.plot(STD, '-', label='STD')

plt.plot(CorrectedMax, '-o', label='Corrected Max')
#~ plt.plot(CorrectedMean, '-o', label='Corrected Mean')
#~ plt.plot(CorrectedSTD, '-o', label='Corrected STD')

#~ plt.plot(ZoomedMax, '-*', label='Zoomed Max')
#~ plt.plot(ZoomedMean, '-*', label='Zoomed Mean')
#~ plt.plot(ZoomedSTD, '-*', label='Zoomed STD')

plt.xlim([-0.5, len(Radiographies) - 0.5])
#~ plt.xlabel('Image')
plt.ylabel('Brightness')

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.savefig('Gainseries.png', bbox_inches='tight')
plt.show()
