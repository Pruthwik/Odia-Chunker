"""Create features for training Chunk CRF model from CoNLL or SSF annotated data."""
from argparse import ArgumentParser
import os
from re import findall
from re import DOTALL
from re import search
# input is the folder containing the CONLL or SSF files


def read_text_from_file(file_path):
    '''
    Read text from a file using a file path.

    :param file_path: File path of an input file

    :return text: Returns text read from file
    '''
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.read().strip()


def find_sentences_from_ssf_text(text):
    '''
    Find all the sentences from text annotated in SSF format.

    :param text: Text with SSF annotations

    :return sentences: Returns sentences extracted from SSF text
    '''
    sentence_pattern = '<Sentence id=.*?>\n(.*?)\n</Sentence>'
    return findall(sentence_pattern, text, DOTALL)


def read_lines_from_file(file_path):
    '''
    Read lines from a file.
    
    :param file_path: Path of the input file

    :return lines: Returns lines read from the file
    '''
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return file_read.readlines()


def read_file_and_find_features_from_sentences(file_path, data_type='conll'):
    '''
    Read a file and find features from sentences.
    
    :param file_path: File path of an input file

    :return features_string: Features for POS to train a CRF model.
    '''
    features_string = ''
    if data_type == 'conll':
        lines = read_lines_from_file(file_path)
        features_string = ''.join(lines)
    else:
        text = read_text_from_file(file_path)
        sentences_found = find_sentences_from_ssf_text(text)
        features_string = find_features_from_sentences(sentences_found)
    return features_string


def find_features_from_sentences(sentences):
    '''
    Find features for chunk from sentences.

    :param sentences: Sentences read from file

    :return features: Features of all tokens for each sentence combined for all the sentences
    '''
    features = ''
    for sentence in sentences:
        sentence_features = ''
        chunk_tag = ''
        tokens_in_chunk = []
        token_pos_chunk_list = []
        for line in sentence.split('\n'):
            line = line.strip()
            if line:
                line_split = line.split('\t')
                if search('^\d+\t\(\(\t[A-Z]+$', line):
                    chunk_tag = line_split[2]
                elif search('^\)\)', line):
                    token_pos_chunk_list = []
                    if tokens_in_chunk:
                        for index, (token, pos) in enumerate(tokens_in_chunk):
                            if index == 0:
                                chunk_tag_for_token = 'B-' + chunk_tag
                            else:
                                chunk_tag_for_token = 'I-' + chunk_tag
                            token_pos_chunk = '\t'.join([token, pos, chunk_tag_for_token])
                            token_pos_chunk_list.append(token_pos_chunk)
                        tokens_in_chunk = []
                        sentence_features += '\n'.join(token_pos_chunk_list) + '\n'
                        token_pos_chunk_list = []
                else:
                    token = line_split[1]
                    tag = line_split[2]
                    tag = tag.replace('__', '_')
                    tokens_in_chunk.append((token, tag))
        if sentence_features.strip():
            features += sentence_features + '\n'
    return features


def write_text_to_file(text, file_path):
    '''
    Write text to file.

    :param text: Text to be written
    :param file_path: File path of the output file
    :return: None
    '''
    with open(file_path, 'w', encoding='utf-8') as file_write:
        file_write.write(text)


def main():
    '''
    Pass arguments and call functions here.

    :param: None
    :return: None
    '''
    parser = ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input path from where tokens and its features will be extracted")
    parser.add_argument('--output', dest='out', help="Add the output file where the features will be saved")
    parser.add_argument('--type', dest='type', help="Add the type of the data either ssf or conll")
    args = parser.parse_args()
    print(args.type)
    if not os.path.isdir(args.inp):
        features_extracted = read_file_and_find_features_from_sentences(args.inp, args.type)
        write_text_to_file(features_extracted, args.out)
    else:
        all_features = ''
        for root, dirs, files in os.walk(args.inp):
            for fl in files:
                input_path = os.path.join(root, fl)
                features_extracted = read_file_and_find_features_from_sentences(input_path, args.type)
                all_features += features_extracted
            write_text_to_file(all_features, args.out)


if __name__ == '__main__':
    main()
