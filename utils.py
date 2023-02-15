import pickle
def save_times(time_list, outfile_name='times.pkl'):
    # save with the binary protocol
    # print(f'Save weight to {outfile_name}')
    with open(outfile_name, 'wb') as outfile:
        pickle.dump(time_list, outfile, pickle.HIGHEST_PROTOCOL)
def load_times(infile_name='times.pkl'):
    # save with the binary protocol
    with open(infile_name, 'rb') as infile:
        times_list = pickle.load(infile)
    return times_list