import re
import codecs
import pandas as pd

def cleanLog(inName,outName):
    with codecs.open(inName,"r",\
                     encoding='utf-8', errors='ignore') as file:
        print("start process file: ", inName)
        src_ip = []
        dst_ip = []
        src_port = []
        dst_port = []
        # i=0
        for row in file:
            if "policy deny" in row:
                g = re.search(
                    ".*SESSION: (?P<src_ip>\d+\.\d+\.\d+\.\d+):(?P<src_port>\d+)->(?P<dst_ip>\d+\.\d+\.\d+\.\d+):(?P<dst_port>\d+)",row)

                src_ip.append(g["src_ip"])
                src_port.append(g["src_port"])
                dst_ip.append(g["dst_ip"])
                dst_port.append(g["dst_port"])
            data = dict(src_ip=src_ip, dst_ip=dst_ip, src_port=src_port, dst_port=dst_port)
        df = pd.DataFrame(data)
        df = df[["src_ip","src_port","dst_ip","dst_port"]]
        df.to_csv(outName,index=None)
        print("data is in ",outName)
if __name__=="__main__":
    # cleanLog("./boot.log.20170903-2359","./out/denied.csv")

    import sys
    print(sys.argv)
    cleanLog(sys.argv[1],sys.argv[2])