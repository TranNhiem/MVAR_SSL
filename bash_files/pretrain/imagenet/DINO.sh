python3 ../../../mv_ma_pretrain_edit.py \
    --dataset mv_ma \
    --mvar_training True \
    --experiment_type ablation \
    --job_name num_augmentation_mv \
    --backbone vit_small_v1 \
    --patch_size 16  \
    --data_dir /data1/1K_New/ \
    --train_dir train \
    --val_dir val \
    --subset_classes 10 \
    --dataset_size 13000 \
    --num_gpus 7 \
    --max_epochs 100 \
    --gpus 0,1,2,3,5,6,7 \
    --accelerator gpu \
    --strategy ddp \
    --sync_batchnorm \
    --precision 16 \
    --optimizer sgd \
    --eta_lars 0.001 \
    --exclude_bias_n_norm \
    --scheduler warmup_cosine \
    --lr 0.3 \
    --accumulate_grad_batches 1 \
    --classifier_lr 0.2 \
    --weight_decay 1e-6 \
    --batch_size 64 \
    --num_workers 20 \
    --num_augment_trategy SimCLR_RA_FA \
    --num_augment_strategies 3\
    --brightness 0.4 0.4 0.4 \
    --contrast 0.4 \
    --saturation 0.2 \
    --hue 0.1 \
    --color_jitter_prob 0.8 \
    --gray_scale_prob 0.2 \
    --horizontal_flip_prob 0.5 \
    --gaussian_prob 1.0  \
    --solarization_prob 0.2  \
    --crop_size 224  \
    --crop_size_glob 224 \
    --crop_size_loc 96 \
    --num_crop_glob 2 \
    --num_crop_loc 5 \
    --crop_type random_uniform \
    --min_scale_loc 0.1 \
    --max_scale_loc 0.3 \
    --min_scale_glob 0.3 \
    --max_scale_glob 1.0 \
    --rda_num_ops 2 \
    --rda_magnitude 9 \
    --ada_policy imagenet \
    --fda_policy imagenet \
    --num_crops_per_aug 1 1 1 \
    --shuffle_transforms_crops False\
    --name test_dino \
    --entity mlbrl \
    --project solo_MASSL_V2 \
    --wandb \
    --save_checkpoint \
    --method dino \
    --proj_output_dim 512 \
    --proj_hidden_dim 4096 \
    --base_tau_momentum 0.99 \
    --final_tau_momentum 1.0 \
    --momentum_classifier \
    --alpha 0.4  \
    --checkpoint_dir /data1/solo_MASSL_ckpt \
    --checkpoint_frequency 20 
