import pandas as pd
from BoBaFor.TreeTune.ClassTuning import Tuning
from BoBaFor.FeatureSelect.ClassFeatureSelection import FeatSelection
import numpy as np
import os
from joblib import Parallel, delayed
from optparse import OptionParser
import pickle

usage="usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-p", "--predictor",  dest="lsbsr", help="lsbsr matrix [REQUIRED]", type="string")
parser.add_option("-r", "--response",  dest="abx", help="response vector [REQUIRED]", type="string")
parser.add_option("-s", "--simulation",  dest="sim", help="simulation identifier [REQUIRED]", type="string")
parser.add_option("-t", "--percentBoruta",  dest="perc", default=1, help="percent of Boruta to select", type="float")
parser.add_option("-l", "--BorutaPercThresh",  dest="BORperc", default=1, help="percent of Boruta to select", type="float")
parser.add_option("-k", "--pvalthresh", dest='pval', default=0.05, help="pvalue threshold for Boruta", type='float')
parser.add_option("-q", "--collectAll",  dest="collect", default=True, help="whether to utilize all boruta selected features in downstream optimization [REQUIRED]", type="string")
parser.add_option('-n', '--repeat', dest='rep', default=os.cpu_count(), help='number of times to Boruta select', type='int')
parser.add_option("-o", "--output", dest="outdir", default=os.getcwd(), help="Output directory [REQUIRED]", type="string")
parser.add_option("-m", "--model", dest="model", default=os.getcwd(), help="Output directory [REQUIRED]", type="string")

# parser.add_option("-g", "--groups", dest="groups", default='Reshuffle_groups.txt', help="group_file", type="string")

options, args = parser.parse_args()

# %% ################################################################
#### Data Input and Boruta Selection
print('BorutaOUT_'+str(options.perc)+str(options.pval))
parentDIR = os.getcwd()
numCores = -1#int(os.cpu_count()/6)
print(os.cpu_count(), numCores)
TuneObj = Tuning()
X, Y, n_splits, class_weight =TuneObj.XY_index(X=options.lsbsr, Y=options.abx, BacGWASim=False)
RAND=np.random.RandomState(4)

# RFoptimal = pickle.load('TuningOUT/RFOptimal_Tuning1_'+options.sim+'.pickle')
with open('TuningOUT_'+str(options.model)+'/Optimal_Tuning1_'+options.sim+'.pickle', 'rb') as filehandle:
    RFoptimal=pickle.load(filehandle)

NewNASPobj = FeatSelection(percent=options.perc, alpha=options.pval, v=1, max_iter=2500, repeat=options.rep)
Borut_Est=RFoptimal.n_estimators
SelectL = Parallel(n_jobs=numCores, backend="loky", prefer='processes' )(delayed(NewNASPobj.BorutaSelect)(RFoptimal, NewNASPobj.percent, NewNASPobj.alpha, X, Y, Borut_Est, NewNASPobj.v, NewNASPobj.max_iter, rand=i, ) for i in range(NewNASPobj.repeat))

Selected, Tentative = NewNASPobj.BorutaOrganize(SelectL, NewNASPobj.repeat)

if not os.path.isdir('BorutaOUT'):
    os.makedirs('BorutaOUT')
os.chdir('BorutaOUT')
BORUTAdir = os.getcwd()
Selected.to_csv(str(options.model)+'_Boruta_Selected_'+options.sim+'.txt', sep='\t')
Tentative.to_csv(str(options.model)+'_Boruta_Tentative_'+options.sim+'.txt', sep='\t')

# %% ################################################################
#### Final Feature Matrix Generation
# Genes = pd.read_csv('Boruta_Selected_'+options.sim+'.txt', index_col=0, sep='\t')
print(len(X.columns))
# print(options.collect)
if options.collect!='True':
    print("Entered Boruta Percent Selection Loop")
    Selected=Selected.loc[Selected["PERCENT_SELECT"]>=options.BORperc]
elif options.collect=='True':
    print("Entered All Boruta selected loop")
    Selected=Selected
else:
    print("Something went wrong in Boruta selection code.")
X = X[Selected['SELECTED'].to_list()]
print(len(X.columns))

X.to_csv(str(options.model)+'_FinalFeatureMatrix_BorutaSelected_'+options.sim+'.txt', sep='\t')
