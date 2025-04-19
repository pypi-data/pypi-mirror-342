import os
import json
from numpy.random import randint


def open_json(json_file):
    with open(json_file) as data:
        return json.load(data)


def read_query(path):
    fd = open(path, 'r')
    sqlFile = fd.read()
    fd.close()
    return sqlFile


def write_dotenv(env, file=".env"):
    """
    python-dotenv dont have any function to overwrite .env file
    write_dotenv is just a write variables in text file
    """
    with open(".env", "w") as f:
        for i in env:
            f.write(f'{i}={env[i]}\n')


def to_print_dict(dic: dict, spaces=4):
    """
    @ make the dict a key: value table string
    """
    ret = ''
    for i in dic:
        ret = ret + '\n' + f"{i}: {dic[i]}"
    return ret


def print_dict(dic: dict):
    """
    @ just print to_print_dict
    """
    print(to_print_dict(dic))


def sample(vec):
    """Return 1 random value of a vector 
    Args:
        vec :list: list or a pd.Series or pd.Dataframe
    Returns:
        what is inside the list/dataframe/series index []
    """
    return vec[randint(len(vec))]


def to_print_list(ls, skip_rows=False):
    """just remove [] from list to print it"""
    ret = ''
    skip = None
    if skip_rows:
        skip = '\n'
    for i in ls:
        ret = ret+f'{i},{skip}'
    return ret[:-1]


def print_list(ls):
    """print the list without []"""
    print(to_print_list(ls))
