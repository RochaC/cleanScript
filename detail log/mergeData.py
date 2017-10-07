import pandas as pd
import os

def merge(dir,outName):
    files = []
    l = os.listdir(dir)
    path = os.getcwd() + "/" + dir + "/"
    for i in l:
        if i.endswith(".csv"):
            i = path + i
            files.append(i)
    print(files)

    base = pd.read_csv(files[0])
    if len(files) >1:
        for file in files[1:]:
            df = pd.read_csv(file)
            base = base.append(df)
            print("merge file {:s}".format(file))
    base.to_csv(outName,index=False)
    print("output {:}".format(outName))

    return

if __name__=="__main__":
    # merge("test","merged.csv")

    import sys

    # print(sys.argv)
    merge(sys.argv[1], sys.argv[2])
