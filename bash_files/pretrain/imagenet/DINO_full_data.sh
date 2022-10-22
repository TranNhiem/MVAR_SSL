python3 ../../../mv_ma_pretrain_edit.py \
    --dataset mv_ma \
    --mvar_training True \
    --experiment_type ablation \
    --job_name vit_full_imagenet \
    --backbone vit_small_v1 \
    --drop_path_rate 0.05 \
    --patch_size 16  \
    --data_dir /data1/1K_New/ \
    --train_dir train \
    --val_dir val \
    --subset_classes 1000 \
    --dataset_size 1281167 \
    --num_gpus 8 \
    --max_epochs 300 \
    --gpus 0,1,2,3,4,5,6,7 \
    --check_val_every_n_epoch 4 \
    --accelerator gpu \
    --strategy ddp \
    --sync_batchnorm \
    --precision 16 \
    --optimizer adamw \
    --student_temperature 0.1 \
    --warmup_teacher_temperature_epochs 30 \
    --warmup_teacher_temperature 0.04 \
    --teacher_temperature 0.07 \
    --center_momentum 0.9 \
    --eta_lars 0.001 \
    --exclude_bias_n_norm \
    --scheduler warmup_cosine \
    --warmup_start_lr 3e-5  \
    --interval step \
    --lr 0.0005 \
    --min_lr 1e-5  \
    --accumulate_grad_batches 1 \
    --classifier_lr 0.1 \
    --knn_eval \
    --knn_k 20 \
    --weight_decay_scheduler cosine_schedule \
    --wd_init 0.004 \
    --wd_final 0.4 \
    --batch_size 128 \
    --num_workers 20 \
    --num_augment_trategy SimCLR_RA \
    --num_augment_strategies 2 \
    --brightness 0.4 0.4  \
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
    --num_crop_loc 10 \
    --crop_type random_uniform \
    --min_scale_loc 0.1 \
    --max_scale_loc 0.4 \
    --min_scale_glob 0.4 \
    --max_scale_glob 1.0 \
    --rda_num_ops 2 \
    --rda_magnitude 9 \
    --ada_policy imagenet \
    --fda_policy imagenet \
    --num_crops_per_aug 1 1 \
    --shuffle_transforms_crops False\
    --name MVMA_DINO_ViTsmall_1048_SimCLR_RA_2_glob_10_loc_master \
    --entity tranrick \
    --project MVAR_SSRL \
    --wandb \
    --save_checkpoint \
    --method dino \
    --proj_input_dim 2048 \
    --proj_bottleneck_dim 256 \
    --proj_hidden_dim 2048 \
    --num_prototypes 65536 \
    --freeze_last_layer_ -1 \
    --base_tau_momentum 0.996 \
    --final_tau_momentum 1.0 \
    --momentum_classifier \
    --alpha 0.5  \
    --checkpoint_dir /data1/solo_MASSL_ckpt \
    --checkpoint_frequency 20 
