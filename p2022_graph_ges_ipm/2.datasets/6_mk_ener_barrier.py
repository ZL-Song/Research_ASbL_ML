# Extract single point energies and energy barriers from the pathway results. 
# Zilin Song, 06 Dec 2021
# 

import iomisc, numpy
if __name__ == '__main__':
    d1_ener, d1_barrier = iomisc.loadener('d1')
    d2_ener, d2_barrier = iomisc.loadener('d2')

    print(d1_ener.shape)
    print(d1_barrier.shape)
    print(d2_ener.shape)
    print(d2_barrier.shape)

    numpy.save('./rawds/ges_imi.d1.ener.npy', d1_ener)
    numpy.save('./rawds/ges_imi.d1.barrier.npy', d1_barrier)
    numpy.save('./rawds/ges_imi.d2.ener.npy', d2_ener)
    numpy.save('./rawds/ges_imi.d2.barrier.npy', d2_barrier)