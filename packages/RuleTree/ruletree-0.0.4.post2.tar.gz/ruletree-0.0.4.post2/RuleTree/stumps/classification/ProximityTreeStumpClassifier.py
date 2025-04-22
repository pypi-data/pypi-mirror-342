import copy
import random
import warnings

import numpy as np
import psutil
import tempfile312
from matplotlib import pyplot as plt
from numba import UnsupportedError

from RuleTree.stumps.classification.DecisionTreeStumpClassifier import DecisionTreeStumpClassifier
from RuleTree.utils.define import DATA_TYPE_TS
from RuleTree.utils.shapelet_transform.Shapelets import Shapelets


class ProximityTreeStumpClassifier(DecisionTreeStumpClassifier):
    """A decision stump classifier for time series data using shapelet-based proximity measures.

    This classifier transforms time series data using shapelets (subsequences of time series)
    and creates decision rules based on the distances between the input time series and
    extracted shapelets.

    Parameters
    ----------
    n_shapelets : int, default=cpu_count*2
        The number of shapelets to be used for classification.
    n_shapelets_for_selection : int or str, default=500
        Number of shapelets to select or 'stratified' for stratified selection.
    n_ts_for_selection_per_class : int, default=100
        Number of time series per class to use for shapelet extraction.
    sliding_window : int, default=50
        The length of the sliding window used to extract shapelets from time series.
    selection : str, default='mi_clf'
        Method for shapelet selection. Options: 'random', 'mi_clf', 'cluster'.
    distance : str, default='euclidean'
        Distance metric used for comparing shapelets to time series.
    mi_n_neighbors : int, default=100
        Number of neighbors for mutual information calculation.
    random_state : int, default=42
        Seed for random number generation for reproducibility.
    n_jobs : int, default=1
        Number of parallel jobs to run for shapelet extraction.
    **kwargs
        Additional parameters for the base DecisionTreeStumpClassifier.
    """
    def __init__(self,
                 n_shapelets=psutil.cpu_count(logical=False) * 2,
                 n_shapelets_for_selection=500,  # int, inf, or 'stratified'
                 n_ts_for_selection_per_class=100,  # int, inf
                 sliding_window=50,
                 selection='mi_clf',  # random, mi_clf, mi_reg, cluster
                 distance='euclidean',
                 mi_n_neighbors=100,
                 random_state=42, n_jobs=1,
                 **kwargs):
        self.n_shapelets = n_shapelets
        self.n_shapelets_for_selection = n_shapelets_for_selection
        self.n_ts_for_selection_per_class = n_ts_for_selection_per_class
        self.sliding_window = sliding_window
        self.selection = selection
        self.distance = distance
        self.mi_n_neighbors = mi_n_neighbors
        self.random_state = random_state
        self.n_jobs = n_jobs

        if "max_depth" in kwargs and kwargs["max_depth"] > 1:
            warnings.warn("max_depth must be 1")

        kwargs["max_depth"] = 1

        if selection not in ['random', 'mi_clf', 'cluster']:
            raise ValueError("'selection' must be 'random', 'mi_clf' or 'cluster'")

        super().__init__(**kwargs)

        self.kwargs |= {
            "n_shapelets": n_shapelets,
            "n_shapelets_for_selection": n_shapelets_for_selection,
            "n_ts_for_selection_per_class": n_ts_for_selection_per_class,
            "sliding_window": sliding_window,
            "selection": selection,
            "distance": distance,
            "mi_n_neighbors": mi_n_neighbors,
            "random_state": random_state,
            "n_jobs": n_jobs,
        }

    def fit(self, X, y, idx=None, context=None, sample_weight=None, check_input=True):
        """Fit the ProximityTreeStumpClassifier on the training data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_timepoints)
            The time series data.
        y : array-like of shape (n_samples,)
            The target values.
        idx : array-like or slice, default=None
            Indices of the samples to be used for training.
        context : object, default=None
            Additional context information (not used).
        sample_weight : array-like, default=None
            Sample weights (not supported for this classifier).
        check_input : bool, default=True
            Whether to check the input parameters.

        Returns
        -------
        self : object
            Fitted estimator.

        Raises
        ------
        UnsupportedError
            If sample_weight is provided.
        """
        if idx is None:
            idx = slice(None)
        X = X[idx]
        y = y[idx]

        self.y_lims = [X.min(), X.max()]

        random.seed(self.random_state)
        if sample_weight is not None:
            raise UnsupportedError(f"sample_weight is not supported for {self.__class__.__name__}")

        self.st = Shapelets(n_shapelets=self.n_shapelets,
                            n_shapelets_for_selection=self.n_shapelets_for_selection,
                            n_ts_for_selection_per_class=self.n_ts_for_selection_per_class,
                            sliding_window=self.sliding_window,
                            selection=self.selection,
                            distance=self.distance,
                            mi_n_neighbors=self.mi_n_neighbors,
                            random_state=random.randint(0, 2**32-1),
                            n_jobs=self.n_jobs
                            )

        X_dist = self.st.fit_transform(X, y)
        actual_n_shapelets = X_dist.shape[1]
        X_bool = np.zeros((X.shape[0], actual_n_shapelets*(actual_n_shapelets-1)), dtype=bool)

        c = 0

        for i in range(actual_n_shapelets):
            for j in range(i+1, actual_n_shapelets):
                X_bool[:, c] = X_dist[:, i] <= X_dist[:, j]
                c += 1

        return super().fit(X_bool, y=y, sample_weight=sample_weight, check_input=check_input)

    def apply(self, X, check_input=False):
        """Apply the decision tree stump to X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_timepoints)
            The time series data to classify.
        check_input : bool, default=False
            Whether to check the input parameters.

        Returns
        -------
        X_leaves : array-like of shape (n_samples,)
            For each datapoint x in X, returns the leaf node it ends up in.
        """
        self.y_lims = [min(self.y_lims[0], X.min()), min(self.y_lims[1], X.max())]
        X_dist = self.st.transform(X)
        actual_n_shapelets = X_dist.shape[1]
        X_bool = np.zeros((X.shape[0], actual_n_shapelets * (actual_n_shapelets - 1)), dtype=bool)

        c = 0

        for i in range(actual_n_shapelets):
            for j in range(i + 1, actual_n_shapelets):
                X_bool[:, c] = X_dist[:, i] <= X_dist[:, j]
                c += 1


        return super().apply(X_bool, check_input=check_input)

    def supports(self, data_type):
        """Check if the classifier supports the given data type.

        Parameters
        ----------
        data_type : int
            Data type identifier.

        Returns
        -------
        bool
            True if the data type is supported, False otherwise.
        """
        return data_type in [DATA_TYPE_TS]


    def get_rule(self, columns_names=None, scaler=None, float_precision: int | None = 3):
        """Generate a human-readable rule representation of the decision stump.

        Creates textual and visual representations of the shapelet-based decision rule.

        Parameters
        ----------
        columns_names : list, default=None
            Names of the features (not used for time series).
        scaler : object, default=None
            Scaler used for normalization (not supported for this classifier).
        float_precision : int or None, default=3
            Number of decimal places to use for floating-point values.

        Returns
        -------
        dict
            Dictionary containing textual and visual representations of the rule.

        Raises
        ------
        UnsupportedError
            If a scaler is provided.
        """
        rule = {
            "feature_idx": self.feature_original[0],
            "threshold": self.threshold_original[0],
            "is_categorical": self.is_categorical,
            "samples": self.n_node_samples[0]
        }

        rule["feature_name"] = f"Shapelet_{rule['feature_idx']}"

        if scaler is not None:
            raise UnsupportedError(f"Scaler not supported for {self.__class__.__name__}")

        comparison = "<="
        not_comparison = ">"

        f = self.feature_original[0]
        shapes_idx = None
        c = 0
        for i in range(self.st.shapelets.shape[0]):
            for j in range(i + 1, self.st.shapelets.shape[0]):
                if c == f:
                    shapes_idx = (i, j)
                c += 1

        with tempfile312.NamedTemporaryFile(delete_on_close=False,
                                            delete=False,
                                            suffix=".png",
                                            mode="wb") as temp_file:
            plt.figure(figsize=(2, 1))
            shape = self.st.shapelets[shapes_idx[0], 0]
            plt.plot([i for i in range(shape.shape[0])], shape, color="tab:green", alpha=0.7)
            shape = self.st.shapelets[shapes_idx[1], 0]
            plt.plot([i for i in range(shape.shape[0])], shape, color="tab:red", alpha=0.7)
            plt.ylim(*self.y_lims)
            plt.xlim(0, shape.shape[0])
            plt.gca().tick_params(axis='both', which='both', length=2, labelsize=6)
            plt.gca().spines['right'].set_color('none')
            plt.gca().spines['top'].set_color('none')
            #plt.gca().spines['bottom'].set_position('zero')
            plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
            plt.savefig(temp_file, format="png", dpi=300, bbox_inches='tight', pad_inches=0)
            plt.close()

        rule["textual_rule"] = f"{self.distance}(TS, green_shp)\n{comparison} {self.distance}(TS, red_shp)"
        rule["blob_rule"] = f"{self.distance}(TS, green_shp)\n{comparison} {self.distance}(TS, red_shp)"
        rule["graphviz_rule"] = {
            "image": f'{temp_file.name}',
            "imagescale": "true",
            "imagepos": "bc",
            "label": f"{self.distance}(TS, green_shp)\n\u2264 {self.distance}(TS, red_shp)",
            "labelloc": "t",
            "fixedsize": "true",
            "width": "2",
            "height": "1.33",
            "shape": "none",
            "fontsize": "8",
        }

        rule["not_textual_rule"] = f"{self.distance}(TS, green_shp)\n{not_comparison} {self.distance}(TS, red_shp)"
        rule["not_blob_rule"] = f"{self.distance}(TS, green_shp)\n{not_comparison} {self.distance}(TS, red_shp)"
        rule["not_graphviz_rule"] = {
            "image": f'{temp_file.name}',
            "imagescale": "true",
            "label": f"{self.distance}(TS, green_shp)\n{not_comparison} {self.distance}(TS, red_shp)",
            "imagepos": "bc",
            "labelloc": "t",
            "fixedsize": "true",
            "width": "2",
            "height": "1.33",
            "shape": "none",
            "fontsize": "8",
        }

        return rule

    def node_to_dict(self):
        """Convert the decision stump to a dictionary representation.

        This method is used for model serialization.

        Returns
        -------
        dict
            Dictionary representing the decision stump, including shapelet information.
        """
        rule = super().node_to_dict() | {
            'stump_type': self.__class__.__module__,
            "feature_idx": self.feature_original[0],
            "threshold": self.threshold_original[0],
            "is_categorical": self.is_categorical,
            "samples": self.n_node_samples[0]
        }

        rule["feature_name"] = f"Shapelet_{rule['feature_idx']}"

        comparison = "<="
        not_comparison = ">"

        rule["textual_rule"] = f"{self.distance}(TS, green_shp)\n{comparison} {self.distance}(TS, red_shp)"
        rule["blob_rule"] = f"{self.distance}(TS, green_shp)\n{comparison} {self.distance}(TS, red_shp)"
        rule["graphviz_rule"] = {
            "image": f'None',
            "imagescale": "true",
            "imagepos": "bc",
            "label": f"{self.distance}(TS, green_shp)\n{comparison} {self.distance}(TS, red_shp)",
            "labelloc": "t",
            "fixedsize": "true",
            "width": "2",
            "height": "1.33",
            "shape": "none",
            "fontsize": "8",
        }

        rule["not_textual_rule"] = f"{self.distance}(TS, green_shp)\n{not_comparison} {self.distance}(TS, red_shp)"
        rule["not_blob_rule"] = f"{self.distance}(TS, green_shp)\n{not_comparison} {self.distance}(TS, red_shp)"
        rule["not_graphviz_rule"] = {
            "image": f'{None}',
            "imagescale": "true",
            "label": f"{self.distance}(TS, green_shp)\n{not_comparison} {self.distance}(TS, red_shp)",
            "imagepos": "bc",
            "labelloc": "t",
            "fixedsize": "true",
            "width": "2",
            "height": "1.33",
            "shape": "none",
            "fontsize": "8",
        }

        # shapelet transform stuff
        rule["shapelets"] = self.st.shapelets.tolist()
        rule["n_shapelets"] = self.st.n_shapelets
        rule["n_shapelets_for_selection"] = self.st.n_shapelets_for_selection
        rule["n_ts_for_selection_per_class"] = self.st.n_ts_for_selection_per_class
        rule["sliding_window"] = self.st.sliding_window
        rule["selection"] = self.st.selection
        rule["distance"] = self.st.distance
        rule["mi_n_neighbors"] = self.st.mi_n_neighbors
        rule["random_state"] = self.st.random_state
        rule["n_jobs"] = self.st.n_jobs
        rule["y_lims"] = self.y_lims

        return rule

    @classmethod
    def dict_to_node(cls, node_dict, X=None):
        self = cls(
            n_shapelets=node_dict["n_shapelets"],
            n_shapelets_for_selection=node_dict["n_shapelets_for_selection"],
            n_ts_for_selection_per_class=node_dict["n_ts_for_selection_per_class"],
            sliding_window=node_dict["sliding_window"],
            selection=node_dict["selection"],
            distance=node_dict["distance"],
            mi_n_neighbors=node_dict["mi_n_neighbors"],
            random_state=node_dict["random_state"],
            n_jobs=node_dict["n_jobs"]
        )

        self.st = Shapelets(
            n_shapelets=node_dict["n_shapelets"],
            n_shapelets_for_selection=node_dict["n_shapelets_for_selection"],
            n_ts_for_selection_per_class=node_dict["n_ts_for_selection_per_class"],
            sliding_window=node_dict["sliding_window"],
            selection=node_dict["selection"],
            distance=node_dict["distance"],
            mi_n_neighbors=node_dict["mi_n_neighbors"],
            random_state=node_dict["random_state"],
            n_jobs=node_dict["n_jobs"]
        )

        self.st.shapelets = np.array(node_dict["shapelets"])

        self.feature_original = np.zeros(3, dtype=int)
        self.threshold_original = np.zeros(3)
        self.n_node_samples = np.zeros(3, dtype=int)

        self.y_lims = node_dict["y_lims"]

        self.feature_original[0] = node_dict["feature_idx"]
        self.threshold_original[0] = node_dict["threshold"]
        self.n_node_samples[0] = node_dict["samples"]
        self.is_categorical = node_dict["is_categorical"]

        args = copy.deepcopy(node_dict["args"])
        self.is_oblique = args.pop("is_oblique")
        self.is_pivotal = args.pop("is_pivotal")
        self.unique_val_enum = args.pop("unique_val_enum")
        self.coefficients = args.pop("coefficients")
        self.kwargs = args

        return self