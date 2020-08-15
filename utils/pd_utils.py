import pandas as pd

def to_dict_dropna(df):
    return [{k.strip():v.strip() if isinstance(v, str) else v for k,v in m.items() if pd.notnull(v)} for m in df.to_dict(orient='records')]

def read_tsv(filename, dropna=True):
    df = pd.read_csv(filename, sep='\t')
    if dropna:
        return to_dict_dropna(df)
    else:
        return df.to_dict(orient='records')


if __name__ == '__main__':
    filename = '/Users/caijinchao/projects/sportsKG/data/basketball/league.tsv'
    df = read_tsv(filename)
    print(df)