# run_dygie_on_MUC 

Run dygiepp model(https://github.com/dwadden/dygiepp) on MUC-4 dataset

## Convert GTT format data to Dygie format data and add incident_types before each document

The processed folder contains strings that are not mentioned in the document (date + location) while processed_string only contains responses with direct mentions in the document.
```
cd run_dygie_on_MUC
python data/MUC_processes_string/process_muc.py
```

## Training a model

First, write a training config muc_processed_string_{max_span_width}_{coref_loss_weights}.jsonnet. Then run

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

This output file ca be used to do Automatic Error Analysis for Document-level Information Extraction(https://github.com/IceJinx33/auto-err-template-fill)
