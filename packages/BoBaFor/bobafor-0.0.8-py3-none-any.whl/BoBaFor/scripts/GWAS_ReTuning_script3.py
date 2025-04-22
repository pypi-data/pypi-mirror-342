from BoBaFor.TreeTune.ClassTuning import Tuning
import BoBaFor.TreeTune.ClassParamAnalysis as PMA
import numpy as np
import scipy.stats as stats
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from itertools import combinations
import os
import pickle
from optparse import OptionParser

usage="usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-p", "--predictor",  dest="lsbsr_boruta", help="lsbsr matrix [REQUIRED]", type="string")
parser.add_option("-r", "--response",  dest="abx", help="response vector [REQUIRED]", type="string")
parser.add_option("-s", "--simulation",  dest="sim", help="simulation identifier [REQUIRED]", type="string")
parser.add_option("-n", "--NumRandSearch",  dest="randNiter", default=100, help="Number of Random Search models to build", type="int")
parser.add_option("-t", "--CVRandSearch",  dest="randCV", default=100, help="Number of Random Search kfold cross-validtion to perform", type="int")
parser.add_option("-k", "--numGridSearch",  dest="gridCV", default=100, help="Number of kfold cross-validation for GridSearch to perform [REQUIRED]", type="int")
parser.add_option("-a", "--scoremetric",  dest="metric", default='roc_auc', help="scoring method to use [REQUIRED]", type="string")
parser.add_option("-o", "--output", dest="outdir", default=os.getcwd(), help="Output directory [REQUIRED]", type="string")
parser.add_option("-m", "--model", dest="model", default='RF', help="model to optimize (RF or XGB) [REQUIRED]", type="string")
# parser.add_option("-g", "--groups", dest="groups", default='Reshuffle_groups.txt', help="group_file", type="string")

options, args = parser.parse_args()

# %% ################################################################
parentDIR = os.getcwd()
numCores = -1#os.cpu_count()
print(os.cpu_count(),numCores)

TuneObj = Tuning()
X, Y, n_splits, class_weight =TuneObj.XY_index(X=options.lsbsr_boruta, Y=options.abx, BacGWASim=False)
RAND=np.random.RandomState(4)
print((X.shape))
print((Y.shape))
print((Y.value_counts()))


# %% ################################################################
#### Instantiate model and Random Search Tuning

if options.model=='RF':
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    param_space= {'max_depth': max_depth,
                'max_features': ['sqrt', 'log2', None, 0.05, 0.25],
                'criterion': ['gini', 'entropy'],
                'min_samples_split': [2, 3, 4, 5, 10, 20],
                'n_estimators': [int(x) for x in np.linspace(start = 200, stop = 2000, num = 7)]}

    ### need some kind of if-else rule on whether class_weight should be balanced
    mod = RandomForestClassifier(random_state=RAND, class_weight=class_weight)
elif options.model=='XGB':
    param_space = {'learning_rate': stats.uniform(1e-9, 0.001),
                    'n_estimators': [25, 50, 100, 200, 500],
                    'subsample': stats.uniform(0.2, 0.8),
                    'colsample_bytree': [0.25, 0.5, 0.75, 1],
                    'max_depth':[int(x) for x in np.linspace(3,100,10)]}

    mod =  XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, random_state=RAND, scale_pos_weight=len(Y==0)/len(Y==1)) #873/236 BinaryFocalLoss

if not os.path.isdir('TuningOUT_' + str(options.model)):
    os.makedirs('TuningOUT_' + str(options.model))
os.chdir('TuningOUT_' + str(options.model))
TUNINGdir = os.getcwd()

