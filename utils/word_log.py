from pathlib import Path

import pandas as pd
from pandas import DataFrame

def word_log(extracted_words, count, selected_ids, filename, experiment_number, condition_number):

    # データを二次元リスト(table)に変換
    log_df = DataFrame(extracted_words)
    log_df.insert(0, 'count', count)
    log_df.insert(4, 'is_selected', False)

    for selected_id in selected_ids:
        log_df.loc[log_df['id'] == int(selected_id), 'is_selected'] = True

    log_dir_path = Path('log') / f'experiment_{experiment_number}' / f'condition_{condition_number}'
    log_dir_path.mkdir(parents=True, exist_ok=True)
    log_file_path = log_dir_path / f'{filename}.csv'

    if count == 1:
        # 名前をつけてcsvを保存
        log_df.to_csv(log_file_path, index=False)
    else:
        # 保存されたcsvに，データを追加
        previous_log_df = pd.read_csv(log_file_path)
        new_log_df = pd.concat([previous_log_df, log_df]).reset_index().drop('index', axis=1)
        new_log_df.to_csv(log_file_path, index=False)
