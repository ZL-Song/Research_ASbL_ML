# This script aligns the transitions
# Zilin Song, 4NOV2019
#

import numpy as numpy

def load_pathways(basis):
    return numpy.load('../../7.feat.sele/0.man.sele/0.ml_dat.build/{0}.ml_dat/ds_all.y_train.npy'.format(basis)).reshape(18,50).tolist()

def load_ts(basis, pathid):

    ts_dat = None
    if basis == 'sccdftb':
        ts_dat = [
            (8, 18, 28), (6, 15, 27), (15, 18, 27), (8, 16, 26), (10, 17, 28), (7, 16, 26),
            (9, 18, 28), (11, 18, 28), (10, 18, 29), (6, 15, 27), (8, 16, 27), (7, 17, 28),
            (4, 14, 27), (6, 15, 26), (7, 16, 27), (8, 17, 28), (6, 15, 29), (15, 19, 28),
        ]
    elif basis == '631G':
        ts_dat = [
            (20, 22, 25), (19, 22, 29), (22, 24, 27), (18, 21, 26), (22, 24, 28), (17, 21, 25),
            (21, 22, 26), (21, 22, 25), (21, 23, 27), (19, 23, 27), (21, 23, 26), (18, 22, 27),
            (19, 21, 24), (20, 21, 24), (21, 23, 26), (20, 23, 29), (21, 22, 26), (18, 21, 25),
        ]
    elif basis == '631+Gd':
        ts_dat = [
            (21, 23, 27), (19, 22, 29), (21, 23, 29), (19, 21, 27), (23, 24, 28), (18, 21, 27),
            (20, 22, 27), (25, 26, 29), (21, 23, 29), (20, 23, 28), (21, 23, 28), (19, 22, 28),
            (19, 22, 24), (20, 21, 26), (21, 23, 28), (21, 23, 29), (21, 22, 27), (19, 22, 28),
        ]
    elif basis == '631++Gdp':
        ts_dat = [
            (21, 24, 27), (19, 22, 29), (22, 23, 29), (19, 21, 27), (23, 24, 29), (18, 21, 27),
            (21, 22, 27), (21, 22, 29), (21, 23, 29), (20, 23, 28), (21, 23, 28), (19, 22, 28),
            (19, 22, 24), (20, 21, 26), (21, 23, 28), (21, 23, 29), (21, 22, 27), (19, 22, 28),
        ]
    elif basis == 'dftd631++Gdp':
        ts_dat = [
            (21, 23, 27), (19, 23, 29), (22, 24, 29), (19, 21, 27), (23, 24, 28), (18, 21, 27),
            (21, 23, 27), (21, 22, 29), (21, 24, 29), (20, 23, 28), (21, 24, 28), (19, 23, 28),
            (19, 22, 24), (20, 22, 26), (21, 23, 28), (21, 23, 29), (21, 23, 27), (19, 22, 28),
        ]
    elif basis == '6311++Gdp':
        ts_dat = [
            (21, 23, 27), (19, 22, 29), (22, 23, 29), (19, 21, 27), (22, 23, 29), (18, 22, 27),
            (21, 22, 27), (25, 26, 29), (22, 23, 29), (20, 22, 28), (21, 23, 28), (19, 22, 28),
            (20, 21, 24), (20, 21, 25), (21, 23, 28), (21, 23, 29), (21, 22, 27), (19, 22, 28),
        ]
    elif basis == 'dftd6311++Gdp':
        ts_dat = [       
            (21, 23, 27), (19, 22, 29), (22, 24, 29), (19, 23, 27), (23, 24, 28), (18, 22, 27),
            (21, 23, 27), (25, 26, 29), (21, 23, 29), (20, 23, 28), (21, 24, 28), (19, 22, 28),
            (19, 22, 24), (20, 22, 26), (21, 23, 28), (21, 23, 29), (21, 22, 27), (19, 22, 28),
        ]

    return ts_dat[pathid]

def get_progress(basis, pathid, path_e):
    first_ts, ti, second_ts = load_ts(basis, pathid)

    first_barrier = round(path_e[first_ts], 6)
    second_barrier = round(path_e[second_ts]-path_e[ti], 6)
    overall_barrier = round(path_e[second_ts], 6)

    first_phase = [i for i in range(0, ti)]
    second_phase = [i for i in range(ti, 49)]
    #third_phase = [i for i in range(second_ts, 49)]

    progress = []
    for i in range(len(first_phase)):
        progress.append(round(i * 1/len(first_phase), 2))
    for i in range(len(second_phase)):
        progress.append(round(i * 1/len(second_phase) + 1, 2))
    #for i in range(len(third_phase)):
    #    progress.append(round(i * 1/len(third_phase) + 2, 2))
    
    progress.append(2.0)
    return progress, [first_barrier, second_barrier, overall_barrier]

def main():

    basis_list = ['sccdftb', '631G', '631+Gd', '631++Gdp', 'dftd631++Gdp', '6311++Gdp', 'dftd6311++Gdp']
    no = 0

    barrier_out = open('estat', 'w')
    for basis_id in range(len(basis_list)):
        pae_list = []
        paths = load_pathways(basis_list[basis_id])

        for pathid in range(len(paths)):
            pae_list.append(get_progress(basis_list[basis_id], pathid, paths[pathid], ))

        barrier_list = [i[1] for i in pae_list]
        progress_list = [i[0] for i in pae_list]
        
        barrier_out.write('==== {} barriers ====\n'.format(basis_list[basis_id]))
        barrier_out.write('first barriers:   {}\n'.format([i[0] for i in barrier_list]))
        barrier_out.write('second barriers:  {}\n'.format([i[1] for i in barrier_list]))
        barrier_out.write('overall barriers: {}\n'.format([i[2] for i in barrier_list]))
        barrier_out.write('average barriers: \nfirst:{} || second:{} || overall:{} \n\n'.format(
            round(sum([i[0] for i in barrier_list])/18, 3), 
            round(sum([i[1] for i in barrier_list])/18, 3), 
            round(sum([i[2] for i in barrier_list])/18, 3))
        )

        numpy.save('aligned_prog_{0}.npy'.format(basis_list[basis_id]), [progress_list])

if __name__ == "__main__":
    main()
