---
library_name: peft
license: other
base_model: C:\Users\Administrator\.cache\modelscope\models\Qwen--Qwen2.5-0.5B\snapshots\master
tags:
- base_model:adapter:C:\Users\Administrator\.cache\modelscope\models\Qwen--Qwen2.5-0.5B\snapshots\master
- llama-factory
- lora
- transformers
pipeline_tag: text-generation
model-index:
- name: train_2026-09-02-10-24-13
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# train_2026-09-02-10-24-13

This model is a fine-tuned version of [C:\Users\Administrator\.cache\modelscope\models\Qwen--Qwen2.5-0.5B\snapshots\master](https://huggingface.co/C:\Users\Administrator\.cache\modelscope\models\Qwen--Qwen2.5-0.5B\snapshots\master) on the lunyu_sample dataset.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 2
- eval_batch_size: 8
- seed: 42
- gradient_accumulation_steps: 2
- total_train_batch_size: 4
- optimizer: Use OptimizerNames.ADAMW_TORCH with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: cosine
- num_epochs: 3.0

### Training results



### Framework versions

- PEFT 0.18.1
- Transformers 5.6.0
- Pytorch 2.13.0+cpu
- Datasets 4.0.0
- Tokenizers 0.22.2