"""
JDIS Machine Learning Package

Training and evaluation scripts. Individual modules import their siblings by
bare name (``from experiment_utils import ...``) and are therefore designed to
be run directly, e.g. ``python src/ml/feature_ablation.py``, which places this
directory on ``sys.path``. Invoking them as ``python -m src.ml.<module>`` also
works because this directory is first on the path in that form.
"""
