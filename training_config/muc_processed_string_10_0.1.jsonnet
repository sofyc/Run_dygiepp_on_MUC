local template = import "template.libsonnet";

template.DyGIE {
  bert_model: "bert-base-cased",
  cuda_device: 0,
  max_span_width: 10,
  data_paths: {
    train: "data/MUC_processed_string/new_train.json",
    validation: "data/MUC_processed_string/new_dev.json",
    test: "data/MUC_processed_string/new_test.json",
  },
  loss_weights: {
    ner: 1.0,
    relation:0.0,
    coref: 0.1,
    events: 0.0
  },
  data_loader +: {
    num_workers: 16
  },
  trainer +: {
    num_epochs: 18,
    optimizer +: {
      lr: 5e-4
    }
  },
  target_task: "ner"
}
