import pandas as pd
import zipfile


def ReadStataDct(dct_file, **options):
    """Reads a Stata dictionary file.

    dct_file: string filename
    options: dict of options passed to open()

    returns: FixedWidthVariables object
    """
    type_map = dict(byte=int, int=int, long=int, float=float,
                    double=float, numeric=float)

    var_info = []
    with open(dct_file, **options) as f:
        for line in f:
            match = re.search(r'_column\(([^)]*)\)', line)
            if not match:
                continue
            start = int(match.group(1))
            t = line.split()
            vtype, name, fstring = t[1:4]
            name = name.lower()
            if vtype.startswith('str'):
                vtype = str
            else:
                vtype = type_map[vtype]
            long_desc = ' '.join(t[4:]).strip('"')
            var_info.append((start, vtype, name, fstring, long_desc))

    columns = ['start', 'type', 'name', 'fstring', 'desc']
    variables = pandas.DataFrame(var_info, columns=columns)

    # fill in the end column by shifting the start column
    variables['end'] = variables.start.shift(-1)
    variables.loc[len(variables) - 1, 'end'] = 0

    dct = FixedWidthVariables(variables, index_base=1)
    return dct





def ReadData(dct_file='athlete_events.csv.zip',
             dat_file='athlete_events.csv'):
    dct =
    df = dct_file.ReadFixedWidth(dct_file)
    return pd.read_csv(df)


def CleanReadData(df):
    pass


def main():
    data = ReadData()
    data.head()

if __name__ == '__main__':
    main()
