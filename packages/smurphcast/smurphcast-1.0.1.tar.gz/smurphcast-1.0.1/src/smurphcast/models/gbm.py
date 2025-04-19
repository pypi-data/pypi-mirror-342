from __future__ import annotations
import pandas as pd
import lightgbm as lgb
from ..features.time_feats import make_time_features
from ..features.lag_feats import add_lag_features, add_rolling_features

_EXCLUDE = {"ds", "y", "y_transformed"}


class GBMModel:
    """
    LightGBM regression for bounded KPIs with calendar + lag + rolling features.
    """

    def __init__(
        self,
        *,
        num_leaves: int = 31,
        n_estimators: int = 300,
        lags: tuple[int, ...] = (1, 7, 14),
        rolls: tuple[int, ...] = (4, 12),
    ):
        self.params = dict(
            objective="regression",
            metric="l2",
            learning_rate=0.05,
            num_leaves=num_leaves,
            verbosity=-1,
        )
        self.n_estimators = n_estimators
        self.lags = lags
        self.rolls = rolls
        self.model: lgb.Booster | None = None
        self._feature_cols: list[str] | None = None

    # --------------------------------------------- #
    def _build_X(self, df: pd.DataFrame) -> pd.DataFrame:
        feats = make_time_features(df)
        feats = add_lag_features(feats, lags=self.lags)
        feats = add_rolling_features(feats, windows=self.rolls)
        cols = [c for c in feats.columns if c not in _EXCLUDE]
        return feats[cols]

    # --------------------------------------------- #
    def fit(self, df: pd.DataFrame, y_col: str = "y_transformed"):
        X = self._build_X(df).dropna()
        y = df.loc[X.index, y_col]
        self._feature_cols = list(X.columns)

        dataset = lgb.Dataset(X, y)
        self.model = lgb.train(self.params, dataset, num_boost_round=self.n_estimators)
        return self

    # --------------------------------------------- #
    def _prep_future(self, future_df: pd.DataFrame) -> pd.DataFrame:
        Xf = self._build_X(future_df)
        # ensure same columns & order as training set
        Xf = Xf.reindex(columns=self._feature_cols, fill_value=0)
        return Xf.ffill().bfill()

    # --------------------------------------------- #
    def predict(self, future_df: pd.DataFrame):
        if self.model is None:
            raise RuntimeError("Call .fit() first.")
        Xf = self._prep_future(future_df)
        return self.model.predict(Xf)