RF = TuneObj.Tuning_RandomSearch_classify(X=X, Y=Y, repeat=options.randCV, n_splits=n_splits, scorer=options.metric, mod=mod, hyperparameters=param_space, n_iter=options.randNiter, n_jobs=numCores) #n_jobs=numCores
RF.to_csv('randSearch2_'+options.sim+'.txt', sep='\t')
ParamFigObj = PMA.Param_analysis()
# CountData = ParamFigObj.RandomSearchAnalysis(RF, 0.25, 3, 'mean_test_score', figTitle='Random Forest Parameter Count \n of Top scorers from RandomSearchCV', figname="RandSearchFIG2_"+options.sim+".png")

RFGridParamSpace = ParamFigObj.RandSearchParamGrid(RF, num_opt=3, outdir=os.getcwd(), outfile='GridParamSpace2_'+options.sim+'.pickle')

# %% ################################################################
# os.chdir("../TuningOUT")
TuneObj.repeat = options.gridCV
RF = TuneObj.Tuning_GridSearch_classify(X=X, Y=Y, repeat=TuneObj.repeat, n_splits=n_splits, scorer=options.metric, mod=mod, hyperparameters=RFGridParamSpace, n_jobs=numCores) #n_jobs=numCores
RF.to_csv('gridSearch2_'+options.sim+'.txt', sep='\t')


ParamFigObj = PMA.Param_analysis()

#### Plotting
RF.params = RF.params.astype('str')
RFbest = ParamFigObj.Best_mean(RF, 'mean_test_score', 10)
RFTestFold =  ParamFigObj.Param_figs(RFbest, 'mean_test_score', 'LSBSR Random RF Tuning', 'param_min_samples_split', 'param_n_estimators') # Convert to seaborn
RFTrainFold =  ParamFigObj.Param_figs(RFbest, 'mean_train_score', 'LSBSR Random RF Tuning', 'param_min_samples_split', 'param_n_estimators')
RFTestFold.save('GridSearchFIG2_'+options.sim+'.png', dpi=300)
print(RFTestFold)
print(RFTrainFold)

#### Define best params
groups = RFbest.groupby('params')
keys = groups.groups.keys()
r = TuneObj.repeat
k = TuneObj.n_splits
nsample =len(X)
n2 = int((1/k)*nsample*r)
n1 =int(((k-1)/k)*nsample*r)
ParamList=list(keys)
Comparables = list(combinations(ParamList,2))


pvalLST = []
for i in range(len(Comparables)):
    t, pval = ParamFigObj.KfoldPairedTtest(r, k, n2, n1, groups.get_group(Comparables[i][0]), groups.get_group(Comparables[i][1]), 'mean_test_score', 'Phenotype')
    if pval <=0.1:
        pvalLST.append(pval)
if len(pvalLST)>0:
    RFbest.sort_values(['mean_test_score'], ascending=[False], inplace=True)
    RFbest.params = RFbest.params.astype(object)
    RFbestParams = eval(RFbest.params[0])
    if options.model=='RF':
        RFoptimal = RandomForestClassifier(random_state=RAND, class_weight=class_weight, **RFbestParams)
    elif options.model=='XGB':
        RFoptimal = XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, random_state=RAND, scale_pos_weight=len(Y==0)/len(Y==1), **RFbestParams)
elif len(pvalLST)==0:
    RFbest.sort_values(['param_n_estimators', 'param_max_depth'], ascending=[False, False], inplace=True)
    RFbest.params = RFbest.params.astype(object)
    RFbestParams = eval(RFbest.params[0])
    if options.model=='RF':
        RFoptimal = RandomForestClassifier(random_state=RAND, class_weight=class_weight, **RFbestParams)
    elif options.model=='XGB':
        RFoptimal = XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, random_state=RAND, scale_pos_weight=len(Y==0)/len(Y==1), **RFbestParams)
    print(pval, RFoptimal)
else:
    print('SOMETHING IS BROKEN')
with open('Optimal_Tuning2_'+options.sim+'.pickle', 'wb') as handle:
    pickle.dump(RFoptimal, handle, protocol=pickle.HIGHEST_PROTOCOL)