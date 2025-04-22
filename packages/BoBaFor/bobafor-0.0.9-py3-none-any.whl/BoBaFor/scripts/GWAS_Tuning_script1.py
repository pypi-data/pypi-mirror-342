import pandas as pd
import math
from BoBaFor.TreeTune.ClassTuning import Tuning
import BoBaFor.TreeTune.ClassParamAnalysis as PMA
import numpy as np
# import scipy.stats as stats
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from itertools import combinations
import os
# import matplotlib.pyplot as plt
from optparse import OptionParser
import pickle

usage="usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-p", "--predictor",  dest="lsbsr", help="lsbsr matrix [REQUIRED]", type="string")
parser.add_option("-r", "--response",  dest="abx", help="response vector [REQUIRED]", type="string")
parser.add_option("-s", "--simulation",  dest="sim", help="simulation identifier [REQUIRED]", type="string")
parser.add_option("-n", "--NumRandSearch",  dest="randNiter", default=100, help="Number of Random Search models to build", type="int")
parser.add_option("-k", "--numGridSearch",  dest="gridCV", default=100, help="Number of kfold cross-validation for GridSearch to perform [REQUIRED]", type="int")
parser.add_option("-t", "--numHyperGrid",  dest="gridepth", default=3, help="Number of each RandomSearchCV selected hyperparameters to run with gridsearch", type="int")
parser.add_option("-a", "--scoremetric",  dest="metric", default='roc_auc', help="scoring method to use [REQUIRED]", type="string")
parser.add_option("-o", "--output", dest="outdir", default=os.getcwd(), help="Output directory [REQUIRED]", type="string")
parser.add_option("-m", "--model", dest="model", default='RF', help="model to optimize (RF or XGB) [REQUIRED]", type="string")
# parser.add_option("-g", "--groups", dest="groups", default='Reshuffle_groups.txt', help="group_file", type="string")

options, args = parser.parse_args()

 ################################################################
#### Data Input and instantiating model.
parentDIR = os.getcwd()
numCores = -1#os.cpu_count()
print(os.cpu_count(), numCores)

TuneObj = Tuning()
X, Y, n_splits, class_weight =TuneObj.XY_index(X=options.lsbsr, Y=options.abx, BacGWASim=False)
RAND=np.random.RandomState(4)
print((X.shape))
print((Y.shape))
print((Y.value_counts()))



if options.model=='RF':
    max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
    max_depth.append(None)
    param_space= {'max_depth': max_depth,
                'max_features': ['sqrt', 'log2', None],
                # 'min_samples_leaf': [1, 2, 4, 5, 10],
                'min_samples_split': [2, 5, 10, 20],
                'n_estimators': [int(x) for x in np.linspace(start = 200, stop = 2000, num = 7)]}

    mod = RandomForestClassifier(random_state=RAND, class_weight=class_weight)

elif options.model=='XGB':
    param_space = {'learning_rate': np.logspace(-7, -3,10),
                    'n_estimators': [5, 10, 25, 50],
                    'subsample': np.linspace(0.1, 1.0, 5),
                    'colsample_bytree': np.linspace(0.05, 1, 5),
                    'max_depth':[int(x) for x in np.linspace(2,10,5)]}

    mod =  XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, colsample_bytree=int(math.sqrt(len(X.columns)))/int(len(X.columns)), random_state=RAND, scale_pos_weight=len(Y==0)/len(Y==1)) #873/236 BinaryFocalLoss

 ################################################################
#### Random Search Tuning
if not os.path.isdir('TuningOUT_' + str(options.model)):
    os.makedirs('TuningOUT_' + str(options.model))
os.chdir('TuningOUT_' + str(options.model))
TUNINGdir = os.getcwd()

print(os.getcwd())
# TuneObj.repeat = options.randCV
RF = TuneObj.Tuning_RandomSearch_classify(X=X, Y=Y, repeat=1, n_splits=n_splits, scorer=options.metric, mod=mod, hyperparameters=param_space, n_iter=options.randNiter, n_jobs=numCores, stratify=True) #, n_jobs=numCores
RF.to_csv('randSearch1_' + options.sim+'.txt', sep='\t')


 ################################################################
