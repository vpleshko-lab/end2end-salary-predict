from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, HuberRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor
from xgboost import XGBRegressor

REGRESSION_MODELS = {
    "LinearRegression": (
        LinearRegression(),
        {"regressor__fit_intercept": [True, False]}
    ),
    "Ridge": (
        Ridge(),
        {
            "regressor__alpha": [0.1, 1.0, 10.0],
            "regressor__fit_intercept": [True, False]
        }
    ),
    "Lasso": (
        Lasso(max_iter=5000),
        {"regressor__alpha": [0.001, 0.01, 0.1, 1.0]}
    ),
    "ElasticNet": (
        ElasticNet(max_iter=5000),
        {
            "regressor__alpha": [0.001, 0.01, 0.1, 1.0],
            "regressor__l1_ratio": [0.2, 0.5, 0.8]
        }
    ),
    "SVR": (
        SVR(),
        {
            "regressor__kernel": ["linear", "rbf"],
            "regressor__C": [0.1, 1, 10]
        }
    ),
    "KNN": (
        KNeighborsRegressor(),
        {
            "regressor__n_neighbors": [3, 5, 7],
            "regressor__weights": ["uniform", "distance"]
        }
    ),
    "DecisionTree": (
        DecisionTreeRegressor(random_state=25),
        {
            "regressor__max_depth": [3, 5, 10, None]
        }
    ),
    "RandomForest": (
        RandomForestRegressor(random_state=25),
        {
            "regressor__n_estimators": [50, 100],
            "regressor__max_depth": [None, 5, 10]
        }
    ),
    "GradientBoosting": (
        GradientBoostingRegressor(random_state=25),
        {
            "regressor__n_estimators": [100, 300],
            "regressor__learning_rate": [0.01, 0.05, 0.1],
            "regressor__max_depth": [3, 5, 7],
            "regressor__min_samples_split": [2, 5, 10]
        }
    ),
    "XGBoost": (
        XGBRegressor(objective="reg:squarederror", random_state=25, n_jobs=-1),
        {
            "regressor__n_estimators": [100, 300],
            "regressor__learning_rate": [0.01, 0.05, 0.1],
            "regressor__max_depth": [3, 5, 7],
            "regressor__min_child_weight": [1, 3],
            "regressor__subsample": [0.8, 1.0],
            "regressor__colsample_bytree": [0.8, 1.0]
        }
    ),
    "Huber": (
        HuberRegressor(epsilon=1.35, alpha=0.0001),
        {
            "regressor__epsilon": [1.15, 1.35, 1.5],
            "regressor__alpha": [0.0001, 0.001, 0.01]
        }
    ),
    "HistGBM": (
        HistGradientBoostingRegressor(random_state=25),
        {
            "regressor__max_iter": [100, 200, 300],
            "regressor__learning_rate": [0.01, 0.05, 0.1],
            "regressor__max_depth": [3, 5, None],
            "regressor__min_samples_leaf": [20, 30, 50],
            "regressor__l2_regularization": [0.0, 0.1, 0.5]
        }
    ),
    "SVR": (
        SVR(),
        {
            "regressor__kernel": ["linear", "rbf"],
            "regressor__C": [0.1, 1, 10],
            "regressor__epsilon": [0.01, 0.1, 0.2]
        }
    )
}
