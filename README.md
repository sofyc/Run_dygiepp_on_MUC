# Run_dygiepp_on_muc

Run dygiepp model(https://github.com/dwadden/dygiepp) on MUC-4 dataset

The MUC dataset has a role called incident_type that can only be one of {'kidnapping': 0, 'attack':1, 'bombing':2, 'robbery':3, 'arson':4, 'bombing / attack':5, 'attack / bombing':6, 'forced work stoppage':7}. We modify the original Dygiepp so that the predicted incident_type can only be one of the labels.

## Convert GTT format data to Dygie format data and add incident_types before each document

Aliva(https://github.com/IceJinx33) processed MUC dataset. The processed folder contains strings that are not mentioned in the document (date + location) while processed_string only contains responses with direct mentions in the document.

To convert the processed data to Dygie format and add incident_types before each document, run
```
cd Run_dygiepp_on_muc
python data/MUC_processes_string/process_muc.py
```

## Training a model

Write a training config and a training script, then run the training scirpt.

```bash
scripts/train_muc_processed_string_{max_span_width}_{coref_loss_weights}.sh
```

## Making predictions on existing datasets

To make a prediction, you can use `allennlp predict`. For example, you can do:

```bash
allennlp predict models/muc_processed_string_{max_span_width}_{coref_loss_weights}/model.tar.gz \
    data/MUC_processed_string/new_test.json \
    --predictor dygie \
    --include-package dygie \
    --use-dataset-reader \
    --output-file predictions_fyc/muc_processed_string_{max_span_width}_{coref_loss_weights}.jsonl \
    --cuda-device 0 \
    --silent
```

## Creating the heuristic for clustering the DyGIE++ output to templates
```
python scripts/span_to_temp.py -i predictions_fyc/muc_processed_string_{max_span_width}_{coref_loss_weights}.jsonl -o template/muc_processed_string_template_{max_span_width}_{coref_loss_weights}.jsonl
```

## Creating the file used as input of the error analysis tool
```
python scripts/eval.py --pred_file template/muc_processed_string_template_{max_span_width}_{coref_loss_weights}.jsonl --gold_file data/MUC_processed_string/test.json --out_file error_input/muc_processed_string_{max_span_width}_{coref_loss_weights}.out 
```

This output file can be used to do Automatic Error Analysis for Document-level Information Extraction(https://github.com/IceJinx33/auto-err-template-fill).

## Eval result:

================= incident_type =================

P: 60.50%,  R: 58.74%, F1: 59.61%

================= incident_date =================

P: 68.00%,  R: 40.48%, F1: 50.75%

================= incident_location =================

P: 47.52%,  R: 20.25%, F1: 28.40%

================= PerpInd =================

P: 55.40%,  R: 29.31%, F1: 38.34%

================= PerpOrg =================

P: 60.67%,  R: 30.77%, F1: 40.83%

================= Target =================

P: 53.39%,  R: 30.67%, F1: 38.96%

================= Victim =================

P: 56.92%,  R: 35.00%, F1: 43.35%

================= Weapon =================

P: 57.69%,  R: 49.28%, F1: 53.15%

***************** micro_avg *****************

P: 56.26%,  R: 34.37%, F1: 42.67%

## Automatic Error Analysis Result:

total: Precision : 0.4760, Recall : 0.3429, F1 : 0.3986

incident_type: Precision : 0.6000, Recall : 0.5825, F1 : 0.5911

incident_date: Precision : 0.6800, Recall : 0.4048, F1 : 0.5075

incident_location: Precision : 0.4539, Recall : 0.2025, F1 : 0.2801

PerpInd: Precision : 0.3741, Recall : 0.2989, F1 : 0.3323

PerpOrg: Precision : 0.4494, Recall : 0.3077, F1 : 0.3653

Target: Precision : 0.3898, Recall : 0.3067, F1 : 0.3433

Weapon: Precision : 0.4231, Recall : 0.4783, F1 : 0.4490

Victim: Precision : 0.5385, Recall : 0.3500, F1 : 0.4242

Error Score: 1216.74988922394

