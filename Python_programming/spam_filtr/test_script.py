import os

import filter
import quality as quality
from utils import read_classification_from_file
from confmat import BinaryConfusionMatrix

#path 2: data to train on, path 1: data to test filter on
path2 = "PATH_TO_FILE_TO_TRAIN_ON"
path1 = "PATH_TO_FILE_TO_TEST_ON"

filtr = filter.MyFilter()
filtr.train(path2)
filtr.test(path1)

print(quality.compute_quality_for_corpus(path1))

#os.remove(os.path.join(path,"!prediction.txt"))
