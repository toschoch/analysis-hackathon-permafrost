import pandas as pd
import pathlib


def sampledata(datapath : pathlib.Path, targets):
    """ makes a pandas pickle from cars data file """

    data = pd.read_csv(datapath.joinpath("cars.csv"), usecols=[1,2])

    data.to_pickle(targets[0])

