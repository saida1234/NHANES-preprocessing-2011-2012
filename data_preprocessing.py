import xport, scipy.io
import numpy as np

def numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:,None]

    # Setup output array and put elements from data into masked positions
    out = np.zeros(mask.shape)
    out[mask] = np.concatenate(data)
    return out


with open('PAXMIN_G.XPT', 'rb') as f:
    columns = xport.to_columns(f)
    print(columns.keys())

    subject_dict = {}
    for i in range(len(columns['SEQN'])):
        PAXDAYM = int(columns['PAXDAYM'][i])
        SEQN = int(columns['SEQN'][i])
        PAXDAYWM = int(columns['PAXDAYWM'][i])
        PAXMTSM = float(columns['PAXMTSM'][i])

        if not ((PAXDAYM == 1) or (PAXDAYM == 9)):
            if SEQN not in subject_dict:
                subject_dict[SEQN] = [
                    [1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0],
                ]

            subject_dict[SEQN][PAXDAYWM - 1].append(PAXMTSM)

    for SEQN in subject_dict.keys():
        subject_dict_np = numpy_fillna(subject_dict[SEQN]).transpose()
        scipy.io.savemat(str(SEQN) + '.mat', mdict={'data': subject_dict_np})


