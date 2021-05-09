import os

import json
import pickle
from datetime import datetime
from IPython.display import display, HTML

import pandas as pd

def create_directory(function):
    """
    Decolator used to create directory if directory is not exist
    """
    def create_dir(*args, **kwargs):
        dirname = os.path.dirname(kwargs["filename"])
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        return function(*args, **kwargs)
    return create_dir

def copy_directory(src, dest):
    """
    Copy files or directorys from source to destination
    src (str) : path to files or directorys that will be copied
    dest (str) : path to place copied files or directorys
    """
    if "." in os.path.basename(src):
        shutil.copyfile(src, dest)
    else:
        try:
            shutil.copytree(src, dest)
        # Directories are the same
        except shutil.Error as e:
            print('Directory not copied. Error: %s' % e)
        # Any error saying that the directory doesn't exist
        except OSError as e:
            print('Directory not copied. Error: %s' % e)

@create_directory
def save_json(json_dict, filename):
    with open(filename, "w") as f:
        json.dump(json_dict, f)

def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data

@create_directory
def save_text(data, filename, encoding="utf-8"):
    with open(filename, "w", encoding=encoding) as f:
        f.write(str(data))

def read_text(filename, encoding="utf-8"):
    with open(filename, "r", encoding=encoding) as f:
        text = f.read()
    return text

@create_directory
def save_pickle(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def read_pickle(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

# Read Utility
def read_csv_from_directory(dirpath):
    file_list = os.listdir(dirpath)
    df_list = []
    for filename in file_list:
        df = pd.read_csv(f"{dirpath}{filename}")
        df_list.append(df)
    return pd.concat(df_list)
    
#alias
def pwb(*args, **kwargs):
    print_with_bracket(*args, **kwargs)

def print_with_bracket(*args, **kwargs):
    for v in args:
        text = "==arg==" * 10
        print(text)
        if isinstance(v, pd.DataFrame):
            display(v)
        else:
            print(v)
        print("=" * len(text))
    for key in kwargs:
        text = f"=={key}==" * 3
        print(text)
        if isinstance(kwargs[key], pd.DataFrame):
            display(kwargs[key])
        else:
            print(kwargs[key])
        print(f"=" * len(text))