import os, argparse 

configs = {
	'path': os.path.abspath(os.getcwd())
}	

pgm="gawk-5.1.0"
def build_gcov():
    # download the benchmark 
    wget_cmd="wget https://ftp.gnu.org/gnu/gawk/"+pgm+".tar.gz"
    os.system(wget_cmd)
    
    tar_cmd="tar -zxvf "+pgm+".tar.gz"
    os.system(tar_cmd)
    
    os.chdir(configs['path']+"/"+pgm)
    os.system("./configure --disable-nls CFLAGS=\"-g -fprofile-arcs -ftest-coverage\"")
    os.system("make")
    
def run_testcase(file_name):
    with open(file_name, 'r') as f:
        testcases=[l.split('\n')[0] for l in f.readlines()]

    os.chdir(configs['path']+"/"+pgm)
    rm_cmd="rm **/*.gcov *.gcov *.gcda **/*.gcda cov_result"
    print(rm_cmd)
    os.system(rm_cmd)
     
    print("----------------Run Test-Cases-------------------------------------")
    print("-------------------------------------------------------------------")
    for tc in testcases:
        print(tc)
        os.system(tc)
    gcov_file="cov_result"
    gcov_cmd="gcov -b *.gcda **/*.gcda 1> "+gcov_file+" 2> err"
    os.system(gcov_cmd)
    print("-------------------------------------------------------------------")
    cal_coverage(gcov_file)

def cal_coverage(cov_file):
    #File 'main.c'
    #Lines executed:18.15% of 639 
    #Branches executed:15.74% of 394 
    #Taken at least once:4.57% of 394 
    #Calls executed:23.73% of 354 
    #Creating 'main.c.gcov'
    coverage=0
    total_coverage=0
    with open(cov_file, 'r') as f:
        lines= f.readlines()
        for line in lines:
            if "Taken at least" in line:
                data=line.split(':')[1]
                percent=float(data.split('% of ')[0])
                total_branches=float((data.split('% of ')[1]).strip())
                covered_branches=int(percent*total_branches/100)
                
                coverage=coverage + covered_branches    
                total_coverage=total_coverage + total_branches 
    print("----------------Results--------------------------------------------")
    print("-------------------------------------------------------------------")
    print("The number of covered branches: "+str(coverage))
    print("The number of total branches: "+str(int(total_coverage)))
    print("-------------------------------------------------------------------")
    return coverage

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument("testcase_file")
    args = parser.parse_args()
    flag = args.build
    testcase_file = args.testcase_file
    
    if flag==True:
        build_gcov()
    else:
        run_testcase(testcase_file)

if __name__ == '__main__':
    main()
