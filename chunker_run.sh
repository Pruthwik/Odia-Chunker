# Just give the input file as an argument
# and run sh chunker_run.sh $input_file
input_file=$1
crf_test -m odia_chunk_model_2k $input_file > output_file_pos_chunk.txt
cut -f1,3 output_file_pos_chunk.txt > output_file.txt
rm output_file_pos_chunk.txt

