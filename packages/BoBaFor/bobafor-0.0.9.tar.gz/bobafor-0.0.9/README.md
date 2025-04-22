# BoBaFor
* a bacterial genome wide association approach through utilizing machine learning practices.
## installation
### Create Conda Virtual Environment with required python version
```bash
conda create -n BoBaFor_env python==3.11.10
```
### Activate BoBaFor_env
```bash
conda activate BoBaFor_env
```
### install BoBaFor via pip
```bash
pip install BoBaFor
```
## Use
### Download example from GitHub
```bash
git clone https://github.com/PaulDanPhillips/BoBaFor.git
```
### **c**hange **d**irectory to example
```bash
cd BoBaFor/examples
```
### Convert relative paths to absolute in example_config.yaml
```bash
python AddAbsolutePaths.py
```
### Run the example data (user needs to pay attention to how many cores they have available and want to use)
```bash
BoBaFor --config example_config.yaml --cores 4
```
## Running your own data:
### Data organization
* The data needs to be split into two files: 1 containing all of the genetic features and 2 the response phenotype ensureing that the indexes on the feature matrix align with the reponse vector.
#### Configure.yaml file:

* You will edit the Sim1.yaml file from the example directory.
1. **Predictor**
    * The absolute or relative path to your genetic feature matrix will take the place of """balanced_features/Strongest_Sim1.txt"""
    * /path/to/data/features.txt
2. **Response**
    * The absolute or relative path to your response phenotype vector will take the place of """balanced_responses/Sim1.txt"""
    /path/to/daata/response.txt
3. ***chi2Correct**
    * The user need to decie if they want to the chi2 prefilter step to be corrected via false-discovery-rate or not (only True or False)
    * True/False
4. **FDRchi2Thresh**
    * The user needs to decide what the FDR chi2 threshold is for removing genetic features based on this chi2 test is. 
    * 0.-1. (float)
5. **PreFilterFileName**
    * The name you want for the output files from just the chi2-prefilter step.
    * Prefilter_Experiment_Name
6. **sim**
    * Experiment Name for prefix file name 
    * Simulation1
7. **GridParamDepth**
    * The number of of options to keep for EVERY hyperparameter after optimizing from RandomSearch leading into the much more thorough and computational demanding GridSearch
    * 1-5 (int)
8. **ScoreMetric**
    * What metric to use to score the model. Pay attention to what type of data your response metric is and how balanced the data is.
    * balanced_accuracy
9. **RandSearch1_Niter**
    * The number of RandomSearch iterations to perform prior to boruta selection (The number of hyperparamter combinations to test)
    * (int)
10. **GridSearch1_CV**
    * The number of GridSearch iterations to perform prior to boruta selection (The number of times to create kfold splits and test EVERY possible hyperparameter combination)
    * (int)
11. boruta_perc
    * The percent strength of the boruta shadow-features to be comparted against the real features.
    * 0-100 (int)
12. boruta_pval
    * Level at which the corrected p-values will get rejected in both correction steps.
    * 0.-1. (float)
13. borutaSelect_perc
    * The percent theshold of which to select final features (the number of times a feature was selected divided by the number of iterations boruta was run).
14. collect
    * A boolean on whether to keep all selected features no matter the boruta_Select_perc setting.
    * True/False 
15. boruta_reps
    * The number of iterations to run boruta selection.
16. model
    * Whether to run a random forest or extreme gradient boosted model
    * RF/XGB
17. RandSearch2_Niter
    * The number of RandomSearch iterations to perform after boruta selection (The number of hyperparamter combinations to test)
    * (int)
18. RandSearch2_CV
    * TO BE REMOVED
    * The number of iterations to create kfolds within a single RandSearch2_Niter.
    * (int)
19. GridSearch2_CV
    * The number of GridSearch iterations to perform after boruta selection (The number of times to create kfold splits and test EVERY possible hyperparameter combination)
    (int)
20. RankingFeatureIters
    * The number of iterations to perform feature ranking via Feature Importance or Permutation Importance
    * (int)
21. PermImpInteralIter
    * The number of internal repetitions for Permutation Importance
    * (int)

#### Output files:
* Most important is **BorutaOUT_1.00.05_RF/FinalFeatures_RF/eatureImportance_Ranked_*.out** as it contains the genentic variants and their associated feature importance value.
* Lots of information and plots on how the random forest tuning performed.
    1. LSBSR_RFrandSearch1_*.txt contains the raw scores for the k-fold fitting from the first randomsearch
    2. LSBSR_RFgridSearch1_*.txt contains the raw scores for the k-fold fitting from the first gridsearch
    3. LSBSR_RFrandSearch2_*.txt contains the raw scores for the k-fold fitting from the second/final randomsearch
    4. LSBSR_RFgridSearch2_*.txt contains the raw scores for the k-fold fitting from the second/final gridsearch
