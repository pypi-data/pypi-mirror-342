import argparse
import os
# import snakemake
# import sys
# import yaml
import subprocess
import BoBaFor
# from . import _program
# _program = "BoBaFor"
parser = argparse.ArgumentParser(
    prog="BoBaFor", description="Description"
)

parser.add_argument(
    "--config", dest="config",
    metavar="FILE", type=str,
    help="Path to a config file", 
)
parser.add_argument(
    "--output-dir",
    metavar="DIR",
    help="Path to the output directory", 
)
parser.add_argument(
    "--cores",
    metavar="CORES", dest='cores', type=int,
    help="number of processes", 
)

args = parser.parse_args()
def main():
    print(args.config)
    result=subprocess.run(["snakemake --nolock --snakefile "+'/'.join(os.path.abspath(BoBaFor.__file__).split('/')[:-1])+'/Snakefile'+ ' --configfile '+os.getcwd()+'/'+str(args.config) + ' --cores ' +str(args.cores)], shell=True, capture_output=True, text=True, check=False)
    print(result.stdout)
    print(result.stderr)
    print(result)
if __name__ == '__main__':
    main()