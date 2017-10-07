import re
import codecs
import pandas as pd

def cleanLog(inName,outName):
    with codecs.open(inName,"r",\
                     encoding='utf-8', errors='ignore') as file:
        src_ip = []
        dst_ip = []
        # i=0
        for row in file:
            if "policy deny" in row:
                g = re.search(".*SESSION: (?P<src_ip>\d+\.\d+\.\d+\.\d+:\d+)->((?P<dst_ip>\d+\.\d+\.\d+\.\d+:\d+))",row)
                src_ip.append(g["src_ip"])
                dst_ip.append(g["dst_ip"])
            # if i == 100000:
            #     break
            # i +=1
        data = dict(src_ip = src_ip,dst_ip = dst_ip)
        df = pd.DataFrame(data)
        df = df[["src_ip","dst_ip"]]
        df.to_csv(outName,index=None)
        print("data is in %s",outName)
if __name__=="__main__":
    cleanLog("./boot.log.20170807-2359","./app/revise.csv")