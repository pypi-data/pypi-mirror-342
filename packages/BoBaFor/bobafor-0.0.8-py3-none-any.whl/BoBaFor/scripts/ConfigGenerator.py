import os
import pandas as pd
from optparse import OptionParser

usage="usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-f", "--filename", default="config", dest="sample_dict", help="FASTQ file to resample [REQUIRED]", type="string")
parser.add_option("-r", "--replace", default="False", dest="repl", help="whether to sample with or without replacement (T,F) [REQUIRED]", type="string")
parser.add_option("-i", "--Iter", dest="rand_state", help="Number of iterations of random seeds to use to generate subsample", type="int")
parser.add_option("-b", "--perc_boot", dest="perc_boot", help="number of repeats [REQUIRED]", type="float")
parser.add_option("-p", "--parentdir", dest="parent_dir", help="working directory for snakemake", default= os.getcwd(), type="string")
parser.add_option("-o", "--output", dest="outdir", default="CONFIGS", help="Output directory", type="string")
options, args = parser.parse_args()
# print(options)
# ls *.gz > samples.txt
# awk '$2="data/"$1' samples.txt > samples2.txt
# awk '{sub(/\.fastq\.gz$/,":",$1)}1' samples2.txt > samples3.txt

COMBOS = pd.read_csv(str(options.parent_dir)+'/names_combos.txt', sep='\t', index_col=0)


os.chdir(str(options.parent_dir))
with open("data/samples3.txt") as f1:
    lines = f1.readlines()
    lines = [line.strip() for line in lines]

if not os.path.isdir(str(options.outdir)):
    os.makedirs(str(options.outdir))
os.chdir(str(options.outdir))


for j in range(options.rand_state):
    with open(str(options.sample_dict)+'_'+str(j)+".yaml", "w") as f:
        f.write("samples:\n")
        for sample in lines:
            f.write("    "+str(sample)+"\n")
        f.write("replace:\n")
        f.write("    "+str(options.repl)+'\n')
        f.write("randomstate:\n")
        f.write("    "+str(j)+ '\n') #options.randstate
        f.write("percentBoot:\n")
        f.write("    "+str(options.perc_boot)+'\n')
        f.write("combos:\n")
        for i in range(len(COMBOS)):
            f.write('    '+str(COMBOS.iloc[i,1])+'vs'+str(COMBOS.iloc[i,2])+': .csv.gz\n')
        f.write("ResampleOUT:\n")
        f.write("    " + str(j) + "/resampling/\n")
        f.write("ResampleIN:\n")
        # f.write("\t/mnt/c/Users/pauld/SNAKEmake/RNAseq/SET3/\n")#options.parentdir
        f.write("    "+str(options.parent_dir)+"/\n")
        f.write("KallistoOUT:\n")
        f.write("    "+str(j)+"/kallisto/\n")
        f.write("DEseqOUT:\n")
        f.write("    out/")