#### Random Search Tuning Analysis
# RF = pd.read_csv('LSBSR_RFrandSearch1_'+options.sim+'.txt', sep='\t')
ParamFigObj = PMA.Param_analysis()
# CountData = ParamFigObj.RandomSearchAnalysis(RF, 0.25, 3, 'mean_test_score', figTitle='Random Forest Parameter Count \n of Top scorers from RandomSearchCV', figname="RandSearchFIG1_"+options.sim+".png")
RFGridParamSpace = ParamFigObj.RandSearchParamGrid(RF, num_opt=options.gridepth, outdir=os.getcwd(), outfile='GridParamSpace1_'+options.sim+'.pickle')

# RFGridParamSpace = ParamFigObj.RandSearchParamGrid(RF, num_opt=options.gridepth,  outfile='RFGridParamSpace1_'+options.sim+'.pickle')

 ################################################################
#### Grid Search Tuning
TuneObj.repeat = options.gridCV
print(options.gridCV)
#options.gridCV=0
if options.gridCV==0:
    print("ENTERED NO GridSearch")
    emptyDF = pd.DataFrame(list())
    emptyDF.to_csv('gridSearch1_'+options.sim+ '.txt')
    emptyDF.to_csv('GridSearchFIG1_'+options.sim+'.png')
    # with('LSBSR_RFgridSearch1_'+options.sim+ '.txt', 'w') as file:
    #     pass
    # with('GridSearchFIG1_'+options.sim+'.png', 'w') as file:
    #     pass
    # RFGridParamSpace = ParamFigObj.RandSearchParamGrid(CountData, num_opt=1, outdir=os.getcwd(), outfile='RFOptimal_Tuning1_'+options.sim+'.pickle')
    # CountData = pd.DataFrame(CountData)
    ParamFigObj = PMA.Param_analysis()
    RF.params = RF.params.astype('str')
    RFbest = ParamFigObj.Best_mean(RF, 'mean_test_score', 10)
    RFbest.reset_index(inplace=True)
    RFbest.sort_values('mean_test_score', ascending=False, inplace=True)
    print(RFbest.columns)
    print(RFbest['params'].head(5))
    RFbest['params'] = RFbest['params'].astype(object)
    RFbestParams = eval(RFbest['params'][0])
    if options.model=='RF':
        RFoptimal = RandomForestClassifier(random_state=RAND, class_weight=class_weight, **RFbestParams)
    elif options.model =='XGB':
        RFoptimal = XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False, random_state=RAND, scale_pos_weight=len(Y==0)/len(Y==1), **RFbestParams) #873/236 BinaryFocalLoss
    with open('Optimal_Tuning1_'+options.sim+'.pickle', 'wb') as handle:
        pickle.dump(RFoptimal, handle, protocol=pickle.HIGHEST_PROTOCOL)

elif options.gridCV>0:
    print("ENTERED GridSearch")
    RF = TuneObj.Tuning_GridSearch_classify(X=X, Y=Y, repeat=TuneObj.repeat, n_splits=n_splits, scorer=options.metric, mod=mod, hyperparameters=RFGridParamSpace, n_jobs=numCores, stratify=True) #, n_jobs=numCores
    RF.to_csv('gridSearch1_'+options.sim+ '.txt', sep='\t')


    ################################################################
    #### Grid Search Tuning Analysis
    # RF =pd.read_csv('LSBSR_RFgridSearch1_'+options.sim+'.txt', sep='\t')
    ParamFigObj = PMA.Param_analysis()


    #### Plotting
    RF.params = RF.params.astype('str')
    RFbest = ParamFigObj.Best_mean(RF, 'mean_test_score', 10)
    RFTestFold =  ParamFigObj.Param_figs(RFbest, 'mean_test_score', 'LSBSR Random RF Tuning', 'param_max_depth', 'param_n_estimators') # Convert to seaborn
    RFTrainFold =  ParamFigObj.Param_figs(RFbest, 'mean_train_score', 'LSBSR Random RF Tuning', 'param_max_depth', 'param_n_estimators')
    RFTestFold.save('GridSearchFIG1_'+options.sim+'.png', dpi=300)


    #### Define best params through repeated k-fold cross validation TTest

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
    with open('Optimal_Tuning1_'+options.sim+'.pickle', 'wb') as handle:
        pickle.dump(RFoptimal, handle, protocol=pickle.HIGHEST_PROTOCOL)

else:
    print('SOMETHING IS BROKEN')
