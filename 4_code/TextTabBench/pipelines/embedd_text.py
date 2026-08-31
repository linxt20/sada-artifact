import os, sys
import pandas as pd
from datasets_notebooks.text_processors.preprocess_text import generate_text_embeddings, load_text_embeddings, embeddings_to_df
from configs.dataset_configs import get_dataset_list, get_a_dataset_dict
from datasets_notebooks.dataloader_functions.utils.log_msgs import info_msg, warn_msg, error_msg
from sklearn.preprocessing import OrdinalEncoder

project_root = os.environ["PROJECT_ROOT"]

def build_embedding_path(dataset_name: str) -> str:
    """
    Build the path to save the embeddings for a given dataset.
    
    Args:
        dataset_name (str): Name of the dataset.
    
    Returns:
        str: Path to save the embeddings.
    """
    datasets_dir = os.path.join(project_root, 'datasets_files', 'embeddings')
    dataset_config = get_a_dataset_dict(dataset_name)
    
    if dataset_config['task'] == 'clf':
        task_folder = 'classification'
    elif dataset_config['task'] == 'reg':
        task_folder = 'regression'
    else:
        raise ValueError(f"Unknown task type '{dataset_config['task']}' for dataset '{dataset_name}'.")

    if dataset_config['dataset_name']:
        dataset_folder_name = dataset_config['dataset_name']

    if not dataset_config:
        raise ValueError(f"Dataset '{dataset_name}' not found in configurations.")
    
    embedding_path = os.path.join(datasets_dir, task_folder, dataset_folder_name)
    
    return embedding_path

def build_pckl_path(dataset_name: str) -> str:
    """
    Build the path to load the raw data for a given dataset.
    
    Args:
        dataset_name (str): Name of the dataset.
    
    Returns:
        str: Path to load the raw data.
    """
    datasets_dir = os.path.join(project_root, 'datasets_notebooks', 'datasets_files', 'raw')
    dataset_config = get_a_dataset_dict(dataset_name)
    
    if dataset_config['task'] == 'clf':
        task_folder = 'classification'
    elif dataset_config['task'] == 'reg':
        task_folder = 'regression'
    else:
        raise ValueError(f"Unknown task type '{dataset_config['task']}' for dataset '{dataset_name}'.")

    if dataset_config['dataset_name']:
        dataset_folder_name = dataset_config['dataset_name']

    if not dataset_config:
        raise ValueError(f"Dataset '{dataset_name}' not found in configurations.")
    
    pckl_path = os.path.join(datasets_dir, task_folder, dataset_folder_name, f"{dataset_name}_processed.pkl")
    
    return pckl_path

def embedd_datasets(
        datasets_selection, 
        methods=['fasttext', 'ag', 'skrub'], 
        save_format='npy',
        output_path=None
        ):
    """
    Embedd the datasets using the selected methods.
    """

    dataset_name_list = get_dataset_list(datasets_selection)

    for dataset_name in dataset_name_list:
        # 1. load the raw data
        load_data_pth = build_pckl_path(dataset_name)
        if output_path:
            load_data_pth = os.path.join(output_path,load_data_pth)
        
        bundle = pd.read_pickle(load_data_pth)
        loaded_df = bundle['data']
        loaded_df.columns = loaded_df.columns.get_level_values(0)
        summary_df = bundle['summary']
        loaded_config = bundle['config']

        # 2. embedd and save the data
        save_embedding_path = build_embedding_path(dataset_name)
        if output_path:
            save_embedding_path = os.path.join(output_path,save_embedding_path)
        
        embeddings = generate_text_embeddings(
            df=loaded_df, 
            meta_df=summary_df, 
            emb_path=save_embedding_path, 
            methods=methods, 
            save_format=save_format
        )

def process_cats(df,summary_df):
    cat_cols = summary_df.loc[summary_df['Type'] == 'categorical', 'Column Name'].tolist()
    num_cols = summary_df.loc[summary_df['Type'] == 'numerical', 'Column Name'].tolist()
    for col in num_cols:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            coerced = pd.to_numeric(df[col], errors='coerce')
            if coerced.notna().any() and coerced.isna().mean() < 0.5:
                df[col] = coerced
            else:
                cat_cols.append(col)
    if cat_cols:
        df[cat_cols] = df[cat_cols].astype('string').fillna('__missing__').astype(object)
        encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
        df[cat_cols] = encoder.fit_transform(df[cat_cols])
    return df

def load_embeddings(dataset_name, methods):
    emb_path = build_embedding_path(dataset_name)
    embeddings = load_text_embeddings(emb_path=emb_path, methods=methods)
    return embeddings

def load_raw_bundle(dataset_name):
    dataset_config = get_a_dataset_dict(dataset_name)
    task_folder = 'classification' if dataset_config['task'] == 'clf' else 'regression'
    dataset_folder_name = dataset_config['dataset_name']

    load_data_pth = os.path.join(
        project_root,
        'datasets_notebooks', 'datasets_files', 'raw',
        task_folder, dataset_folder_name,
        f"{dataset_name}_processed.pkl"
    )

    bundle = pd.read_pickle(load_data_pth)
    bundle['data'].columns = bundle['data'].columns.get_level_values(0)
    bundle['data'] = process_cats(bundle['data'], bundle['summary'])
    return bundle

def load_embedded_dataset(dataset_name, methods=['fasttext', 'ag', 'skrub'], save_format='npy'):
    """
    Get the embedded dataset for a given dataset name.
    """
    # 1. load the embeddings
    embeddings = load_embeddings(dataset_name, methods)
    # 2. load the raw data
    bundle = load_raw_bundle(dataset_name)
    # 3. convert to df
    dfs = embeddings_to_df(embeddings, original_df=bundle["data"], meta_df=bundle["summary"])
    return dfs, bundle

