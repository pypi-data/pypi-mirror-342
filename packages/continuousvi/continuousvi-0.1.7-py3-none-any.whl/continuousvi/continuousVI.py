"""ContinuousVI module for scRNA-seq data analysis.

This module provides classes and methods to train and utilize scVI models for
single-cell RNA-seq data. It supports the inclusion of continuous covariates
(e.g., pseudotime in trajectory analysis, aging or other continuous measurements) while correcting for batch
effects. The main classes are:

- ContinuousVI: Sets up the anndata object and trains multiple scVI models.
- TrainedContinuousVI: Manages one or more trained scVI models, provides methods
  for generating embeddings, sampling expression parameters, and performing
  regression analysis.
"""

from __future__ import annotations

import math
import os
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import TYPE_CHECKING, Literal, overload

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import patsy
import pyro
import pyro.distributions as dist
import scanpy as sc
import scipy.sparse as sp
import scvi
import statsmodels.api as sm
import torch
from pyro.infer import MCMC, NUTS
from sklearn.linear_model import LinearRegression
from tqdm import tqdm
from tqdm.auto import tqdm

from .continuous_harmony import run_continuous_harmony

if TYPE_CHECKING:
    from scvi.distributions import ZeroInflatedNegativeBinomial


class ContinuousVI:
    """ContinuousVI module for scRNA-seq data analysis.

    This class is responsible for configuring the input data (AnnData object)
    and training multiple scVI models to account for batch effects, label keys,
    and one optional continuous covariate. Use the `train` method to train
    multiple scVI models. The trained models can be accessed via the returned
    `TrainedContinuousVI` instance.
    """

    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
    ) -> None:
        """Initialize a ContinuousVI object.

        Parameters
        ----------
        adata : sc.AnnData
            The annotated data matrix with cells (observations) and genes (variables).
        batch_key : str
            The column name in `adata.obs` that contains batch information.
        label_key : str or None
            The column name in `adata.obs` that contains label or cell-type information.
            If None, no label covariate is used.
        continuous_key : str or None
            The column name in `adata.obs` that contains a single continuous covariate
            (e.g., pseudotime). If None, no continuous covariate is used.

        """
        self.adata: sc.AnnData = adata
        self.batch_key: str = batch_key
        self.label_key: str | None = label_key
        self.continuous_key: str | None = continuous_key

    def train(
        self,
        n_train: int = 5,
        n_latent: int = 30,
        max_epochs: int = 800,
        early_stopping: bool = True,
    ) -> TrainedContinuousVI:
        """Train multiple scVI models (n_train times) and return a TrainedContinuousVI object.

        This method sets up the scVI anndata configuration once per training run
        and trains `n_train` scVI models with the same hyperparameters but
        potentially different random initializations.

        Parameters
        ----------
        n_train : int, default=5
            The number of times to train scVI with the same setup.
        n_latent : int, default=30
            The dimensionality of the scVI latent space (z).
        max_epochs : int, default=800
            The maximum number of training epochs.
        early_stopping : bool, default=True
            Whether to apply early stopping based on validation loss improvements.

        Returns
        -------
        TrainedContinuousVI
            A TrainedContinuousVI object containing the trained scVI models,
            allowing further analysis and model usage.

        """
        _trained_models: list[scvi.model.SCVI] = []
        for _ in tqdm(
            range(n_train),
            desc="Training multiple scVI models",
            leave=False,
        ):
            scvi.model.SCVI.setup_anndata(
                self.adata,
                batch_key=self.batch_key,
                labels_key=self.label_key,
                continuous_covariate_keys=[self.continuous_key] if self.continuous_key else None,
            )
            model = scvi.model.SCVI(self.adata, n_latent=n_latent)
            model.train(max_epochs=max_epochs, early_stopping=early_stopping)
            _trained_models.append(model)
        return TrainedContinuousVI(
            adata=self.adata,
            batch_key=self.batch_key,
            label_key=self.label_key,
            continuous_key=self.continuous_key,
            trained_models=_trained_models,
        )


