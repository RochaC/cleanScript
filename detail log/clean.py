from mergeData import *
import os
import re
import codecs
import pandas as pd
import shutil



def _cleanLog(inName, outName, ft=None):
    '''

    :param inName:  Input filename
    :param outName: output filename
    :param ft: if need filter. filter config file
    :return: 
            csv output
    '''
    # for debug params
    print("input argv is ", inName, outName, ft)

    # readin data

    with codecs.open(inName, "r", \
                     encoding='utf-8', errors='ignore') as file:
        month = []
        day = []
        time = []
        src_ip = []
        dst_ip = []
        src_port = []
        dst_port = []
        policyid = []
        action = []
        i = 0
        for row in file:
            # whether is ISG
            if re.search(".*ISG.*", row):
                m = re.search("(?P<month>\S+)", row)
                if m:
                    month.append(m["month"])
                else:
                    month.append(None)

                d = re.search("\S+\s+(?P<day>\d+)", row)
                if d:
                    day.append(d["day"])
                else:
                    day.append(None)

                t = re.search("\S+\s+\d+\s+(?P<time>\d+:\d+:\d+)", row)
                if t:
                    time.append(t["time"])
                else:
                    time.append(None)

                sip = re.search(".*src_ip=(?P<src_ip>\d+\.\d+\.\d+\.\d+).*", row)
                if sip:
                    src_ip.append(sip["src_ip"])
                else:
                    src_ip.append(None)

                dip = re.search(".*dst_ip=(?P<dst_ip>\d+\.\d+\.\d+\.\d+).*", row)
                if dip:
                    dst_ip.append(dip["dst_ip"])
                else:
                    dst_ip.append(None)

                sp = re.search(".*src_port=(?P<src_port>\d+).*", row)
                if sp:
                    src_port.append(sp["src_port"])
                else:
                    src_port.append(None)

                dp = re.search(".*dst_port=(?P<dst_port>\d+).*", row)
                if dp:
                    dst_port.append(dp["dst_port"])
                else:
                    dst_port.append(None)

                pid = re.search(".*policyid=(?P<policyid>\d+).*", row)
                if pid:
                    policyid.append(pid["policyid"])
                else:
                    policyid.append(None)

                act = re.search(".*action=(?P<action>\S+);.*", row)
                if act:
                    action.append(act["action"])
                else:
                    action.append(None)
    print("finfish extract field in %s" % inName)

    # data process
    data = dict(month=month, day=day, time=time, src_ip=src_ip, dst_ip=dst_ip, \
                src_port=src_port, dst_port=dst_port, policyid=policyid, action=action)
    df = pd.DataFrame(data)

    # filter ip
    if ft:
        blacklist = []
        with open(ft) as file:
            for row in file:
                blacklist += row.split()
        black_reg = "|".join(blacklist)
        print("Filter ip like %s in src_ip and dst_ip." % ",".join(blacklist))
        df = df[~(df["src_ip"].str.contains(black_reg, na=True) | df["dst_ip"].str.contains(black_reg, na=True))]

    # ready to output
    df = df[["month", "day", "time", "src_ip", "dst_ip", "src_port", "dst_port", "policyid", "action"]]
    df.to_csv(outName, index=None)
    print("output file to  {:s}".format(outName))
    return

def cleanLog(outName,inName=None,dir=None,ft=None):
    '''
    
    :param outName: output fileName
    :param inName: single input
    :param dir: data in the whole directory
    :param ft: blacklist
    :return: none
    '''
    if dir:
        os.makedirs("./out_tmp",exist_ok=True)
        files = os.listdir(dir)
        print("Process dir in %s" %dir)
        num_file = len(files)
        for i,file in enumerate(files):
            _cleanLog(dir+"/"+file,"./out_tmp/"+"out%s"%i+".csv",ft)

        print("merge the output to %s"%outName)
        merge("./out_tmp",outName)

        # remove tmp directory
        shutil.rmtree("./out_tmp")
        return

    elif inName:
        print("Process single file: %s " %inName)
        _cleanLog(inName,outName,ft)
        return

    else:
        print("Please have an input file or input directory.")
        return
if __name__=="__main__":
    cleanData("./out/clean.csv","./messages.20170620-2359")
    # cleanData("./out/clean.csv", dir="./messages-201707")

    # import sys
    # print(sys.argv)
    # cleanLog(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
