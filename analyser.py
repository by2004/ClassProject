import os
import sys
import csv
from ConfigParser import SafeConfigParser


#-----------------------------------------------------------------------------
#--returns sim time and # of cycles for a given simulation summary file
def getResult(path):
        parser = SafeConfigParser()
        res = {}
        try:
            parser.read(path)
        except:
            res[0] = "io"
            res[1] = "io"
            res[2] = "io"
            print "IO ERROR " + path
            return res
        try:
            res[0] = parser.get(' Evergreen ', 'Instructions')
            res[1] = parser.get(' Evergreen ', 'Cycles')
            res[2] = str(parser.get(' General ', 'SimTime'))[:-5]
        except:
            if os.stat(path).st_size == 0:
                res[0] = "empty"
                res[1] = "empty"
                res[2] = "empty"
                print "EMPTY " + path
            else:
                res[0] = "error"
                res[1] = "error"
                res[2] = "error"
                print "ERROR " + path
        return res

#-----------------------------------------------------------------------------
#--returns sim time and # of cycles for a given simulation report log file
def getResultReport(path, numCompUnits):
        parser = SafeConfigParser()
        res = {}
        try:
            parser.read(path)
        except:
            for index in range(0, 43):
                res[index] = "io"
            print "IO ERROR " + path
            return res
        try:
            res[0] = parser.get(' Device ', 'Instructions')
            res[1] = parser.get(' Device ', 'Cycles')
            res[2] = str(parser.get(' Device ', 'InstructionsPerCycle'))
            for compUnit in range(0, 40):
                compName = " ComputeUnit " + str(compUnit) + " "
                index = 3 + compUnit
                try:
                    res[index] = parser.get(compName, 'Instructions')
                except:
                	res[index] = "-1"
            print path
        except:
            if os.stat(path).st_size == 0:
                for index in range(0, 43):
                    res[index] = "empty"
                print "EMPTY " + path
            else:
                for index in range(0, 43):
                    res[index] = "error"
                print "ERROR " + path
        return res
#-----------------------------------------------------------------------------
#--main
if __name__ == "__main__":
	path_d = "/afs/nd.edu/user39/ldaudet/project/res"
	csv_path = "/afs/nd.edu/user39/ldaudet/project/res/report.csv"
	csv_path_summary = "/afs/nd.edu/user39/ldaudet/project/res/report_summary.csv"
	try:
		os.remove(csv_path)
		os.remove(csv_path_summary)
	except OSError:
		pass
	writer=csv.writer(open(csv_path,'wb'))
	writer_summary=csv.writer(open(csv_path_summary,'wb'))
	writer.writerow(["Benchmark", "NumComputeUnits","num_sc","num_reg","reg_alloc","wf_size","max_wg_pcu","max_wf_pcu", "sched", "lds_sizes", "cycles_gen", "cycles_si", "simtime"] )
	writer_summary.writerow(["Benchmark", "NumComputeUnits","num_sc","num_reg","reg_alloc","wf_size","max_wg_pcu","max_wf_pcu", "sched", "lds_sizes", "Instructions", "Cycles", "IPC", "c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "c13", "c14", "c15", "c16", "c17", "c18", "c19", "c20", "c21", "c22", "c23", "c24", "c25", "c26", "c27", "c28", "c29", "c30", "c31", "c32", "c33", "c34", "c35", "c36", "c37", "c38", "c39", "avg occupancy"] )
	for path, subdirs, files in os.walk(path_d):
			for name in files:
				if "summarygg" in name and ".csv" not in name:
					full_path = path+ "/" + name
					sum = getResult(full_path)
					if sum != -1:
						cycles_gen = sum[0]
						cycles_si = sum[1]
						simtime = sum[2]
						full_row = name+","+cycles_gen+","+cycles_si
						testname = name[7:-4]
						args = testname.rsplit("_")
						if args[9] == "1":
							args[9] = "BinarySearch"
						if args[9] == "3":
							args[9] = "BitonicSort"
						if args[9] == "4":
							args[9] = "BlackScholes"
						if args[9] == "5":
							args[9] = "DCT"
						if args[9] == "6":
							args[9] = "DwtHaar1D"
						if args[9] == "8":
							args[9] = "DwtHaar1D"
						if args[9] == "9":
							args[9] = "PrefixSum"
						if args[9] == "10":
							args[9] = "MatrixTranspose"
						if args[9] == "12":
							args[9] = "MatrixMultiplication"
						writer.writerow([args[9],args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],cycles_gen,cycles_si,simtime])
				if "report" in name and ".csv" not in name:
					full_path = path+ "/" + name
					testname = name[10:-4]
					args = testname.rsplit("_")
					sum = getResultReport(full_path,args[0])
					if sum != -1:
						Instructions = sum[0]
						Cycles = sum[1]
						IPC = sum[2]
						full_row = Instructions+","+Cycles+","+IPC
						testname = name[10:-4]
						args = testname.rsplit("_")
						if args[9] == "1":
							args[9] = "BinarySearch"
						if args[9] == "3":
							args[9] = "BitonicSort"
						if args[9] == "4":
							args[9] = "BlackScholes"
						if args[9] == "5":
							args[9] = "DCT"
						if args[9] == "6":
							args[9] = "DwtHaar1D"
						if args[9] == "8":
							args[9] = "DwtHaar1D"
						if args[9] == "9":
							args[9] = "PrefixSum"
						if args[9] == "10":
							args[9] = "MatrixTranspose"
						if args[9] == "12":
							args[9] = "MatrixMultiplication"
						maxInst = 0
						count = 0
						avgOccupancy = 0
						occ = {}
						if sum[3] != "io" and sum[3] != "error" and sum[3] != "empty":
							for index in range (3, 43):
								 if sum[index] != "-1":
								 	count += 1
									if float(sum[index]) > maxInst:
										maxInst = float(sum[index])
							print str(maxInst)
							for index in range (0, count):
								occ[index] = float(sum[(index+3)]) / maxInst
								print "CU" + str(index) + ": " + str(occ[index])
							for index in range (0, count):
								avgOccupancy += occ[index]
							print "avgOccupancy before: " + str(avgOccupancy)
							print "count: " + str(count)
							avgOccupancy = str(avgOccupancy / float(count))
							print "avgOccupancy after: " + str(avgOccupancy)
						else:
							avgOccupancy = sum[3]
						writer_summary.writerow([args[9],args[0],args[1],args[2],args[3],args[4],args[5],args[6],args[7],args[8],Instructions,Cycles,IPC,sum[3],sum[4],sum[5],sum[6],sum[7],sum[8],sum[9],sum[10],sum[11],sum[12],sum[13],sum[14],sum[15],sum[16],sum[17],sum[18],sum[19],sum[20],sum[21],sum[22],sum[23],sum[24],sum[25],sum[26],sum[27],sum[28],sum[29],sum[30],sum[31],sum[32],sum[33],sum[34],sum[35],sum[36],sum[37],sum[38],sum[39],sum[40],sum[41],sum[42], avgOccupancy])

