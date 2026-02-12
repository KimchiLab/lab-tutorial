# %% Import sklearn and other needed libraries
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, precision_score, recall_score, f1_score
from sklearn.inspection import PartialDependenceDisplay
from sklearn.linear_model import LinearRegression, ElasticNet, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
import warnings
from os import chdir
from os import path
warnings.filterwarnings('ignore')
scriptpath = path.realpath(__file__)
parentDirInd = scriptpath.find("03_Scripts")
parent_dir = scriptpath[0:parentDirInd]
chdir(parent_dir)

# Define lists to itererate thorough the creation of different datasets
# using sklearn.make_classification
dataset_params = {
    'n_samples': [100, 200, 500, 1000],
    'n_features': [50, 150, 300, 600, 1000],
    'imbalance_ratios': [0.1, 0.2, 0.3, 0.4],
    'class_sep': [0.8, 1.0, 1.2, 1.4]
}

n_samples = dataset_params['n_samples']
n_features = dataset_params['n_features']
imbalance_ratios = dataset_params['imbalance_ratios']
class_sep = dataset_params['class_sep']

# Static parameters for the dataset creation
n_informative = 40
n_classes = 2

# %% Create a library of possible hyperparameters for XGBoost to be used in the grid search
param_grid = {
    'classifier__max_depth': range(2, 11),  # Maximum depth of the trees
    'classifier__min_child_weight': range(1, 5),  # Regularization parameter
    'classifier__n_estimators': np.logspace(1, 5, num=5, base=5.0).astype(int),
    'classifier__learning_rate': np.logspace(-2, 0, num=5, base=10.0),
    'classifier__scale_pos_weight': range(1, 5),  # Balancing classes
    'classifier__colsample_bytree': np.arange(0.5, 1, 0.1)
}


# Create the pipeline for the grid search
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', xgb.XGBClassifier(random_state=42, eval_metric='logloss'))
])

# Define the cross validation strategy to be used in the grid search
cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


# Iteratively fit the models and save the results in a dataframe
# Store the characteristics of the dataset, the hyperparameters used and
# performance metrics: roc_auc, balanced_accuracy, precision, recall, f1_score

results = []

# Generate all combinations of dataset parameters
for n_sample, n_feature, imbalance_ratio, class_separation in product(
    dataset_params['n_samples'],
    dataset_params['n_features'],
    dataset_params['imbalance_ratios'],
    dataset_params['class_sep']
):
    print(f"Processing: n_samples={n_sample}, n_features={n_feature}, imbalance_ratio={imbalance_ratio}, class_sep={class_separation}")
    
    # Calculate weights for imbalanced dataset
    n_majority = int(n_sample * (1 - imbalance_ratio))
    n_minority = n_sample - n_majority
    weights = [n_minority / n_sample, n_majority / n_sample]
    n_redundant = int(n_feature/5)
    
    # Create synthetic dataset
    X, y = make_classification(
        n_samples=n_sample,
        n_features=n_feature,
        n_informative=min(n_informative, n_feature),
        n_redundant=min(n_redundant, n_feature - min(n_informative, n_feature)),
        n_classes=n_classes,
        weights=weights,
        class_sep=class_separation,
        random_state=42
    )
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Perform grid search
    hyperparam_search = RandomizedSearchCV(
        pipeline, 
        param_grid, 
        cv=cv_strategy, 
        scoring='roc_auc', 
        n_jobs=-1,
        verbose=0
    )
    
    # Fit the model
    hyperparam_search.fit(X_train, y_train)
    
    # Make predictions
    y_pred = hyperparam_search.predict(X_test)
    y_pred_proba = hyperparam_search.predict_proba(X_test)[:, 1]
    
    # Calculate metrics
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    balanced_acc = balanced_accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    # Store results
    result = {
        'n_samples': n_sample,
        'n_features': n_feature,
        'imbalance_ratio': imbalance_ratio,
        'class_separation': class_separation,
        'roc_auc': roc_auc,
        'balanced_accuracy': balanced_acc,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'best_params': hyperparam_search.best_params_
    }
    
    results.append(result)

# Convert to DataFrame
results_df = pd.DataFrame(results)
print(f"\nCompleted {len(results_df)} experiments")
print(results_df.head())
results_df.to_csv('04_Outputs/03_Data/xgboost_performance_results.csv', index=False)


# %% Take resulting dataframe and fit the performance of each model
# to the dataset parameters using linear regression

if not ('results_df' in locals()):
    results_df = pd.read_csv('04_Outputs/03_Data/xgboost_performance_results.csv')

# Prepare features (dataset characteristics) and targets (performance metrics)
param_cols = ['n_samples', 'n_features', 'imbalance_ratio', 'class_separation']
selected_metrics = ['roc_auc'] # , 'balanced_accuracy', 'f1_score']


X_reg = results_df[param_cols]
regression_results = {}

print("\nFitting regression models for each metric:")

for metric in selected_metrics:
    y_reg = results_df[metric]
    
    # Fit regression
    reg = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
    reg.fit(X_reg, y_reg)
    
    # Store results
    regression_results[metric] = {
        'model': reg,
        'r2_score': reg.score(X_reg, y_reg),
    }
    print(f"{metric}: R^2 Score = {regression_results[metric]['r2_score']:.4f}")


# %%Plot the results of the linear regression to see how the dataset
# parameters affect the performance of the model

for metric in selected_metrics:
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")

    # Create a comprehensive visualization
    dim_subplots = len(dataset_params)
    fig, axes = plt.subplots(dim_subplots, dim_subplots, figsize=(2.5*dim_subplots, 2.3*dim_subplots))
    metric_name = metric.replace("_", " ").title()
    fig.suptitle(f"XGBoost {metric_name} Across Dataset Characteristics", fontsize=16, fontweight='bold')

    # Plotting a correlation type matrix for comparison

    # Iterate though each dataset parameter
    for i, param_x in enumerate(param_cols):
        for j, param_y in enumerate(param_cols):
            if i < j:
                #Rempove upper triangle to avoid redundancy
                axes[i, j].set_visible(False)
                continue

            ax = axes[i, j]
            if i == j:
                # Diagonal: Plot partial dependence of the metric on the single parameter
                PartialDependenceDisplay.from_estimator(
                    regression_results[metric]['model'], 
                    X_reg, 
                    [(param_x)], 
                    ax=ax, 
                    kind='average'
                )
                ax.set_xticks([])
                ax.set_xticks(sorted(X_reg[param_x].unique()))

            else:
                # Plot two way partial dependence between two parameters
                PartialDependenceDisplay.from_estimator(
                    regression_results[metric]['model'], 
                    X_reg, 
                    [(param_x, param_y)], 
                    ax=ax,
                )

    # Show and save the final plot
    plt.tight_layout()
    plt.savefig(f'04_Outputs/01_Figures/xgboost_performance_analysis_{metric_name}.png', dpi=300)
    plt.show()

# %%
