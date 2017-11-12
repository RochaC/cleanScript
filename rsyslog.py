import re
import argparse
import codecs

class Rsyslog():
    def __init__(self,inFile,outFile):
        self.file = inFile
        self.output = outFile
        # self.verbose = 10000

        # catch fields
        self.time = "None"
        self.producer = "None"
        self.event = "None"
        self.src_ip = "None"
        self.src_port = "None"
        self.dst_ip = "None"
        self.dst_port = "None"
        self.app_name = "None"

    def _parser(self,data,outfile):
        line = data.split()
        valid = line[3]

        if re.search("\d+\.\d+\.\d+\.\d+",valid):
            # print(data)
            self.producer = valid

            reg = re.search(".*time:\s*(?P<time>\d+-\d+-\d+ \d+:\d+:\d+);.*", data)
            if reg:
                self.time = reg.group("time")

            reg = re.search(".*;event:\s*(?P<event>.*?);.*", data)
            if reg:
                self.event = reg.group("event")

            reg = re.search(".*src_addr:\s*(?P<src_addr>\d+\.\d+\.\d+\.\d+);.*", data)
            if reg:
                self.src_addr = reg.group("src_addr")

            reg = re.search(".*src_port:\s*(?P<src_port>\d+);.*", data)
            if reg:
                self.src_port = reg.group("src_port")


            reg = re.search(".*dst_addr:\s*(?P<dst_addr>\d+\.\d+\.\d+\.\d+);.*", data)
            if reg:
                self.dst_addr = reg.group("dst_addr")

            reg = re.search(".*dst_port:\s*(?P<dst_port>\d+);.*", data)
            if reg:
                self.dst_port = reg.group("dst_port")

            reg = re.search(".*app_name:\s*(?P<app_name>.*)", data)
            if reg:
                self.app_name = reg.group("app_name")

            fields = [self.time, self.producer, self.event,
                           self.src_ip, self.src_port, self.dst_ip,
                           self.dst_port, self.app_name]
            outfile.write(",".join(fields)+"\n")

    def run(self):
        with codecs.open(self.file, "r", encoding='utf-8', errors='ignore') as file,\
             open(self.output,"w+") as outfile:
            # write field name
            outfile.write("time,producer,event,src_ip,src_port,dst_ip,dst_port,app_name\n")
            for i,line in enumerate(file):
                self._parser(line,outfile)
                # break
                # if i % self.verbose:
                print("Line %d processed." %i)

def main():
    infile = "data-11.txt"
    outfile = "test.txt"

    parser = argparse.ArgumentParser(description="rsyslog parser")
    parser.add_argument("--input",action="store",help="input file name")
    parser.add_argument("--output",action="store",help="output file name")
    args = parser.parse_args()

    rsys = Rsyslog(args.input, args.output)
    rsys.run()

if __name__ == '__main__':
    main()
