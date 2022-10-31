# If data type is conll where the common format of each line is token\tpos_tag\tchunk_tag
## python create_features_for_chunk_crf_training.py --input Sample-Odia-CoNLL/ --output sample_odia_chunk_features.txt --type conll
# If data type is SSF for SSF annotated POS files
## python create_features_for_chunk_crf_training.py --input Sample-Odia-SSF/ --output sample_odia_chunk_features.txt --type ssf
# How to train a crf using CRF++ toolkit (https://taku910.github.io/crfpp/), requires a template for reading features
## crf_learn template-chunk-window5-token-pos feature_file_path model_chunk_odia.m