class TrainedContinuousVI:
    """TrainedContinuousVI manages one or more trained scVI models for scRNA-seq data.

    This class provides methods to:
    - Load or store multiple trained scVI models.
    - Calculate embeddings (UMAP, clusters) using the latent representation.
    - Perform regressions against the continuous covariate.
    - Sample parameters from the generative model (px).
    - Save the trained models to disk.
    """

    @overload
    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
        trained_models: list[scvi.model.SCVI],
    ) -> None: ...

    @overload
    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
        trained_model_path: Path | str,
    ) -> None: ...

    def __init__(
        self,
        adata: sc.AnnData,
        batch_key: str,
        label_key: str | None,
        continuous_key: str | None,
        trained_models: list[scvi.model.SCVI] | None = None,
        trained_model_path: Path | str | None = None,
    ) -> None:
        """Initialize a TrainedContinuousVI object with trained scVI models or a path to load them.

        Parameters
        ----------
        adata : sc.AnnData
            The annotated data matrix used for model training or inference.
        batch_key : str
            The column name in `adata.obs` for batch information.
        label_key : str or None
            The column name in `adata.obs` for label or cell-type information.
        continuous_key : str or None
            The column name in `adata.obs` for continuous covariate information.
        trained_models : list[scvi.model.SCVI], optional
            A list of scVI models that have already been trained.
        trained_model_path : Path or str, optional
            Path to a directory that contains one or more trained scVI models.
            If provided, the models at this path will be loaded instead of using
            `trained_models`.

        Raises
        ------
        ValueError
            If both `trained_models` and `trained_model_path` are None.

        """
        self.adata = adata
        self.batch_key: str = batch_key
        self.label_key: str | None = label_key
        self.continuous_key: str | None = continuous_key

        scvi.model.SCVI.setup_anndata(
            adata=adata,
            batch_key=batch_key,
            labels_key=label_key,
            continuous_covariate_keys=[continuous_key] if continuous_key is not None else None,
        )

        if trained_models is None and trained_model_path is None:
            raise ValueError(
                "`trained_models` or `trained_model_path` is required. Both are None.",
            )

        if trained_models is None and trained_model_path is not None:
            _trained_model_paths = [p for p in (trained_model_path if isinstance(trained_model_path, Path) else Path(trained_model_path)).rglob("*") if p.is_dir()]
            _trained_models: list[scvi.model.SCVI] = [scvi.model.SCVI.load(str(p), adata) for p in tqdm(_trained_model_paths, desc="Loading pre-trained models")]
        else:
            _trained_models = trained_models

        self.trained_models = _trained_models

        self._embeddings: TrainedContinuousVI.Embeddings | None = None

    @property
    def embeddings(self) -> TrainedContinuousVI.Embeddings:
        """Return the Embeddings object for visualizations and further downstream analyses.

        Returns
        -------
        TrainedContinuousVI.Embeddings
            An Embeddings object that provides methods such as `umap` for
            generating UMAP plots.

        Raises
        ------
        ValueError
            If embeddings have not been computed yet. Please call
            `calc_embeddings()` first.

        """
        if self._embeddings is None:
            raise ValueError(
                "No Embeddings object found. Please execute `calc_embeddings()` first.",
            )
        return self._embeddings

    def latent_coord(
        self,
        n_use_model: int = 0,
        use_clusteringbased_correction: bool = False,
    ) -> np.ndarray:
        """Return the latent coordinates from one of the trained scVI models.

        Parameters
        ----------
        n_use_model : int, default=0
            The index of the trained model in `self.trained_models` to use for
            obtaining the latent representation.

        Returns
        -------
        numpy.ndarray
            A 2D array of shape (n_cells, n_latent) containing the latent representation.

        """
        arr: np.ndarray = self.trained_models[n_use_model].get_latent_representation(
            adata=self.adata,
        )
        if use_clusteringbased_correction:
            if self.continuous_key is None:
                ho = run_continuous_harmony(
                    data_mat=arr.T,
                    meta_data=self.adata.obs,
                    vars_use=[self.batch_key],
                    remove_vars=[self.batch_key],
                )
            else:
                ho = run_continuous_harmony(
                    data_mat=arr.T,
                    meta_data=self.adata.obs,
                    vars_use=[self.batch_key, self.continuous_key],
                    remove_vars=[self.batch_key],
                )
            arr = ho.result().T
        return arr

    def calc_embeddings(
        self,
        resolution: float = 0.5,
        n_neighbors: int = 10,
        n_pcs: int = 30,
        n_use_model: int = 0,
        use_clusteringbased_correction: bool = False,
    ) -> TrainedContinuousVI:
        """Calculate embeddings and cluster labels using the latent space.

        This method:
        - Stores the latent coordinates in `adata.obsm["X_latent"]`.
        - Computes neighborhood graphs using `scanpy.pp.neighbors`.
        - Performs draw_graph, leiden clustering, paga, and UMAP embedding.
        - Creates an `Embeddings` object that can be used for plotting.

        Parameters
        ----------
        resolution : float, default=0.5
            Resolution parameter for the leiden clustering. Higher values lead to
            more granular clustering.
        n_neighbors : int, default=10
            Number of neighbors to use for building the k-NN graph.
        n_pcs : int, default=30
            Number of principal components to use for neighborhood computation (if applicable).
        n_use_model : int, default=0
            The index of the trained model to use when extracting latent coordinates.
        use_clusteringbased_correction : bool, default = False
            Use clustering based (harmony) correction?

        Returns
        -------
        TrainedContinuousVI
            The TrainedContinuousVI instance with updated embeddings in `adata.obsm`
            and a newly created `Embeddings` object (`self._embeddings`).

        """
        KEY_LATENT = "X_latent"
        KEY_CLUSTER = "clusters"
        self.adata.obsm[KEY_LATENT] = self.latent_coord(
            n_use_model,
            use_clusteringbased_correction,
        )
        sc.pp.neighbors(
            self.adata,
            n_neighbors=n_neighbors,
            n_pcs=n_pcs,
            use_rep=KEY_LATENT,
        )
        sc.tl.draw_graph(self.adata)
        sc.tl.leiden(
            self.adata,
            key_added=KEY_CLUSTER,
            resolution=resolution,
            directed=False,
        )
        sc.tl.paga(self.adata, groups=KEY_CLUSTER)
        sc.tl.umap(self.adata)
        self._embeddings = TrainedContinuousVI.Embeddings(self)
        return self

    def save(
        self,
        dir_path: Path | str,
        overwrite: bool = False,
    ) -> TrainedContinuousVI:
        """Save the trained models to the specified directory.

        Each model is saved in a subdirectory named `model_{i}` where `i`
        is the index of the model. For example, if there are 5 models in
        `self.trained_models`, subdirectories `model_0, model_1, ... model_4`
        will be created.

        Parameters
        ----------
        dir_path : Path or str
            The directory path where the models will be saved.
        overwrite : bool, default=False
            Whether to overwrite existing models at the target path if a
            model directory already exists.

        Returns
        -------
        TrainedContinuousVI
            The TrainedContinuousVI instance (self) for chained operations.

        """
        _base_path = dir_path if isinstance(dir_path, Path) else Path(dir_path)
        for n in tqdm(range(len(self.trained_models)), desc="Saving trained model."):
            _path = _base_path / Path(f"model_{n}")
            self.trained_models[n].save(_path, overwrite=overwrite)
        return self

    def sample_px(
        self,
        transform_batch: int = 0,
        n_draw: int = 25,
        batch_size: int = 512,
        mean: bool = True,
    ) -> torch.Tensor:
        """Return model-corrected `px` means for every cell.

        The function removes **both** batch effects and library-size variation,
        making the output directly comparable across projects/batches.

        Parameters
        ----------
        transform_batch : int, default = 0
            Index of the reference batch to which *all* cells are virtually
            transformed during the generative step.
        n_draw : int, default = 25
            Number of Monte-Carlo stochastic forward passes.  Larger values
            reduce sampling noise at the cost of runtime.
        batch_size : int, default = 512
            Mini-batch size for inference / generative forward passes.  Choose a
            value that fits comfortably in GPU/CPU memory.
        mean : bool, default = True
            If ``True`` (default) the function returns the average over all
            draws with shape ``(n_cells, n_genes)``.  If ``False`` the full
            tensor with shape ``(n_draw, n_cells, n_genes)`` is returned.

        Returns
        -------
        torch.Tensor
            * shape ``(n_cells, n_genes)`` when ``mean=True``
            * shape ``(n_draw, n_cells, n_genes)`` when ``mean=False``

        Notes
        -----
        1. **Inference** is executed with each cell’s *original* batch index so
        that the latent variables `z` and the cell-specific library size
        estimate are consistent with the raw data.
        2. **Generative** step uses:
            • ``batch_index = transform_batch`` (batch effects removed)
            • ``library = median(inference_library)`` (library-size normalised)
        3. If multiple models are held in ``self.trained_models`` their outputs
        are averaged first, then the `n_draw` draws are averaged when
        ``mean=True``.

        """
        adata = self.adata
        n_cells, n_genes = adata.n_obs, adata.n_vars
        cont_obsm_key = "_scvi_extra_continuous_covs"

        # ----------------------------- input as torch
        x_full = adata.X.toarray() if hasattr(adata.X, "toarray") else adata.X
        x_full_torch = torch.as_tensor(x_full, dtype=torch.float32)

        # original batch index (inference)
        if "_scvi_batch" in adata.obs:
            batch_index_full = torch.as_tensor(adata.obs["_scvi_batch"].to_numpy(), dtype=torch.int64).unsqueeze(1)
        else:
            cats = adata.obs[self.batch_key].astype("category").cat.codes.to_numpy()
            batch_index_full = torch.as_tensor(cats, dtype=torch.int64).unsqueeze(1)

        # continuous covariates (if any)
        cont_covs_arr = adata.obsm[cont_obsm_key] if isinstance(adata.obsm[cont_obsm_key], np.ndarray) else adata.obsm[cont_obsm_key].to_numpy()
        cont_covs_full = torch.as_tensor(cont_covs_arr, dtype=torch.float32)

        # ----------------------------- output buffer
        px_samples = torch.empty((n_draw, n_cells, n_genes), dtype=torch.float32)
        all_idx = np.arange(n_cells)

        for draw in range(n_draw):
            draw_accum = torch.zeros((n_cells, n_genes), dtype=torch.float32)

            for model in self.trained_models:
                if model.module is None:
                    raise ValueError("Found an un-initialised model in `trained_models`.")

                for start in range(0, n_cells, batch_size):
                    end = min(start + batch_size, n_cells)
                    idx = all_idx[start:end]

                    x_batch = x_full_torch[idx]
                    batch_idx_infer = batch_index_full[idx]
                    cont_covs_batch = cont_covs_full[idx]

                    # ------------------- inference (original batch)
                    with torch.no_grad():
                        inf = model.module.inference(
                            x=x_batch,
                            batch_index=batch_idx_infer,
                            cont_covs=cont_covs_batch,
                            cat_covs=None,
                        )

                    z_est = inf["z"]

                    # ------------------- generative (batch corrected, library fixed)
                    lib_scalar = torch.median(inf["library"]).item()
                    library_fixed = torch.full_like(inf["library"], lib_scalar)
                    batch_idx_gen = torch.full_like(batch_idx_infer, transform_batch)

                    with torch.no_grad():
                        gen = model.module.generative(
                            z=z_est,
                            library=library_fixed,
                            batch_index=batch_idx_gen,
                            cont_covs=cont_covs_batch,
                            cat_covs=None,
                        )

                    draw_accum[idx] += gen["px"].mean  # (cells, genes)

            draw_accum /= len(self.trained_models)
            px_samples[draw] = draw_accum

        return px_samples.mean(0) if mean else px_samples

    def plot_px_expression(
        self,
        target_genes: Sequence[str],
        *,
        mode: Literal["px", "raw"] = "px",
        continuous_key: str = "age",
        batch_key: str = "project",
        transform_batch: str | None = None,
        n_draws: int = 25,
        stabilize_log1p: bool = False,
        summary_stat: Literal["median", "mean"] = "median",
        ci: float = 0.80,
        ribbon_style: Literal["uniform", "gradient"] = "gradient",
        n_quantile_bands: int = 5,
        cmap_name: str = "viridis",
        # Central-line appearance -------------------------------------------------
        line_color: str = "black",
        line_width: float = 2.5,
        outline: bool = True,
        outline_width: float = 5,
        outline_color: str = "white",
        marker_size: int = 50,
        # Summarisation -----------------------------------------------------------
        summarise: bool = False,
        summarise_label: str | None = None,
        summarise_fn: Literal["sum", "mean"] = "sum",
    ) -> None:
        """Visualise gene expression along a continuous covariate.

        Parameters
        ----------
        mode : {"px", "raw"}
            * "px"  – use model-corrected ``sample_px`` means (default).
            * "raw" – use uncorrected counts stored in ``adata.X`` (no batch transform).
        transform_batch : str | None
            Only relevant for ``mode='px'`` – target batch label for expression normalisation.

        Other Parameters
        ----------------
        Please refer to in-code documentation for full argument list.

        """
        # ------------------------------------------------------------------- data
        adata = self.adata
        x_vals = adata.obs[continuous_key].to_numpy()

        # Gene indices -----------------------------------------------------------
        gene_idx = [np.where(adata.var_names == g)[0][0] for g in target_genes]

        # ------------------------------------------------------------------- mode
        if mode == "px":
            # Batch mapping (only needed for px)
            if transform_batch is None:
                tb_idx = 0
            else:
                cats = list(adata.obs[batch_key].cat.categories) if pd.api.types.is_categorical_dtype(adata.obs[batch_key]) else list(pd.Categorical(adata.obs[batch_key]).categories)
                if transform_batch not in cats:
                    raise ValueError(f"transform_batch '{transform_batch}' not found in '{batch_key}' column.")
                tb_idx = cats.index(transform_batch)

            px = self.sample_px(
                transform_batch=tb_idx,
                n_draw=n_draws,
                batch_size=512,
            )
            expr = px.cpu().numpy() if hasattr(px, "cpu") else px
            expr = expr[:, gene_idx]

        elif mode == "raw":
            # adata.X may be sparse; slice & densify only small matrix (cells × genes)
            X_sub = adata[:, gene_idx].X
            if sp.issparse(X_sub):
                X_sub = X_sub.toarray()
            expr = np.asarray(X_sub, dtype=float)
        else:
            raise ValueError("mode must be 'px' or 'raw'")

        # ---------------------------------------------------------------- log1p
        if stabilize_log1p:
            expr = np.log1p(expr)
            y_label = "log1p(px)" if mode == "px" else "log1p(raw)"
        else:
            y_label = "px mean" if mode == "px" else "raw counts"

        # ---------------------------------------------------------------- summarise
        if summarise:
            collapsed = expr.sum(axis=1) if summarise_fn == "sum" else expr.mean(axis=1)
            expr = collapsed[:, None]
            target_genes = [summarise_label or f"{summarise_fn.capitalize()} ({len(gene_idx)} genes)"]

        # ---------------------------------------------------------------- figure
        n_genes = len(target_genes)
        ncols = 3 if not summarise else 1
        nrows = math.ceil(n_genes / ncols)
        fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows), squeeze=False)
        axes = axes.ravel()

        # Colour map for gradient ribbons ---------------------------------------
        if ribbon_style == "gradient":
            cmap = mpl.cm.get_cmap(cmap_name, 2 * n_quantile_bands + 1)

        unique_x = np.sort(np.unique(x_vals))
        q_low_outer = (1 - ci) / 2
        q_high_outer = 1 - q_low_outer
        if ribbon_style == "gradient":
            band_probs = np.linspace(q_low_outer, 0.5, n_quantile_bands, endpoint=False)

        for ax, gi, gene in zip(axes, range(n_genes), target_genes, strict=False):
            y = expr[:, gi]
            central, low_outer, high_outer = [], [], []
            if ribbon_style == "gradient":
                lower_grid = np.empty((n_quantile_bands, unique_x.size))
                upper_grid = np.empty_like(lower_grid)

            # Aggregate per x ---------------------------------------------------
            for j, xv in enumerate(unique_x):
                subset = y[x_vals == xv]
                if subset.size == 0:
                    central.append(np.nan)
                    low_outer.append(np.nan)
                    high_outer.append(np.nan)
                    if ribbon_style == "gradient":
                        lower_grid[:, j] = np.nan
                        upper_grid[:, j] = np.nan
                    continue

                low_outer.append(np.quantile(subset, q_low_outer))
                high_outer.append(np.quantile(subset, q_high_outer))
                central.append(np.median(subset) if summary_stat == "median" else np.mean(subset))

                if ribbon_style == "gradient":
                    for b, p in enumerate(band_probs):
                        lower_grid[b, j] = np.quantile(subset, p)
                        upper_grid[b, j] = np.quantile(subset, 1 - p)

            # Ribbons -----------------------------------------------------------
            if ribbon_style == "uniform":
                ax.fill_between(unique_x, low_outer, high_outer, alpha=0.3, color="grey", zorder=1)
            else:
                for b in range(n_quantile_bands)[::-1]:
                    ax.fill_between(
                        unique_x,
                        lower_grid[b],
                        upper_grid[b],
                        color=cmap(b + n_quantile_bands + 1),
                        alpha=0.7,
                        zorder=1 + b,
                    )

            # Central line ------------------------------------------------------
            if outline:
                ax.plot(unique_x, central, lw=outline_width, color=outline_color, zorder=4)
            ax.plot(
                unique_x,
                central,
                marker="o",
                markersize=marker_size / 10,
                lw=line_width,
                color=line_color,
                zorder=5,
            )

            # Labels ------------------------------------------------------------
            ax.set_title(gene)
            ax.set_xlabel(continuous_key)
            ax.set_ylabel(y_label)

        for ax in axes[n_genes:]:
            ax.axis("off")

        fig.tight_layout()

    # def regression(
    #     self,
    #     transform_batch: int = 0,
    #     stabilize_log1p: bool = True,
    #     mode: Literal["ols", "poly2", "spline"] = "ols",
    #     n_samples: int = 25,
    #     batch_size: int = 512,
    #     spline_df: int = 5,
    #     spline_degree: int = 3,
    #     use_mcmc: bool = True,
    #     # use_clusteringbased_correction: bool = False,
    # ) -> pd.DataFrame:
    #     """Perform gene-wise regression of scVI-imputed expression values (px) against a continuous covariate.

    #     Parameters
    #     ----------
    #     transform_batch : int, optional
    #         Batch index to which all cells are 'transformed' when generating px.
    #     stabilize_log1p : bool, optional
    #         If True, applies log1p to the px values before regression.
    #     mode : {"ols", "poly2", "spline"}, optional
    #         Regression model to use.
    #     n_samples : int, optional
    #         - If `use_mcmc=False`, number of draws for frequentist regressions.
    #         - If `use_mcmc=True`, number of posterior samples (per chain) in MCMC.
    #     batch_size : int, optional
    #         Mini-batch size for sampling latent variables, useful for large datasets.
    #     spline_df : int, optional
    #         Degrees of freedom for spline basis if mode="spline".
    #     spline_degree : int, optional
    #         Polynomial degree for the spline if mode="spline".
    #     use_mcmc : bool, optional
    #         If True, performs hierarchical Bayesian regression with MCMC (Pyro).

    #     Returns
    #     -------
    #     pd.DataFrame
    #         DataFrame of regression results. The content depends on whether MCMC is used or not.

    #     """
    #     # -----------------------------------------------------------------------
    #     # (A) Basic checks / data prep
    #     # -----------------------------------------------------------------------
    #     if self.continuous_key is None:
    #         raise ValueError("continuous_key must not be None for regression.")
    #     if mode not in {"ols", "poly2", "spline"}:
    #         raise ValueError("Unsupported mode. Use 'ols', 'poly2', or 'spline'.")

    #     adata_local = self.adata.copy()
    #     continuous_values = adata_local.obs[self.continuous_key].astype(float).to_numpy()
    #     n_cells = adata_local.n_obs
    #     n_genes = adata_local.n_vars
    #     gene_names = adata_local.var_names.to_numpy()

    #     # -----------------------------------------------------------------------
    #     # (B) Sample px using sample_px_new (mean=False => keep all draws)
    #     # -----------------------------------------------------------------------
    #     px_samples_torch = self.sample_px(
    #         transform_batch=transform_batch,
    #         n_draw=n_samples,
    #         batch_size=batch_size,
    #         # use_clusteringbased_correction=False,
    #         mean=False,  # get shape=(n_samples, n_cells, n_genes)
    #     )
    #     px_samples = px_samples_torch.cpu().numpy()  # convert to numpy
    #     # shape: (n_samples, n_cells, n_genes)

    #     # Optional log transform
    #     if stabilize_log1p:
    #         px_samples = np.log1p(px_samples)

    #     # -----------------------------------------------------------------------
    #     # (C) Design matrix
    #     # -----------------------------------------------------------------------
    #     if mode == "ols":
    #         X_design = sm.add_constant(continuous_values)
    #         design_cols = ["Intercept", "Slope"]
    #     elif mode == "poly2":
    #         X_design = np.column_stack(
    #             [
    #                 continuous_values**2,
    #                 continuous_values,
    #                 np.ones_like(continuous_values),
    #             ],
    #         )
    #         design_cols = ["Coef_x2", "Coef_x1", "Intercept"]
    #     else:  # spline
    #         spline_frame = patsy.dmatrix(
    #             f"bs(x, df={spline_df}, degree={spline_degree}, include_intercept=True)",
    #             {"x": continuous_values},
    #             return_type="dataframe",
    #         )
    #         X_design = spline_frame.to_numpy()
    #         design_cols = list(spline_frame.columns)

    #     # Helper: compute summary stats
    #     def compute_stats(array_2d: np.ndarray) -> dict:
    #         """Computes mean, std, 2.5%, 97.5%, prob_positive along axis=0.
    #         array_2d shape = (n_samples, n_genes).
    #         """
    #         mean_ = array_2d.mean(axis=0)
    #         std_ = array_2d.std(axis=0)
    #         pct2_5 = np.percentile(array_2d, 2.5, axis=0)
    #         pct97_5 = np.percentile(array_2d, 97.5, axis=0)
    #         prob_pos = (array_2d > 0).mean(axis=0)
    #         return {
    #             "mean": mean_,
    #             "std": std_,
    #             "2.5pct": pct2_5,
    #             "97.5pct": pct97_5,
    #             "prob_positive": prob_pos,
    #         }

    #     if not use_mcmc:
    #         # n_samples draws => for each draw, fit OLS (or poly2/spline) on each gene
    #         n_params = X_design.shape[1]
    #         param_values = np.zeros((n_samples, n_genes, n_params), dtype=np.float32)
    #         r2_values = np.zeros((n_samples, n_genes), dtype=np.float32)

    #         def _fit_one_gene(task):
    #             s_idx, g_idx, y_ = task
    #             reg_res = sm.OLS(y_, X_design).fit()
    #             return s_idx, g_idx, reg_res.params, reg_res.rsquared

    #         tasks = []
    #         for s_idx in range(n_samples):
    #             current_px = px_samples[s_idx]  # shape=(n_cells, n_genes)
    #             for g_idx in range(n_genes):
    #                 y_vals = current_px[:, g_idx]
    #                 tasks.append((s_idx, g_idx, y_vals))

    #         with ThreadPoolExecutor(max_workers=1) as executor:
    #             futures = [executor.submit(_fit_one_gene, t) for t in tasks]
    #             for fut in tqdm(
    #                 as_completed(futures),
    #                 total=len(futures),
    #                 desc="Fitting regressions",
    #                 leave=True,
    #             ):
    #                 s_idx, g_idx, params, r2_val = fut.result()
    #                 param_values[s_idx, g_idx, :] = params
    #                 r2_values[s_idx, g_idx] = r2_val

    #         # 統計量まとめ
    #         parameters_summary = {}
    #         for param_idx, col_name in enumerate(design_cols):
    #             param_array = param_values[
    #                 :,
    #                 :,
    #                 param_idx,
    #             ]  # shape=(n_samples, n_genes)
    #             parameters_summary[col_name] = compute_stats(param_array)

    #         r2_summary = compute_stats(r2_values)

    #         # 出力整形
    #         output_dict = {"gene": gene_names}
    #         for col_name, stats_dict in parameters_summary.items():
    #             output_dict[f"{col_name}_mean"] = stats_dict["mean"]
    #             output_dict[f"{col_name}_std"] = stats_dict["std"]
    #             output_dict[f"{col_name}_2.5pct"] = stats_dict["2.5pct"]
    #             output_dict[f"{col_name}_97.5pct"] = stats_dict["97.5pct"]
    #             output_dict[f"{col_name}_prob_positive"] = stats_dict["prob_positive"]

    #         output_dict["r2_mean"] = r2_summary["mean"]
    #         output_dict["r2_std"] = r2_summary["std"]
    #         output_dict["r2_2.5pct"] = r2_summary["2.5pct"]
    #         output_dict["r2_97.5pct"] = r2_summary["97.5pct"]
    #         output_dict["r2_prob_positive"] = r2_summary["prob_positive"]

    #         regression_output = pd.DataFrame(output_dict)

    #         # 例: OLS/Poly2 の場合は係数でソート
    #         if mode == "ols" and "Slope_mean" in regression_output.columns:
    #             regression_output = regression_output.sort_values(
    #                 "Slope_mean",
    #                 ascending=False,
    #             )
    #         elif mode == "poly2" and "Coef_x1_mean" in regression_output.columns:
    #             regression_output = regression_output.sort_values(
    #                 "Coef_x1_mean",
    #                 ascending=False,
    #             )

    #         return regression_output.reset_index(drop=True)

    #     # -----------------------------------------------------------------------
    #     # (E) use_mcmc=True => Pyro による階層ベイズ回帰
    #     # -----------------------------------------------------------------------
    #     # ここでは 1 サンプル目 (px_samples[0]) などを使う例を示す
    #     # 本当に scVI の不確実性 (n_draw) まで反映させたい場合は、さらにモデルを拡張するなど検討が必要
    #     # -----------------------------------------------------------------------
    #     Y_data = px_samples[0]  # shape=(n_cells, n_genes)

    #     # 階層ベイズモデル (chunk 単位で遺伝子を分割)
    #     def hierarchical_model_chunk(x_torch: torch.Tensor, y_torch: torch.Tensor):
    #         """Hierarchical Bayesian linear model for a chunk of genes.

    #         param[g, d] ~ Normal(param_mean[d], param_sd[d])
    #         sigma[g]    ~ Exponential(1)
    #         y_{cell,g}  ~ Normal( (x_{cell} @ param[g]), sigma[g] )
    #         """
    #         n_cells_chunk, n_genes_chunk = y_torch.shape
    #         n_params_local = x_torch.shape[1]

    #         # Hyper-priors
    #         param_mean = pyro.sample(
    #             "param_mean",
    #             dist.Normal(
    #                 torch.zeros(n_params_local),
    #                 5.0 * torch.ones(n_params_local),
    #             ).to_event(1),
    #         )
    #         param_sd = pyro.sample(
    #             "param_sd",
    #             dist.Exponential(torch.ones(n_params_local)).to_event(1),
    #         )

    #         # gene-wise parameters
    #         param = pyro.sample(
    #             "param",
    #             dist.Normal(param_mean.unsqueeze(0), param_sd.unsqueeze(0)).expand([n_genes_chunk, n_params_local]).to_event(2),
    #         )
    #         sigma = pyro.sample(
    #             "sigma",
    #             dist.Exponential(1.0).expand([n_genes_chunk]).to_event(1),
    #         )

    #         param_t = param.transpose(0, 1)  # => shape=(n_params_local, n_genes_chunk)
    #         mu = x_torch @ param_t  # => (n_cells_chunk, n_genes_chunk)

    #         with pyro.plate("data", n_cells_chunk, dim=-2):
    #             pyro.sample("obs", dist.Normal(mu, sigma), obs=y_torch)

    #     # geneごとにチャンク分割
    #     n_threads = 1  # 並列数 (要調整)
    #     chunk_size = max(1, n_genes // n_threads) if n_threads > 0 else n_genes
    #     chunk_starts = range(0, n_genes, chunk_size)
    #     chunk_intervals = [(start, min(start + chunk_size, n_genes)) for start in chunk_starts]

    #     warmup_steps = 200  # MCMCウォームアップ (要調整)

    #     def run_mcmc_for_chunk(g_start: int, g_end: int) -> pd.DataFrame:
    #         g_slice = slice(g_start, g_end)
    #         Y_chunk = Y_data[:, g_slice]  # (n_cells, chunk_size)
    #         x_torch_chunk = torch.tensor(X_design, dtype=torch.float32)
    #         y_torch_chunk = torch.tensor(Y_chunk, dtype=torch.float32)

    #         nuts_kernel = NUTS(hierarchical_model_chunk)
    #         mcmc = MCMC(
    #             nuts_kernel,
    #             num_samples=n_samples,
    #             warmup_steps=warmup_steps,
    #             num_chains=1,  # for simplicity
    #         )
    #         mcmc.run(x_torch_chunk, y_torch_chunk)
    #         posterior = mcmc.get_samples()  # dict with ["param_mean", "param_sd", "param", "sigma"]

    #         # (n_samples, chunk_size, n_params)
    #         param_array = posterior["param"].cpu().numpy()
    #         sigma_array = posterior["sigma"].cpu().numpy()  # (n_samples, chunk_size)
    #         # R^2 用
    #         r2_array = np.zeros((n_samples, Y_chunk.shape[1]), dtype=np.float32)

    #         # R^2計算
    #         for s_idx in range(n_samples):
    #             param_s = param_array[s_idx]  # shape=(chunk_size, n_params)
    #             # 予測
    #             predicted_s = X_design @ param_s.T  # => (n_cells, chunk_size)
    #             for g_local in range(Y_chunk.shape[1]):
    #                 y_true = Y_chunk[:, g_local]
    #                 y_hat = predicted_s[:, g_local]
    #                 sse = np.sum((y_true - y_hat) ** 2)
    #                 sst = np.sum((y_true - y_true.mean()) ** 2)
    #                 r2_value = 1.0 - (sse / (sst + 1e-12))
    #                 r2_array[s_idx, g_local] = r2_value

    #         chunk_gene_names = gene_names[g_slice]
    #         records = []
    #         for g_local, gene_name in enumerate(chunk_gene_names):
    #             row = {"gene": gene_name}
    #             # param_array[:, g_local, :] => (n_samples, n_params)
    #             for d_idx, col_name in enumerate(design_cols):
    #                 samples_d = param_array[:, g_local, d_idx]
    #                 row[f"{col_name}_mean"] = samples_d.mean()
    #                 row[f"{col_name}_std"] = samples_d.std()
    #                 row[f"{col_name}_2.5pct"] = np.percentile(samples_d, 2.5)
    #                 row[f"{col_name}_97.5pct"] = np.percentile(samples_d, 97.5)
    #                 row[f"{col_name}_prob_positive"] = (samples_d > 0).mean()

    #             sigma_samples = sigma_array[:, g_local]
    #             row["sigma_mean"] = sigma_samples.mean()
    #             row["sigma_std"] = sigma_samples.std()
    #             row["sigma_2.5pct"] = np.percentile(sigma_samples, 2.5)
    #             row["sigma_97.5pct"] = np.percentile(sigma_samples, 97.5)
    #             row["sigma_prob_positive"] = (sigma_samples > 0).mean()

    #             # R^2
    #             r2_gene = r2_array[:, g_local]
    #             row["r2_mean"] = r2_gene.mean()
    #             row["r2_std"] = r2_gene.std()
    #             row["r2_2.5pct"] = np.percentile(r2_gene, 2.5)
    #             row["r2_97.5pct"] = np.percentile(r2_gene, 97.5)
    #             row["r2_prob_positive"] = (r2_gene > 0).mean()

    #             records.append(row)
    #         return pd.DataFrame(records)

    #     # 並列でチャンク処理
    #     results_list = []
    #     with ThreadPoolExecutor(max_workers=n_threads) as executor:
    #         futures = []
    #         for start_i, end_i in chunk_intervals:
    #             fut = executor.submit(run_mcmc_for_chunk, start_i, end_i)
    #             futures.append(fut)

    #         for fut in tqdm(
    #             as_completed(futures),
    #             total=len(futures),
    #             desc="MCMC chunks",
    #             leave=True,
    #         ):
    #             df_part = fut.result()
    #             results_list.append(df_part)

    #     df_out = pd.concat(results_list, axis=0).reset_index(drop=True)

    #     # ソート(ols相当でSlopeがあれば / poly2でCoef_x1があれば)
    #     if mode == "ols":
    #         if len(design_cols) > 1 and f"{design_cols[1]}_mean" in df_out.columns:
    #             df_out = df_out.sort_values(f"{design_cols[1]}_mean", ascending=False)
    #     elif mode == "poly2" and "Coef_x1_mean" in df_out.columns:
    #         df_out = df_out.sort_values("Coef_x1_mean", ascending=False)

    #     return df_out.reset_index(drop=True)

    def regression(
        self,
        transform_batch: int = 0,
        stabilize_log1p: bool = True,
        mode: Literal["ols", "poly2", "spline"] = "ols",
        n_samples: int = 25,
        batch_size: int = 512,
        spline_df: int = 5,
        spline_degree: int = 3,
        use_mcmc: bool = True,
        use_raw: bool = False,
        mcmc_warmup: int = 200,
        mcmc_max_threads: int | None = None,
    ) -> pd.DataFrame:
        """Gene-wise regression on a continuous covariate.

        Parameters
        ----------
        use_raw
            True  – regress raw counts in ``adata.X`` (ignores transform_batch, n_samples, use_mcmc).
            False – regress batch-normalised px samples from ``sample_px``.
        use_mcmc
            When False a frequentist (OLS / GLM) fit is used.  When True a hierarchical
            Bayesian linear model is sampled with NUTS + MCMC.  For use_raw=True the
            function forces ``use_mcmc=False``.
        mcmc_warmup
            Warm-up (burn-in) steps for every chain.
        mcmc_max_threads
            Upper bound on parallel MCMC chains / gene chunks.  ``None`` = all CPU cores.

        All other arguments are identical to the original signature.

        """
        # -------------------- basic checks
        if self.continuous_key is None:
            raise ValueError("continuous_key must be set in the model.")
        if mode not in {"ols", "poly2", "spline"}:
            raise ValueError("mode must be 'ols', 'poly2', or 'spline'.")

        adata = self.adata
        n_cells, n_genes = adata.n_obs, adata.n_vars
        gene_names = adata.var_names.to_numpy()
        x_c = adata.obs[self.continuous_key].astype(float).to_numpy()

        # -------------------- obtain expression tensor: shape (draws, cells, genes)
        if use_raw:
            mat = adata.X.toarray() if sp.issparse(adata.X) else adata.X
            expr = mat.astype(float)[None, ...]  # add draws axis
            n_draws = 1
            use_mcmc = False  # force frequentist
        else:
            px_stack = self.sample_px(
                transform_batch=transform_batch,
                n_draw=n_samples,
                batch_size=batch_size,
                mean=False,
            )
            expr = px_stack.cpu().numpy()
            n_draws = n_samples

        if stabilize_log1p:
            expr = np.log1p(expr)

        # -------------------- design matrix
        if mode == "ols":
            X_design = sm.add_constant(x_c)
            design_cols = ["Intercept", "Slope"]
        elif mode == "poly2":
            X_design = np.vstack([x_c**2, x_c, np.ones_like(x_c)]).T
            design_cols = ["Coef_x2", "Coef_x1", "Intercept"]
        else:  # spline
            dm = patsy.dmatrix(
                f"bs(x, df={spline_df}, degree={spline_degree}, include_intercept=True)",
                {"x": x_c},
                return_type="dataframe",
            )
            X_design = dm.to_numpy()
            design_cols = dm.columns.tolist()

        def _summarise(mat2d: np.ndarray) -> dict[str, np.ndarray]:
            return {
                "mean": mat2d.mean(0),
                "std": mat2d.std(0),
                "2.5pct": np.percentile(mat2d, 2.5, 0),
                "97.5pct": np.percentile(mat2d, 97.5, 0),
                "prob_positive": (mat2d > 0).mean(0),
            }

        # =============================================================================================
        #  Frequentist branch (OLS / poly / spline, optionally multi-draw)
        # =============================================================================================
        if not use_mcmc:
            n_p = X_design.shape[1]
            coeff = np.zeros((n_draws, n_genes, n_p), dtype=np.float32)
            r2 = np.zeros((n_draws, n_genes), dtype=np.float32)

            def _fit(args):
                d, g, y_vec = args
                res = sm.OLS(y_vec, X_design).fit()
                return d, g, res.params, res.rsquared

            jobs = [(d, g, expr[d, :, g]) for d in range(n_draws) for g in range(n_genes)]
            with ThreadPoolExecutor(max_workers=1) as ex:
                futures = [ex.submit(_fit, j) for j in jobs]
                for fut in tqdm(as_completed(futures), total=len(jobs), desc="OLS fits"):
                    d_idx, g_idx, p_vec, rval = fut.result()
                    coeff[d_idx, g_idx] = p_vec
                    r2[d_idx, g_idx] = rval

            summary = {"gene": gene_names}
            for j, col in enumerate(design_cols):
                s = _summarise(coeff[:, :, j])
                summary.update({f"{col}_{k}": v for k, v in s.items()})

            s_r2 = _summarise(r2)
            summary.update({f"r2_{k}": v for k, v in s_r2.items()})
            df = pd.DataFrame(summary)

            sort_key = "Slope_mean" if mode == "ols" else ("Coef_x1_mean" if mode == "poly2" else None)
            if sort_key in df.columns:
                df = df.sort_values(sort_key, ascending=False, ignore_index=True)

            return df

        # =============================================================================================
        #  MCMC branch – hierarchical Bayesian linear regression
        # =============================================================================================
        pyro.enable_validation(False)
        torch.set_default_tensor_type(torch.FloatTensor)

        n_params = X_design.shape[1]
        x_torch = torch.tensor(X_design, dtype=torch.float32)

        # auto chunk size: balance memory & speed
        max_threads = mcmc_max_threads or max(1, (os.cpu_count() or 2) - 1)
        chunk_size = int(np.ceil(n_genes / max_threads))
        chunks = [(i, min(i + chunk_size, n_genes)) for i in range(0, n_genes, chunk_size)]

        def _model(x_mtx, y_mtx):
            n_cells_loc, n_genes_loc = y_mtx.shape
            with pyro.plate("params", n_params):
                mu = pyro.sample("mu", dist.Normal(0.0, 5.0))
                tau = pyro.sample("tau", dist.HalfCauchy(2.5))
            with pyro.plate("gene", n_genes_loc):
                beta = pyro.sample("beta", dist.Normal(mu, tau).expand([n_params]).to_event(1))
                sigma = pyro.sample("sigma", dist.HalfCauchy(2.5))
            mu_y = x_mtx @ beta.T  # (cells, genes)
            with pyro.plate("data", n_cells_loc):
                pyro.sample("obs", dist.Normal(mu_y, sigma), obs=y_mtx)

        def _run_mcmc(start, end):
            y = torch.tensor(expr[0, :, start:end], dtype=torch.float32)  # first draw only for speed
            nuts = NUTS(_model, target_accept_prob=0.8)
            mcmc = MCMC(
                nuts,
                num_samples=n_samples,
                warmup_steps=mcmc_warmup,
                num_chains=1,
                progress_bar=False,
            )
            mcmc.run(x_torch, y)
            post = mcmc.get_samples()  # dict: beta (draw, gene, param)
            beta_arr = post["beta"].cpu().numpy()  # (draws, genes, params)
            sigma_arr = post["sigma"].cpu().numpy()  # (draws, genes)

            # R² per draw & gene
            y_np = y.cpu().numpy()
            r2_arr = np.zeros((n_samples, end - start), dtype=np.float32)
            for d in range(n_samples):
                pred = X_design @ beta_arr[d].T
                ss_res = ((y_np - pred) ** 2).sum(0)
                ss_tot = ((y_np - y_np.mean(0)) ** 2).sum(0) + 1e-12
                r2_arr[d] = 1.0 - ss_res / ss_tot

            res = {"gene": gene_names[start:end]}
            for j, col in enumerate(design_cols):
                stat = _summarise(beta_arr[:, :, j])
                res.update({f"{col}_{k}": v for k, v in stat.items()})
            stat_sigma = _summarise(sigma_arr)
            res.update({f"sigma_{k}": v for k, v in stat_sigma.items()})
            stat_r2 = _summarise(r2_arr)
            res.update({f"r2_{k}": v for k, v in stat_r2.items()})
            return pd.DataFrame(res)

        with ThreadPoolExecutor(max_workers=len(chunks)) as ex:
            futures = [ex.submit(_run_mcmc, s, e) for s, e in chunks]
            dfs = [f.result() for f in tqdm(as_completed(futures), total=len(futures), desc="MCMC")]
        df_final = pd.concat(dfs, axis=0, ignore_index=True)

        if mode == "ols" and "Slope_mean" in df_final.columns:
            df_final = df_final.sort_values("Slope_mean", ascending=False, ignore_index=True)
        elif mode == "poly2" and "Coef_x1_mean" in df_final.columns:
            df_final = df_final.sort_values("Coef_x1_mean", ascending=False, ignore_index=True)

        return df_final

    class Embeddings:
        """Embeddings class for handling dimensional reductions and plotting.

        An instance of this class is created after calling `calc_embeddings()`
        on the parent `TrainedContinuousVI` object. Provides convenience methods
        for plotting UMAP or other embeddings with gene or metadata coloring.
        """

        def __init__(self, trained_vi: TrainedContinuousVI) -> None:
            """Construct an Embeddings object.

            Parameters
            ----------
            trained_vi : TrainedContinuousVI
                The parent TrainedContinuousVI instance containing the AnnData
                and trained models.

            """
            self.trained_vi = trained_vi

        def umap(
            self,
            color_by: list[str] | None = None,
            n_draw: int = 25,
            transform_batch: int | str | None = None,
            n_use_model: int = 0,
        ) -> TrainedContinuousVI.Embeddings:
            """Plot a UMAP embedding colored by genes or metadata.

            If `color_by` contains gene names that exist in `adata.var_names`,
            expression levels are sampled from the scVI models. If `color_by`
            contains column names that exist in `adata.obs`, those columns are used
            for coloring. The resulting AnnData (with X_umap, X_latent, etc.)
            is then plotted via `scanpy.pl.umap`.

            Parameters
            ----------
            color_by : list of str, optional
                A list of gene names (in `adata.var_names`) or column names (in `adata.obs`)
                by which to color the UMAP plot.
            n_draw : int, default=25
                Number of forward passes (draws) to estimate gene expression with scVI
                for coloring genes. Ignored for categorical obs coloring.
            transform_batch : int, str, or None, default=None
                The batch to condition on when estimating normalized gene expression.
                If None, no specific batch transformation is applied.
            n_use_model : int, default=0
                The index of the trained model to use when obtaining latent coordinates
                (if needed).

            Returns
            -------
            TrainedContinuousVI.Embeddings
                The Embeddings instance (self) for potential chaining.

            """
            unique_color_by: list[str] | None = list(dict.fromkeys(color_by)) if color_by is not None else None
            _target_vars: list[str] = []
            _target_obs: list[str] = []

            if unique_color_by is not None:
                for c in unique_color_by:
                    if c in self.trained_vi.adata.var_names:
                        _target_vars.append(c)
                    elif c in self.trained_vi.adata.obs.columns:
                        _target_obs.append(c)

                expression: np.ndarray | None = None
                if len(_target_vars) > 0:
                    expression = np.mean(
                        [
                            model.get_normalized_expression(
                                self.trained_vi.adata,
                                gene_list=_target_vars,
                                n_samples=n_draw,
                                transform_batch=transform_batch,
                            )
                            for model in tqdm(
                                self.trained_vi.trained_models,
                                desc="Sampling expression",
                                leave=True,
                            )
                        ],
                        axis=0,
                    )

                obs_df: pd.DataFrame = self.trained_vi.adata.obs[_target_obs] if len(_target_obs) > 0 else pd.DataFrame(index=self.trained_vi.adata.obs.index)
                vars_df: pd.DataFrame | None = None
                if len(_target_vars) > 0:
                    vars_df = self.trained_vi.adata.var[self.trained_vi.adata.var.index.isin(_target_vars)]

                _adata = sc.AnnData(
                    X=expression,
                    obs=obs_df,
                    var=vars_df,
                    obsm={
                        "X_latent": self.trained_vi.latent_coord(n_use_model),
                        "X_umap": self.trained_vi.adata.obsm["X_umap"],
                    },
                )
            if color_by is not None:
                sc.pl.umap(_adata, color=color_by, show=False)
            else:
                sc.pl.umap(_adata, show=False)

            return self
