# import timeit
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import chi2_contingency#, false_discovery_control
import statsmodels.stats.multitest as multi
# from BoBaFor.ClassIndexing import Indexing
from BoBaFor.TreeTune.ClassIndexing import Indexing 

class Tuning(Indexing):
    """
    Tuning of machine learning models

    Attributes
    ----------
    n_splits: int
        The K in K-fold cross-validation
    repeat: int
        The number of repetions to perform on different k splits
    n_jobs: int
        The number of cores to use to parallelize
    class_weight: str or None
        assigns the class wheight to either None or 'balanced'


    Methods
    ----------
    _timer_func
        A timer decorator function
    XY_index
        Aligns predictor and repsonse indices and calculates optimal n_splits and class_weight
    Tuning_RandomSearch_classify
        Using RandomSearch to preliminarily investigate large hyperparameter space to find subset of that space to evaluate further with GridSearch.
    Tuning_GridSearch_classify
        Using GridSearch to thoroughly investigate hyperparameter space to find optimal model for the given dataset.

    """
    def __init__(self, n_splits=None, repeat=None, n_jobs=None, class_weight=None):
        self.n_splits = n_splits
        self.repeat = repeat
        self.n_jobs = n_jobs
        self.class_weight = class_weight

    def chi2_Sim_Test(self, Predictor, Response): 
        FeaturesLST = Predictor.columns.to_list()
        DF = Response.merge(Predictor, how='inner', left_index=True, right_index=True)
        plst=[]
        crssTb = []
        
        for col in Predictor:
            CT2 = pd.crosstab(DF['response'], DF[col])
            stat, p, dof, expected = chi2_contingency(CT2)
            plst.append(p)
            crssTb.append(CT2)
        padj = multi.fdrcorrection(plst, alpha=0.05, method='indep', is_sorted=False)[1]
        df = pd.DataFrame({'Col':FeaturesLST, 'Pval':plst, 'Padj':padj}).sort_values(['Padj'], ascending=True)
        return df
    
    @Indexing._timer_func
    def Tuning_RandomSearch_classify(self, X, Y, repeat, n_splits, scorer, mod, hyperparameters, n_iter,  n_jobs=None, stratify=True): #n_jobs=None,
        """
        Using RandomSearch to preliminarily investigate large hyperparameter space to find subset of that space to evaluate further with GridSearch.

        Parameters
        ----------
        X : dataframe
            Predictor or Feature dataframe
        Y : series
            Repsonse variables
        repeat : int
            Number of stratified k-fold cross validations to perform
        n_splits: int
            number of splits in k-fold cross validation
        scorer : str
            Metric of which to compare model performance to calculate subsequent feature importances
        mod : model object
            scikit learn style model (e.g. Random Forest, XGBoost, logistic, or linear).
        hyperparameters : dict
            A dictionary of all hyperparameter keys and associated values desired to be tuned.
        n_iter: int
            The number of hyperparameters tested per each k-fold cross-validation splitting
        n_jobs : int
            The number of cores to utilize in parallelization
        """
        print("Number of k-fold cross-validations run is: " + str(repeat))
        print("Number of hyperparamter iterations tested is: " + str(n_iter))
        dfL = []
        for i in range(0,repeat):
            if stratify==True:
                cv = StratifiedKFold(n_splits=n_splits, random_state=i, shuffle=True) 
            else:
                cv = KFold(n_splits=n_splits, random_state=i, shuffle=True)
            boosted_grid = RandomizedSearchCV(mod, hyperparameters, random_state=mod.random_state, n_iter=n_iter, scoring=scorer, cv=cv, verbose=0, refit=True, error_score=np.nan, return_train_score=True, n_jobs=n_jobs) #n_jobs=n_jobs
            grid_fit = boosted_grid.fit(X, Y)
            DF = pd.DataFrame(grid_fit.cv_results_)
            DF['Iteration'] = i
            dfL.append(DF)
        DFall = pd.concat(dfL)
        return DFall

    @Indexing._timer_func
    def Tuning_GridSearch_classify(self, X, Y, repeat, n_splits, scorer, mod, hyperparameters,  n_jobs=None, stratify=True): #n_jobs=None,
        """
        Using GridSearch to thoroughly investigate hyperparameter space to find optimal model for the given dataset..

        Parameters
        ----------
        X : dataframe
            Predictor or Feature dataframe
        Y : series
            Repsonse variables
        repeat : int
            Number of stratified k-fold cross validations to perform
        n_splits: int
            number of splits in k-fold cross validation
        scorer : str
            Metric of which to compare model performance to calculate subsequent feature importances
        mod : model object
            scikit learn style model (e.g. Random Forest, XGBoost, logistic, or linear).
        hyperparameters : dict
            A dictionary of all hyperparameter keys and associated values desired to be tuned.
        n_jobs : int
            The number of cores to utilize in parallelization
        """
        print("Number of repeats run is: " + str(repeat))
        dfL = []
        for i in range(0,repeat):
            if stratify==True:
                cv = StratifiedKFold(n_splits=n_splits, random_state=i, shuffle=True) 
            else:
                cv = KFold(n_splits=n_splits, random_state=i, shuffle=True)
            boosted_grid = GridSearchCV(mod, hyperparameters, scoring=scorer, cv=cv, verbose=0, refit=True, error_score=np.nan, return_train_score=True, n_jobs=n_jobs) #n_jobs=n_jobs,
            grid_fit = boosted_grid.fit(X, Y)
            DF = pd.DataFrame(grid_fit.cv_results_)
            DF['Iteration'] = i
            dfL.append(DF)
        DFall = pd.concat(dfL)
        return DFall