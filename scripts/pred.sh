allennlp predict models/muc_processed_string_10_0.1_36/model.tar.gz \
    data/MUC_processed_string/new_test.json \
    --predictor dygie \
    --include-package dygie \
    --use-dataset-reader \
    --output-file predictions_fyc/muc_processed_string_10_0.1_36.jsonl \
    --cuda-device 0 \
    --silent