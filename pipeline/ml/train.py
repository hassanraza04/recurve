"""Train the churn model.

Scaffold only — built in P5. Two honesty constraints are fixed now because they
decide whether the model is real or a demo prop:

  1. No target leakage. Features are computed strictly from data available
     *before* the churn label window. Anything that encodes the outcome (e.g.
     a cancellation timestamp inside the feature window) is excluded.
  2. Honest evaluation. We report precision@k for the top-k at-risk accounts a
     CS team could actually call this week — not a flattering global AUC.
"""

from __future__ import annotations


def train_churn_model() -> None:
    """Fit the model on labeled, leakage-free features and persist the artifact.

    TODO(P5): build features from the marts, time-split train/test, fit a
    gradient-boosted / logistic baseline, evaluate precision@k, save the model.
    """
    raise NotImplementedError("churn training lands in P5")


if __name__ == "__main__":
    train_churn_model()
