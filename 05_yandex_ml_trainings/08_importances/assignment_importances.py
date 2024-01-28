
import pandas as pd
import numpy as np
import shap
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier

dataset = pd.read_csv(
    'https://raw.githubusercontent.com/girafe-ai/ml-course/23f_basic/homeworks/lab01_ml_pipeline/car_data.csv',
    delimiter=',', header=None).values
data = dataset[:, :-1].astype(int)
target = dataset[:, -1]
binary_subset = np.array([x in ['bus', 'opel'] for x in target])
data, target = data[binary_subset], target[binary_subset]

# do not change the code in the block below
# __________start of block__________
submission_dict = {}
# __________end of block__________

# Ensure the correct data subsets are used for logistic regression
# X_train_basic, y_train_basic = data[:350, 1:], target[:350]
X_train, y_train = data[:350, 1:], target[:350]
X_val, y_val = data[350:, 1:], target[350:]

# Estimating features importances using logistic regression coefficients.
# # Train basic logistic regression and save its coefficients (weights).
# lr_basic = LogisticRegression(max_iter=1000)
# lr_basic.fit(X_train, y_train)
#
# # Find the Logistic Regression weights and save them to the variable `lr_basic_coef`:
# lr_basic_coef = lr_basic.coef_

# Train basic logistic regression on the subsetted data
lr_basic = LogisticRegression(max_iter=2000)
lr_basic.fit(X_train, y_train)

# Get the Logistic Regression weights and save them to the variable `lr_basic_coef`:
lr_basic_coef = lr_basic.coef_

# do not change the code in the block below
# __________start of block__________
submission_dict['lr_basic_coef'] = lr_basic_coef
# __________end of block__________

# Estimating features importances using logistic regression coefficients.
# Train basic logistic regression on scaled data and save its coefficients (weights) as well
lr_scaled = LogisticRegression(max_iter=2000)

# Use `StandardScaler` on your data.
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

lr_scaled.fit(X_train_scaled, y_train)

# Save model coefficients to the variable `lr_scaled_coef`:
lr_scaled_coef = lr_scaled.coef_

# Save index of the most important feature for lr_scaled to the variable `lr_scaled_most_important_index`:
lr_scaled_most_important_index = np.argmax(np.abs(lr_scaled_coef))

# do not change the code in the block below
# __________start of block__________
# assert isinstance(int(lr_scaled_most_important_index), int)
submission_dict['lr_scaled_coef'] = lr_scaled_coef
submission_dict['lr_scaled_most_important_index'] = lr_scaled_most_important_index
# __________end of block__________

# Estimating features importances for logistic regression using shap
# Use shap library to check the importance of the features. Use Linear explainer and the scaled data.
explainer = shap.LinearExplainer(lr_scaled, X_train_scaled)
shap_values_scaled = explainer.shap_values(X_train_scaled)

# Finally, write a function which transforms shap values to Logistic Regression coefficients.
# Note: This task main goal is your deeper understanding of the shap importance estimation process.
def get_coef_from_shap_values(shap_values, X_train_scaled):
    w = shap_values * (X_train_scaled - X_train_scaled.mean(0))
    return w.mean(0)

coef_from_shap = get_coef_from_shap_values(shap_values_scaled, X_train_scaled)

# # Training the GradientBoosting
# gb_basic = GradientBoostingClassifier(n_estimators=10)
# gb_basic.fit(X_train, y_train)
#
# gb_basic_feature_importances = gb_basic.feature_importances_

# Train GradientBoostingClassifier on unscaled data
gb_basic = GradientBoostingClassifier(n_estimators=100)
gb_basic.fit(X_train, y_train)

gb_basic_feature_importances = gb_basic.feature_importances_

gb_scaled = GradientBoostingClassifier(n_estimators=100)
gb_scaled.fit(X_train_scaled, y_train)

gb_scaled_feature_importances = gb_scaled.feature_importances_

# do not change the code in the block below
# __________start of block__________
submission_dict['gb_basic_feature_importances'] = gb_basic_feature_importances
# __________end of block__________

explainer = shap.TreeExplainer(gb_scaled)
shap_values = explainer.shap_values(X_train)

gb_scaled_most_important_index = np.argmax(np.abs(gb_scaled_feature_importances))

# do not change the code in the block below
# __________start of block__________
submission_dict['gb_scaled_most_important_index'] = gb_scaled_most_important_index
# __________end of block__________

# do not change the code in the block below
# __________start of block__________
np.save('2_submission_dict_hw08.npy', submission_dict, allow_pickle=True)
print('File saved to `2_submission_dict_hw.npy`')
# __________end of block__________
