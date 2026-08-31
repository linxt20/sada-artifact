# 1. user chooses a dataset by name or selects all
# 2. the code will go to the datasets_notebooks directory and run the notebook based on the name -> make use of download_datasets.py
# 3. the code will run embedding functions based on the variable settings in __main__ -> make use of text_processors/preprocess_text.py
# 4. the code will downsample the loaded features by selected strategy -> make use of  feature_selection.py
# 5. the code will train a model out of a small selection of models based on the variable settings in __main__, by default it will do xgboost -> main part of this file, rest imported
import numpy as np
import json
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
import numpy as np
import os

def setup_project_root(path=None):
    if path:
        project_root = os.path.abspath(path)
        os.makedirs(project_root, exist_ok=True)
    else:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..'))

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    return project_root

def save_partial_results(run_timestamp, partial_results, results_path='results.json'):
    all_results = {}
    if os.path.exists(results_path):
        try:
            with open(results_path, 'r', encoding='utf-8') as f:
                all_results = json.load(f)
        except (json.JSONDecodeError, ValueError) as e:
            # Existing results file is corrupted (e.g. interrupted write or
            # concurrent run). Back it up and start fresh so we don't lose
            # the result we just computed.
            backup_path = f"{results_path}.corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            try:
                os.replace(results_path, backup_path)
                print(f"[save_partial_results] WARNING: '{results_path}' is "
                      f"corrupted ({e}). Backed up to '{backup_path}' and "
                      f"starting a fresh results file.")
            except OSError as move_err:
                print(f"[save_partial_results] WARNING: '{results_path}' is "
                      f"corrupted ({e}) and could not be backed up "
                      f"({move_err}). Overwriting.")
            all_results = {}

    all_results[run_timestamp] = partial_results

    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Main pipeline for dataset processing and model training.")    
    parser.add_argument('--dataset', type=str, default='it_salary', help='Name of the dataset to process (or a group of datasets).')
    parser.add_argument('--embed_methods', nargs='+', default=['fasttext', 'skrub', 'ag'], help='Methods for text embeddings.') 
    parser.add_argument('--save_format', type=str, default='npy', choices=['npy', 'pkl'], help='Format to save embeddings.')
    parser.add_argument('--project_root', type=Path, default=None, help='Output Path')
    parser.add_argument('--download_datasets', action='store_true', help='Run data preprocessing notebooks')
    parser.add_argument('--generate_embeddings', action='store_true', help='Run data preprocessing notebooks')
    parser.add_argument('--run_pipe', action='store_true', help='Run pipeline')
    parser.add_argument('--eval_method', default= 'tabpfn', choices=['xgb', 'tabpfn', 'autogluon'],help='Methods for text embeddings.')
    parser.add_argument('--downsample_methods', nargs='+', default=['t-test', 'anova', 'variance', 'pca', 'correlation', 'shap', 'random'], help='Methods for downsampling.') 
    parser.add_argument('--no_text', action='store_true', help='Drop Text Columns')
    parser.add_argument('--seed', type=int, default=0, help='Random seed for the stratified row downsample (vary for repeat runs / mean±std).')
    parser.add_argument('--ds_rows', type=int, default=3000, help='Row-downsample target; <=0 uses the FULL dataset (no row downsampling).')
    parser.add_argument('--emb_top_k', type=int, default=None, help='Fixed number of embedding dimensions to keep via the selector, regardless of default-column count. Makes the embedding budget uniform across conditions.')
    parser.add_argument('--per_fold_shap', action='store_true',
                        help='For XGBoost, fit SHAP embedding selection separately '
                             'inside each training fold instead of before cross-validation.')

    # NEW: user-provided CSV (rows only); summary/config still come from --dataset
    parser.add_argument('--custom_csv', type=str, default=None,
                        help='Path to a user-provided CSV that replaces rows; '
                             'summary/config come from --dataset.')
    parser.add_argument('--custom_tag', type=str, default=None,
                        help='Tag to isolate embedding cache & results when --custom_csv is used. '
                             'Defaults to the CSV file stem.')
    args = parser.parse_args()

    os.environ["PROJECT_ROOT"] = setup_project_root(args.project_root)

    from configs.dataset_configs import get_dataset_list, data_configs
    from pipelines.download_datasets import download_datasets
    from pipelines.embedd_text import (
        embedd_datasets, load_embedded_dataset,
        embedd_custom, load_embedded_dataset_custom,
    )
    from pipelines.feature_selection import downsample_features
    from pipelines.row_downsampling import downsample_rows_wrapper
    from pipelines.evaluation import (
        tabpfn_v2_eval, xgboost_eval, xgboost_eval_per_fold_shap,
        autogluon_eval,
    )

    RUN_TIMESTAMP = datetime.now().strftime('run_%Y%m%d_%H%M%S')

    # tag for custom-CSV mode (auto-derived from filename if not given)
    custom_tag = None
    if args.custom_csv:
        custom_tag = args.custom_tag or Path(args.custom_csv).stem

    run_results = {}
    
    # Block 1: Download and process datasets
    if args.download_datasets:
        if args.custom_csv:
            print("[main_pipeline] --download_datasets ignored in --custom_csv mode.")
        else:
            download_datasets(args.dataset)

    # Block 2: Take the features labeled as textual and embedd them according to the selected methods
    text_embedding_methods = args.embed_methods # -> we are taking all of them
    save_format = args.save_format  
    
    if args.generate_embeddings:
        if args.custom_csv:
            embedd_custom(
                dataset_name=args.dataset,
                csv_path=args.custom_csv,
                methods=text_embedding_methods,
                save_format=save_format,
                tag=custom_tag,
            )
        else:
            embedd_datasets(args.dataset, text_embedding_methods, save_format)

    
    if args.run_pipe:
        if args.custom_csv:
            dataset_name_list = [args.dataset]
        else:
            dataset_name_list = get_dataset_list(args.dataset)
        for dataset_name in dataset_name_list:
            
            # Block 3: Load the text emebeddings and the original data and merge them together into a single dataframe
            if args.custom_csv:
                data, bundle = load_embedded_dataset_custom(
                    dataset_name=dataset_name,
                    csv_path=args.custom_csv,
                    methods=text_embedding_methods,
                    save_format=save_format,
                    tag=custom_tag,
                )
            else:
                data, bundle = load_embedded_dataset(dataset_name, methods=text_embedding_methods, save_format=save_format)

            loaded_config = bundle['config']
            summary_df = bundle['summary']

            if args.no_text:
                text_columns = summary_df.loc[summary_df['Type'] == 'textual', 'Column Name'].tolist()
                df = bundle['data'].copy()
                df = df.drop(columns=[c for c in text_columns if c in df.columns])
                data = {'no-text': df}

            # Block 4: Downsample and Train
            seed = args.seed
            ds_rows = args.ds_rows
            ds_mode = 'stratified'
            if ds_rows and ds_rows > 0:
                data = downsample_rows_wrapper(data, target_col=loaded_config['target'], task=loaded_config['task'],mode=ds_mode, downsampled_rows=ds_rows, seed=seed)
            # else: ds_rows<=0 -> use the FULL dataset (no row downsampling)

            start_list = args.downsample_methods
            suffix = f"__{custom_tag}" if custom_tag else ""
            results_path = "."
            if args.eval_method == "tabpfn":
                max_features = 300
                data = downsample_features(data, config_df=loaded_config, summary_df=summary_df, max_features=max_features, strat_list=start_list, emb_top_k=args.emb_top_k)
                tabpfn_results = tabpfn_v2_eval(emb_df=data, config=loaded_config, eval_cvg=data_configs[dataset_name])
                dataset_results = {
                    "tabpfn": tabpfn_results,
                }
                results_path = f"tabpfn_results_{dataset_name}{suffix}.json"
            elif args.eval_method == "xgb":
                max_features = 300
                if args.per_fold_shap:
                    if start_list != ['shap']:
                        raise ValueError(
                            "--per_fold_shap requires --downsample_methods shap"
                        )
                    xgb_results = xgboost_eval_per_fold_shap(
                        emb_df=data,
                        config=loaded_config,
                        summary_df=summary_df,
                        eval_cvg=data_configs[dataset_name],
                        emb_top_k=args.emb_top_k or 64,
                        seed=seed,
                    )
                else:
                    data = downsample_features(data, config_df=loaded_config, summary_df=summary_df, max_features=max_features, strat_list=start_list, emb_top_k=args.emb_top_k)
                    xgb_results = xgboost_eval(emb_df=data, config=loaded_config, eval_cvg=data_configs[dataset_name], seed=seed)
                dataset_results = {
                    "xgb": xgb_results,
                }
                results_path = f"xgb_results_{args.dataset}{suffix}.json"
            elif args.eval_method == "autogluon":
                max_features = 300
                data = downsample_features(data, config_df=loaded_config, summary_df=summary_df, max_features=max_features, strat_list=start_list, emb_top_k=args.emb_top_k)
                autogluon_results = autogluon_eval(emb_df=data, config=loaded_config, eval_cvg=data_configs[dataset_name])
                dataset_results = {
                    "autogluon": autogluon_results,
                }
                results_path = f"autogluon_results_{args.dataset}{suffix}.json"
            else:
                raise ValueError(f"Unsupported evaluation method: '{args.eval_method}'. Supported methods are: 'tabpfn', 'xgb', 'autogluon'.")

            run_results[dataset_name] = dataset_results
            save_partial_results(RUN_TIMESTAMP, run_results,results_path=results_path)


