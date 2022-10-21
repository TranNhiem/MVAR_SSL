# Copyright 2021 solo-learn development team.

# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import argparse

import pytorch_lightning as pl
from MV_MA_SSL.args.dataset import (
    augmentations_args,
    custom_dataset_args,
    dataset_args,
    linear_augmentations_args,
)
from MV_MA_SSL.args.utils import additional_setup_linear, additional_setup_pretrain  # look !! additional_setup_pretrain
from MV_MA_SSL.methods import METHODS
from MV_MA_SSL.utils.auto_resumer import AutoResumer
from MV_MA_SSL.utils.checkpointer import Checkpointer

try:
    from MV_MA_SSL.utils.auto_umap import AutoUMAP
except ImportError:
    _umap_available = False
else:
    _umap_available = True


def parse_args_pretrain() -> argparse.Namespace:
    """Parses dataset, augmentation, pytorch lightning, model specific and additional args.

    First adds shared args such as dataset, augmentation and pytorch lightning args, then pulls the
    model name from the command and proceeds to add model specific args from the desired class. If
    wandb is enabled, it adds checkpointer args. Finally, adds additional non-user given parameters.

    Returns:
        argparse.Namespace: a namespace containing all args needed for pretraining.
    """

    parser = argparse.ArgumentParser()

    # add shared arguments
    dataset_args(parser)
    augmentations_args(parser)
    custom_dataset_args(parser)

    # add pytorch lightning trainer args
    parser = pl.Trainer.add_argparse_args(parser)

    # add method-specific arguments
    parser.add_argument("--method", type=str)

    # THIS LINE IS KEY TO PULL THE MODEL NAME
    temp_args, _ = parser.parse_known_args()

    # add model specific args
    parser = METHODS[temp_args.method].add_model_specific_args(parser)

    # add auto checkpoint/umap args
    parser.add_argument("--save_checkpoint", action="store_true")
    parser.add_argument("--auto_umap", action="store_true")
    parser.add_argument("--auto_resume", action="store_true")

    parser.add_argument("--num_augment_trategy",  type=str, default="SimCLR_RA_AA_FA", help="Augmentation Strategies")
    parser.add_argument("--num_augment_strategies",  type=int, default=4, help="The total number of Augmentation Strategies")
    parser.add_argument("--rda_num_ops",  type=int, default=2)
    parser.add_argument("--rda_magnitude",  type=int, default=10)
    parser.add_argument("--ada_policy",  type=str, default="imagenet")
    parser.add_argument("--fda_policy",  type=str, default="imagenet")
    parser.add_argument("--encoder_width", type=int, default=1, help="scaling the width of ResNet encoder")
    parser.add_argument("--experiment_type",  type=str, default="ablation")
    parser.add_argument("--job_name",  type=str, default="multiaugment_ablation")
    parser.add_argument("--subset_classes",  type=int, default=1000, help="Subset ImageNet Class or Others Dataset")
    parser.add_argument("--num_large_crops",  type=int, default=4)
    parser.add_argument("--num_small_crops",  type=int, default=0)
    parser.add_argument("--weight_decay_scheduler",  type=str, default="cosine_scheduler")
    parser.add_argument("--wd_init",  type=float, default=0.004)
    parser.add_argument("--wd_final",  type=float, default=0.4)
    parser.add_argument("--num_classes",  type=int, default=1000)
    parser.add_argument("--backbone_args",  type=str, default="resnet50")
    parser.add_argument("--extra_optimizer_args",  type=str, default="LARS")

    temp_args, _ = parser.parse_known_args()

    # optionally add checkpointer and AutoUMAP args
    if temp_args.save_checkpoint:
        parser = Checkpointer.add_checkpointer_args(parser)

    if _umap_available and temp_args.auto_umap:
        parser = AutoUMAP.add_auto_umap_args(parser)

    if temp_args.auto_resume:
        parser = AutoResumer.add_autoresumer_args(parser)

    # parse args
    args = parser.parse_args()



    # prepare arguments with additional setup
    additional_setup_pretrain(args)

    return args


def parse_args_linear() -> argparse.Namespace:
    """Parses feature extractor, dataset, pytorch lightning, linear eval specific and additional args.

    First adds an arg for the pretrained feature extractor, then adds dataset, pytorch lightning
    and linear eval specific args. If wandb is enabled, it adds checkpointer args. Finally, adds
    additional non-user given parameters.

    Returns:
        argparse.Namespace: a namespace containing all args needed for pretraining.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--pretrained_feature_extractor", type=str)

    # add shared arguments
    dataset_args(parser)
    linear_augmentations_args(parser)
    custom_dataset_args(parser)

    # add pytorch lightning trainer args
    parser = pl.Trainer.add_argparse_args(parser)

    # linear model
    parser = METHODS["linear"].add_model_specific_args(parser)

    # THIS LINE IS KEY TO PULL WANDB AND SAVE_CHECKPOINT
    parser.add_argument("--save_checkpoint", action="store_true")
    temp_args, _ = parser.parse_known_args()

    # optionally add checkpointer
    if temp_args.save_checkpoint:
        parser = Checkpointer.add_checkpointer_args(parser)

    # parse args
    args = parser.parse_args()
    additional_setup_linear(args)

    return args


def parse_args_knn() -> argparse.Namespace:
    """Parses arguments for offline K-NN.

    Returns:
        argparse.Namespace: a namespace containing all args needed for pretraining.
    """

    parser = argparse.ArgumentParser()

    # add knn args
    parser.add_argument("--pretrained_checkpoint_dir", type=str)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--num_workers", type=int, default=10)
    parser.add_argument("--k", type=int, nargs="+")
    parser.add_argument("--temperature", type=float, nargs="+")
    parser.add_argument("--distance_function", type=str, nargs="+")
    parser.add_argument("--feature_type", type=str, nargs="+")

    # add shared arguments
    dataset_args(parser)
    custom_dataset_args(parser)

    # parse args
    args = parser.parse_args()

    return args


def parse_args_umap() -> argparse.Namespace:
    """Parses arguments for offline UMAP.

    Returns:
        argparse.Namespace: a namespace containing all args needed for pretraining.
    """

    parser = argparse.ArgumentParser()

    # add knn args
    parser.add_argument("--pretrained_checkpoint_dir", type=str)
    parser.add_argument("--batch_size", type=int, default=16)
    parser.add_argument("--num_workers", type=int, default=10)

    # add shared arguments
    dataset_args(parser)
    custom_dataset_args(parser)

    # parse args
    args = parser.parse_args()

    return args
