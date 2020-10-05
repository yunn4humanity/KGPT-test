# KGPT
Code and Data for EMNLP2020 Paper "KGPT: Knowledge-Grounded Pre-Training for Data-to-Text Generation"



## Download Preprocessed Dataset
```
wget https://kgpt.s3-us-west-2.amazonaws.com/dataset.zip
unzip dataset.zip
```

## Download Pre-trained KGPT model
```
wget https://kgpt.s3-us-west-2.amazonaws.com/models.zip
unzip models.zip
```

## Option1: Finetune on Full Set
Finetune the model on the full downstream dataset
### Sequence Encoder
  - WebNLG
    ```
      bash scripts/webnlg/finetune_sequence_webnlg_from_wikidata.sh 0 checkpoint_wikidata/checkpoint_sequence_head8_layer6_GPT2_maxfact12/model_ep14.pt
    ```
  - E2ENLG
    ```
      bash scripts/e2enlg/finetune_sequence_e2enlg_from_wikidata.sh 0 checkpoint_wikidata/checkpoint_sequence_head8_layer6_GPT2_maxfact12/model_ep14.pt
    ```
### Graph Encoder
  - WebNLG
    ```
      bash scripts/webnlg/finetune_graph_e2enlg_from_wikidata.sh 0 checkpoint_wikidata/checkpoint_sequence_head8_layer6_GPT2_maxfact12/model_ep14.pt
    ```
  - E2ENLG
    ```
      bash scripts/e2enlg/finetune_graph_e2enlg_from_wikidata.sh 0 checkpoint_wikidata/checkpoint_graph_head8_layer6_GPT2_maxfact12/model_ep14.pt
    ```

## Option2: Finetune for Few-Shot Leanring
Finetune the model on the 1% downstream dataset
- WebNLG
  ```
    scripts/webnlg/finetune_sequence_webnlg_from_wikidata_fewshot.sh 0 checkpoint_wikidata/checkpoint_sequence_head8_layer6_GPT2_maxfact12/model_ep14.pt 0.01
  ```
- E2ENLG
  ```
    bash scripts/e2enlg/finetune_sequence_e2enlg_from_wikidata.sh 0 checkpoint_wikidata/checkpoint_sequence_head8_layer6_GPT2_maxfact12/model_ep14.pt 0.01
  ```
  
## Model selection
Evaluate all the saved models on the validation set to select the best model.
### Sequence Encoder
  ```
    bash scripts/webnlg/eval_sequence_webnlg_all.sh 0 test checkpoint_webnlg/checkpoint_finetune_sequence_head8_layer6_GPT2_maxfact12/
  ```
### Graph Encoder
  ```
    bash scripts/webnlg/eval_graph_webnlg_all.sh 0 test checkpoint_webnlg/checkpoint_finetune_graph_head8_layer6_GPT2_maxfact12/
  ```

## Final test
For example, the model at 20th epoch arrives the best score, then you will output prediction using the following command.
### Sequence Encoder
  ```
    bash scripts/webnlg/eval_sequence_webnlg_all.sh 0 challenge checkpoint_webnlg/checkpoint_finetune_sequence_head8_layer6_GPT2_maxfact12/model_ep20.pt
  ```
### Graph Encoder
  ```
    bash scripts/webnlg/eval_graph_webnlg_all.sh 0 challenge checkpoint_webnlg/checkpoint_finetune_graph_head8_layer6_GPT2_maxfact12/model_ep20.pt
  ```
