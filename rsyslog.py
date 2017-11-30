import re
import argparse
import codecs

class Rsyslog():
    def __init__(self,inFile,outFile,filter=None):
        self.file = inFile
        self.output = outFile
        self.blacklist = filter
        self.filter = []
        # self.verbose = 10000

        if filter:
            with open(filter) as blacklist_file:
                for line in blacklist_file:
                    self.filter.append(line.strip())
        print("The filter words is %s. \n" % self.filter)

    def init(self):
        # catch fields
        self.time = "None"
        self.producer = "None"
        self.event = "None"
        self.src_ip = "None"
        self.src_port = "None"
        self.dst_ip = "None"
        self.dst_port = "None"
        self.app_name = "None"
        self.valid = False
        return

    def _parser(self,data,outfile):
        self.init()
        line = data.split()
        producer_ip = line[3]
        # print(producer_ip)
        # if producer_ip == "30.1.32.221" or producer_ip == "30.1.32.223":
        if line[4] == "rule_id:":
            # print("catch it ")
            self.valid = True
        if self.valid == True:
            self.producer = line[3]

            reg = re.search(".*time:\s*(?P<time>\d+-\d+-\d+ \d+:\d+:\d+);.*", data)
            if reg:
                self.time = reg.group("time")
            # else:
            #     print(data)

            reg = re.search(".*;event:\s*(?P<event>.*?);.*", data)
            if reg:
                self.event = reg.group("event")

            reg = re.search(".*src_addr:\s*(?P<src_addr>\d+\.\d+\.\d+\.\d+);.*", data)
            if reg:
                self.src_ip = reg.group("src_addr")

            reg = re.search(".*src_port:\s*(?P<src_port>\d+);.*", data)
            if reg:
                self.src_port = reg.group("src_port")


            reg = re.search(".*dst_addr:\s*(?P<dst_addr>\d+\.\d+\.\d+\.\d+);.*", data)
            if reg:
                self.dst_ip = reg.group("dst_addr")

            reg = re.search(".*dst_port:\s*(?P<dst_port>\d+);.*", data)
            if reg:
                self.dst_port = reg.group("dst_port")

            reg = re.search(".*app_name:\s*(?P<app_name>.*)", data)
            if reg:
                self.app_name = reg.group("app_name")
        return

    def _filter(self,data):
        for cond in self.filter:
            # modify app_name bug
            if re.search("app_name", cond):
                cond = cond+";"
            mod_data = data.strip()+";"
            if re.search(cond, mod_data):
                return True
        return False

    def run(self):
        with codecs.open(self.file, "r", encoding='utf-8', errors='ignore') as file,\
             open(self.output,"w+") as outfile:
            # write field name
            outfile.write("time,producer,event,src_ip,src_port,dst_ip,dst_port,app_name\n")
            for i,line in enumerate(file):
                if self._filter(line):
                    continue
                # print(line)
                self._parser(line,outfile)

                # write to file
                if self.valid:
                    fields = [self.time, self.producer, self.event,
                              self.src_ip, self.src_port, self.dst_ip,
                              self.dst_port, self.app_name]
                    # print(",".join(fields) + "\n")
                    outfile.write(",".join(fields) + "\n")
                # if i > 10:
                #     break
                print("Line %d processed." %i)

def main():
    # infile = "data-11.txt"
    # outfile = "test.txt"

    parser = argparse.ArgumentParser(description="rsyslog parser")
    parser.add_argument("--input",action="store",help="input file name")
    parser.add_argument("--output",action="store",help="output file name")
    parser.add_argument("--filter", action="store", help="filter condition file")
    args = parser.parse_args()

    rsys = Rsyslog(args.input, args.output,args.filter)
    rsys.run()

if __name__ == '__main__':
    main()