# ============================================================
# Custom-CSV support: replace bundle['data'] rows with a user CSV,
# but keep the dataset's summary_df and config.
# ============================================================

def build_custom_embedding_path(dataset_name: str, tag: str) -> str:
    """Sibling of the original embedding folder, with __<tag> suffix to avoid clobbering."""
    base = build_embedding_path(dataset_name)
    return os.path.join(
        os.path.dirname(base),
        f"{os.path.basename(base)}__{tag}",
    )


def load_custom_bundle(dataset_name: str, csv_path: str, processed: bool = True):
    """
    summary_df + config come from <dataset>_processed.pkl;
    data rows come from the user's CSV (aligned to summary's column names).

    processed=False -> embedding generation stage (keep textual columns as raw text)
    processed=True  -> run_pipe stage (apply process_cats on categorical/numerical)
    """
    base_bundle = pd.read_pickle(build_pckl_path(dataset_name))

    if isinstance(base_bundle['data'].columns, pd.MultiIndex):
        base_bundle['data'].columns = base_bundle['data'].columns.get_level_values(0)

    summary_df = base_bundle['summary']
    loaded_config = base_bundle['config']

    df = pd.read_csv(csv_path)
    info_msg(f"[custom_csv] loaded CSV {csv_path} with shape {df.shape}")

    schema_cols = summary_df['Column Name'].tolist()
    target_col = loaded_config['target']
    if target_col not in df.columns:
        raise ValueError(
            f"Target column '{target_col}' not found in CSV: {csv_path}"
        )

    missing = [c for c in schema_cols if c not in df.columns]
    if missing:
        warn_msg(f"[custom_csv] columns missing in CSV (will be skipped): {missing}")

    keep = [c for c in schema_cols if c in df.columns]
    extra = [c for c in df.columns if c not in schema_cols and c != target_col]
    df = df[keep + extra].copy().reset_index(drop=True)

    # Extend summary_df with any columns the CSV adds beyond the original schema.
    # Infer type from dtype: numeric -> 'numerical', otherwise -> 'categorical'.
    if extra:
        extra_rows = []
        for col in extra:
            coerced = pd.to_numeric(df[col], errors='coerce')
            if pd.api.types.is_numeric_dtype(df[col]) or (
                coerced.notna().any() and coerced.isna().mean() < 0.5
            ):
                col_type = 'numerical'
            else:
                col_type = 'categorical'
            extra_rows.append({'Column Name': col, 'Type': col_type})
        summary_df = pd.concat(
            [summary_df, pd.DataFrame(extra_rows)],
            ignore_index=True,
        )
        info_msg(
            f"[custom_csv] added extra columns from CSV not in original schema: "
            f"{[(r['Column Name'], r['Type']) for r in extra_rows]}"
        )

    # textual columns must be string, not NaN/float
    text_cols = summary_df.loc[summary_df['Type'] == 'textual', 'Column Name'].tolist()
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].fillna('').astype(str)

    if processed:
        df = process_cats(df, summary_df)

    return {'data': df, 'summary': summary_df, 'config': loaded_config}


def embedd_custom(dataset_name, csv_path, methods, save_format, tag):
    """Generate embeddings from the user's CSV into an isolated cache folder."""
    bundle = load_custom_bundle(dataset_name, csv_path, processed=False)
    emb_path = build_custom_embedding_path(dataset_name, tag)
    os.makedirs(emb_path, exist_ok=True)
    info_msg(f"[custom_csv] writing embeddings to {emb_path}")
    generate_text_embeddings(
        df=bundle['data'],
        meta_df=bundle['summary'],
        emb_path=emb_path,
        methods=methods,
        save_format=save_format,
    )


def load_embedded_dataset_custom(dataset_name, csv_path, methods, save_format, tag):
    """Counterpart of load_embedded_dataset, but rows come from the user CSV."""
    bundle = load_custom_bundle(dataset_name, csv_path, processed=True)
    emb_path = build_custom_embedding_path(dataset_name, tag)
    embeddings = load_text_embeddings(emb_path=emb_path, methods=methods)
    dfs = embeddings_to_df(
        embeddings,
        original_df=bundle["data"],
        meta_df=bundle["summary"],
    )
    return dfs, bundle


if __name__ == "__main__":

    # BLock = 2 =
    # Take the features labeled as textual and embedd them according to the selected methods

    # 1. load the pp data:
    dataset_name = 'hs_cards'

    if False:
        embeddings = embedd_datasets(
            datasets_selection=dataset_name, 
            methods=['ag'], 
            save_format='npy'
        )
    else:

        df_path = build_pckl_path(dataset_name)
        bundle = pd.read_pickle(df_path)
        # 1. Extract components
        loaded_df = bundle['data']
        loaded_df.columns = loaded_df.columns.get_level_values(0)
        summary_df = bundle['summary']
        loaded_config = bundle['config']

        # 2. embedd and save the data
        generate_text_embeddings(
            df=loaded_df, 
            meta_df=summary_df, 
            emb_path=build_embedding_path(dataset_name),
            methods=['skrub'],
            save_format='npy'
        )
        # 3. load embeddings
        embeddings = load_text_embeddings(emb_path=build_embedding_path(dataset_name))

        # 4. convert to df
        dfs = embeddings_to_df(embeddings, original_df=loaded_df, meta_df=summary_df)

        # 5. aesthetic printing ✨
        for df_name, df in dfs.items():
            print(f"======{df_name}======")
            print(df.head(3))