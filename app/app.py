import argparse
import os
import sys
import pathlib
import datetime

from flask import Flask, request, redirect, url_for, render_template, flash, send_from_directory, jsonify, session
from werkzeug.utils import secure_filename
import gensim

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from mains.main import extract_words_1
from mains.main2 import extract_words_2
from mains.main3 import extract_words_3
from mains.main4 import extract_words_4
from word_extractor.lexemes_vector import AutoextendExtractor
from utils.word_log import word_log

app = Flask(__name__)

UPLOAD_FOLDER = './app/static/uploads'
lexemes_filepath = './data/lexemes.txt'
mapping_filepath = './data/mapping.txt'
word2vec_filepath = './data/GoogleNews-vectors-negative300.bin'
app.secret_key = 'count'
app.secret_key = 'date'
app.secret_key = 'subject_name'
app.secret_key = 'extracted_words'

@app.route('/')
def index():
    session['count'] = 0
    session['date'] = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        selected_words_log = None

        # ログの保存
        if session['count'] == 0:
            session['subject_name'] = request.form.getlist('name')[0]

        if session['count'] >= 1:
            selected_ids = request.form.getlist('ids') # これは前回の選ばれたidであることに注意 一回目の処理にも注意
            print(selected_ids)
            previous_extracted_words = session['extracted_words']
            file_name = session['date'] + '_' + session['subject_name']
            experiment_number = app.config['experiment_number']
            condition_number = app.config['condition_number']
            selected_words_log = word_log(previous_extracted_words, session['count'], selected_ids, file_name, experiment_number, condition_number)

        session['count'] += 1
        print(session['count'], '回目')

        input_words = request.form.getlist('words')
        print('\n### extracting words ###\n')
        if app.config['condition_number'] == 1:
            extracted_words, links = extract_words_1(input_words, autoextend)
        elif app.config['condition_number'] == 2:
            extracted_words, links = extract_words_2(input_words, word2vec)
        # extracted_wordsの更新
        session['extracted_words'] = extracted_words
        print('\n### extracting compleded ###\n')


        return render_template('index.html', extracted_words=extracted_words, links=links, selected_words_log=selected_words_log) 
    else:
        return redirect(url_for('index'))

def choose_method(condition_number) -> object:    
    if condition_number == 1:
        return extract_words_1
    elif condition_number == 2:
        return extract_words_2
    elif condition_number == 3:
        return extract_words_3
    elif condition_number == 4:
        return extract_words_4

def parser():
    parser = argparse.ArgumentParser('app argument')
    parser.add_argument('-e','--experiment_number', type=int, default=0, help='experiment number')
    parser.add_argument('-c','--condition_number', type=int, default=1, help='condition number')
    parser.add_argument('-p','--port', type=int, default=80, help='condition number')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parser()
    condition_number = args.condition_number
    app.config['condition_number'] = condition_number
    app.config['experiment_number'] = args.experiment_number

    if condition_number == 1:
        print('\n### load AutoExtend ... ###\n')
        autoextend = AutoextendExtractor(lexemes_filepath, mapping_filepath)
    elif condition_number == 2:
        print('\n### load Word2vec ... ###\n')
        word2vec = gensim.models.KeyedVectors.load_word2vec_format(word2vec_filepath, binary=True)
    else:
        raise Exception('input valid condition number')
    print('\n### loading compleded ###\n')

    app.run(host="0.0.0.0", port=args.port, debug=True, threaded=True)