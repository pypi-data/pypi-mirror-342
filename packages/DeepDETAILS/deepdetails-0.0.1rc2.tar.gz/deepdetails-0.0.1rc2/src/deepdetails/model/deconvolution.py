import torch
from typing import Tuple
from torch import nn
from . import ResidualConv, ResidualConvWithXProjection


class BaseRegressor(nn.Module):
    def __init__(self, filters=512, n_non_dil_layers=0, non_dil_kernel_size=3,
                 n_dil_layers=8, dil_kernel_size=3, profile_kernel_size=75,
                 counts_head_mlp_layers=3, num_tasks=1) -> None:
        super().__init__()
        self.body = nn.Sequential()

        for _ in range(n_non_dil_layers):
            self.body.append(
                ResidualConv(filters=filters, kernel_size=non_dil_kernel_size,
                             dilation_rate=1)
            )
        for i in range(n_dil_layers):
            self.body.append(
                ResidualConv(filters=filters, kernel_size=dil_kernel_size,
                             dilation_rate=2 ** (i + 1))
            )

        self.shape_head = nn.LazyConv1d(
            num_tasks, kernel_size=profile_kernel_size, padding="valid")
        self.counts_head = nn.Sequential()
        for _ in range(counts_head_mlp_layers):
            self.counts_head.append(nn.LazyLinear(filters))
            self.counts_head.append(nn.ReLU())
        self.counts_head.append(nn.LazyLinear(num_tasks))

    def forward(self, x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """

        Parameters
        ----------
        x : torch.Tensor
            Shape: batch, channels, seq_len

        Returns
        -------
        profile : torch.Tensor
            Shape: batch, num_tasks, seq_len_1
        counts : torch.Tensor
            Shape: batch, num_tasks
        """
        body = self.body(x)  # (batch, filters, remaining_length)
        shape = self.shape_head(body)  # (batch, strands, target_length)
        # shape = shape.squeeze()
        body_gap = body.mean(axis=2)  # (batch, filters)
        counts = self.counts_head(body_gap)
        return nn.functional.softmax(shape, dim=2), nn.functional.softplus(counts)


class SeqOnlyRegressor(nn.Module):
    def __init__(
            self, expected_clusters: int,
            filters=512, n_non_dil_layers=0, non_dil_kernel_size=3,
            n_dil_layers=8, dil_kernel_size=3, conv1_kernel_size=21, profile_kernel_size=75,
            counts_head_mlp_layers=3, num_tasks=1, n_times_more_embeddings=2,
            scale_function_placement: str = "late-ch") -> None:

        super().__init__()
        self.expected_clusters = expected_clusters

        # first convolution without dilation
        self.motif_detector = nn.Conv1d(
            4, filters, kernel_size=conv1_kernel_size, padding="valid")

        self.cluster_regressor = nn.ModuleList()

        for _ in range(self.expected_clusters):
            self.cluster_regressor.append(
                BaseRegressor(
                    filters=filters,
                    n_non_dil_layers=n_non_dil_layers,
                    non_dil_kernel_size=non_dil_kernel_size,
                    n_dil_layers=n_dil_layers,
                    dil_kernel_size=dil_kernel_size,
                    profile_kernel_size=profile_kernel_size,
                    counts_head_mlp_layers=counts_head_mlp_layers,
                    num_tasks=num_tasks)
            )

        self.scale_function_placement = scale_function_placement

    def forward(self, x: Tuple[torch.Tensor, torch.Tensor], per_cluster_load: torch.Tensor) -> tuple[
        list[torch.Tensor], list[torch.Tensor], torch.Tensor, list[torch.Tensor]]:
        """Forward propagation

        Parameters
        ----------
        x : Tuple[torch.Tensor, torch.Tensor]
            seq: Shape: batch, ATCG, window_size
            atac: Shape: batch, n_clusters, window_size
        per_cluster_load : torch.Tensor
            Prior about per cluster loads

        Returns
        -------
        tuple[list[torch.Tensor], list[torch.Tensor], torch.Tensor, list[torch.Tensor]]
            1. First element is per cluster profile (Shape: batch, strands, window_size).
            2. Second element is per cluster counts (Shape: batch, strands).
            3. Per cluster weights (Shape: batch, n_clusters)
            4. Per cluster motif gates (Shape: batch, filters)
            Elements in per cluster profiles can be directly used for the imputation of
            pseudo-bulk initiation patterns.
        """
        seq, atac = x
        motifs = self.motif_detector(seq)  # shape: batch, filters_1, seq_len

        cluster_weights = per_cluster_load
        per_cluster_profiles = []
        per_cluster_counts = []
        per_cluster_activations = []

        for cluster_id in range(self.expected_clusters):
            cw = cluster_weights[:, cluster_id]

            if self.scale_function_placement == "early":
                cluster_profile, cluster_counts = self.cluster_regressor[cluster_id](
                    motifs * cw[:, None, None])
            else:
                cluster_profile, cluster_counts = self.cluster_regressor[cluster_id](motifs)
            if self.scale_function_placement == "late":
                per_cluster_profiles.append(cluster_profile * cw[:, None, None])
                per_cluster_counts.append(cluster_counts * cw[:, None])
            elif self.scale_function_placement == "late-ch":
                per_cluster_profiles.append(cluster_profile)
                per_cluster_counts.append(cluster_counts * cw[:, None])
            else:
                per_cluster_profiles.append(cluster_profile)
                per_cluster_counts.append(cluster_counts)

        return per_cluster_profiles, per_cluster_counts, cluster_weights, per_cluster_activations


class PerClusterHead(nn.Module):
    def __init__(self, shape_filters=512, profile_kernel_size=75, counts_head_mlp_layers=3, num_tasks=1) -> None:
        super().__init__()

        self.shape_head = nn.Sequential()
        for _ in range(counts_head_mlp_layers):
            self.shape_head.append(nn.LazyConv1d(shape_filters, kernel_size=1))
            self.shape_head.append(nn.ELU())
        self.shape_head.append(nn.LazyConv1d(num_tasks, kernel_size=profile_kernel_size, padding="valid"))
        self.counts_head = nn.Sequential()
        for _ in range(counts_head_mlp_layers):
            self.counts_head.append(nn.LazyLinear(shape_filters, bias=False))
            self.counts_head.append(nn.ELU())
        self.counts_head.append(nn.LazyLinear(num_tasks))
        self.shape_act = nn.Softmax(dim=2)
        self.counts_act = nn.Softplus()

    def forward(self, x: tuple[torch.Tensor, torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor]:
        """

        Parameters
        ----------
        x : (torch.Tensor, torch.Tensor)
            Seq: shape: batch, channels_1, seq_len
            ATAC: shape: batch, channels_2, seq_len

        Returns
        -------
        profile : torch.Tensor
            Shape: batch, num_tasks, seq_len_1
        counts : torch.Tensor
            Shape: batch, num_tasks
        """
        seq_gap = x[0].mean(axis=2)

        shape = self.shape_head(torch.hstack([x[0], x[1]]))  # (batch, strands, target_length)
        counts = self.counts_head(torch.hstack([seq_gap, x[1].mean(axis=2)]))
        return self.shape_act(shape), self.counts_act(counts)


class Regressor(nn.Module):
    def __init__(
            self, expected_clusters: int,
            profile_shrinkage=1, filters=512, n_non_dil_layers=0, non_dil_kernel_size=3,
            n_dil_layers=8, dil_kernel_size=3, conv1_kernel_size=21, profile_kernel_size=75,
            counts_head_mlp_layers=3, num_tasks=1, gru_layers=1, gru_dropout=0.1, n_times_more_embeddings=2,
            scale_function_placement: str = "late-ch") -> None:

        super().__init__()
        self.expected_clusters = expected_clusters
        n_profile_filters = int(filters / profile_shrinkage)

        # first convolution without dilation
        self.motif_detector = nn.Sequential(nn.Conv1d(
            4, filters, kernel_size=conv1_kernel_size, padding="valid"))
        self.filter_gates = nn.ModuleList(
            [nn.LazyLinear(filters * n_times_more_embeddings, bias=False) for _ in range(expected_clusters)])
        self.profile_refiner = nn.GRU(input_size=1, hidden_size=n_profile_filters,
                                      num_layers=gru_layers, dropout=gru_dropout,
                                      batch_first=True, bidirectional=True)

        for _ in range(n_non_dil_layers):
            self.motif_detector.append(
                ResidualConv(filters=filters, kernel_size=non_dil_kernel_size,
                             dilation_rate=1)
            )

        for i in range(n_dil_layers):
            if i < n_dil_layers - 1:
                self.motif_detector.append(
                    ResidualConv(filters=filters, kernel_size=dil_kernel_size,
                                 dilation_rate=2 ** (i + 1))
                )
            else:
                self.motif_detector.append(
                    ResidualConvWithXProjection(filters=filters * n_times_more_embeddings, kernel_size=dil_kernel_size,
                                                dilation_rate=2 ** (i + 1))
                )

        self.per_cluster_preds = nn.ModuleList()
        for _ in range(self.expected_clusters):
            self.per_cluster_preds.append(
                PerClusterHead(
                    shape_filters=filters, profile_kernel_size=profile_kernel_size,
                    counts_head_mlp_layers=counts_head_mlp_layers, num_tasks=num_tasks
                ))

        self.scale_function_placement = scale_function_placement

    def forward(self, x: Tuple[torch.Tensor, torch.Tensor], per_cluster_load: torch.Tensor) -> tuple[
        list[torch.Tensor], list[torch.Tensor], torch.Tensor, list[torch.Tensor]]:
        """Forward propagation

        Parameters
        ----------
        x : Tuple[torch.Tensor, torch.Tensor]
            seq: Shape: batch, ATCG, window_size
            atac: Shape: batch, n_clusters, window_size
        per_cluster_load : torch.Tensor
            Prior about per cluster loads

        Returns
        -------
        tuple[list[torch.Tensor], list[torch.Tensor], torch.Tensor, list[torch.Tensor]]
            1. First element is per cluster profile (Shape: batch, strands, window_size).
            2. Second element is per cluster counts (Shape: batch, strands).
            3. Per cluster weights (Shape: batch, n_clusters)
            4. Per cluster motif gates (Shape: batch, filters)
            Elements in per cluster profiles can be directly used for the imputation of
            pseudo-bulk initiation patterns.
        """
        seq, atac = x
        motifs = self.motif_detector(seq)  # shape: batch, filters_1, seq_len
        motifs_gap = motifs.mean(axis=2)
        atac_truncation = (atac.shape[-1] - motifs.shape[-1]) // 2

        cluster_weights = per_cluster_load
        per_cluster_profiles = []
        per_cluster_counts = []
        per_cluster_activations = []

        for cluster_id in range(self.expected_clusters):
            cw = cluster_weights[:, cluster_id]
            profiles, _ = self.profile_refiner(atac[:, cluster_id, :].unsqueeze(2))  # shape: batch, filters_2, seq_len
            profiles = torch.swapaxes(profiles, 1, 2)[:, :, atac_truncation:-atac_truncation]

            gates = torch.sigmoid(self.filter_gates[cluster_id](motifs_gap))
            filtered_activations = motifs * gates[:, :, None]

            if self.scale_function_placement == "early":
                cluster_profile, cluster_counts = self.per_cluster_preds[cluster_id](
                    (filtered_activations * cw[:, None, None], profiles))
            else:
                cluster_profile, cluster_counts = self.per_cluster_preds[cluster_id]((filtered_activations, profiles))
            if self.scale_function_placement == "late":
                per_cluster_profiles.append(cluster_profile * cw[:, None, None])
                per_cluster_counts.append(cluster_counts * cw[:, None])
            elif self.scale_function_placement == "late-ch":
                per_cluster_profiles.append(cluster_profile)
                per_cluster_counts.append(cluster_counts * cw[:, None])
            else:
                per_cluster_profiles.append(cluster_profile)
                per_cluster_counts.append(cluster_counts)
            per_cluster_activations.append(gates)

        return per_cluster_profiles, per_cluster_counts, cluster_weights, per_cluster_activations
