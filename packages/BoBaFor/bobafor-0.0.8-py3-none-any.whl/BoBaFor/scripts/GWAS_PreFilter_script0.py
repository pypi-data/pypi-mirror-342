# %%
import pandas as pd
import os
# from scipy.stats import chi2_contingency, false_discovery_control
# import statsmodels.stats.multitest as multi
from itertools import combinations
import random
import numpy as np
from optparse import OptionParser
from BoBaFor.TreeTune.ClassTuning import Tuning

# %%
usage="usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-p", "--predictor",  dest="predictor", help=" Predictor Matrix [REQUIRED]", type="string")
parser.add_option("-r", "--response", dest="resp", help="response file [REQUIRED]", type="string")
#parser.add_option("-c", "--correct", dest="correct", help="if pvals should be corrected [REQUIRED]",default = False, action = 'store_true')
parser.add_option("-c", "--correct", dest="correct", help="if pvals should be corrected [REQUIRED]",default = 'True', type='string')
parser.add_option("-k", "--thresh", dest="thresh", help="pval threshold to remove noise [REQUIRED]", type="float")
parser.add_option("-t", "--outfile", dest="outf", help="name to save predictor file [REQUIRED]", type="string")
parser.add_option("-o", "--output", dest="outdir", default=os.getcwd(), help="Output directory [REQUIRED]", type="string")
options, args = parser.parse_args()

# %%
TuneObj = Tuning()
print(options.correct)

Predictor = pd.read_csv(options.predictor, sep='\t', index_col=0)#.T
response=pd.read_csv(options.resp, sep='\t', index_col=0)
response.columns=['response']

if not os.path.isdir(options.outdir):
    os.makedirs(options.outdir)
os.chdir(options.outdir)

pval = TuneObj.chi2_Sim_Test( Predictor, response)
if options.correct=='True':
    Predictor=Predictor[pval.loc[pval['Padj']<options.thresh]['Col'].to_list()]
elif options.correct=='False':
    Predictor=Predictor[pval.loc[pval['Pval']<options.thresh]['Col'].to_list()]
else:
    print("Please choose True/False when correcting chi2 pvalues for prefilter step.")

print("number of columns",len(Predictor.columns))
print('\n')
Predictor.to_csv(str(options.outf), sep='\t')
