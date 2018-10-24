import pandas as pd
import sklearn.preprocessing as skp
import sklearn.model_selection as skm


def read_data_spreadsheet(filename):
    """
    Reads excel...
    :param filename:
    :return: pd.DataFrame of all file contents
    """
    contents = pd.read_excel(filename)

    return contents


def add_primary(dataframe):
    col_name = dataframe.columns.values[0]
    dataframe.loc[-1] = col_name
    dataframe.index = dataframe.index + 1
    dataframe = dataframe.sort_index()
    dataframe = dataframe.rename(index=str, columns={col_name: 'all'})
    return dataframe


def check_certification(cert):
    return cert in ['Silver', 'Gold', 'Platinum', 'Certified']


def check_versioning(ver):
    return ver.startswith('v')


def valid_index_range(start, end):
    return end - start == 8


def get_valid_frames(dataframe):
    start_index = 0
    end_index = 0
    indices = []
    for index, row in dataframe.iterrows():
        val = row['all']
        if 'http' in val:
            indices.append((start_index, end_index))
            start_index = int(index) - 1
        if check_versioning(val):
            end_index = int(index)
        if check_certification(val):
            end_index = int(index)
    valid_indices = []
    for frame in indices:
        if valid_index_range(frame[0], frame[1]):
            valid_indices.append(frame)
    return valid_indices


def arrange_cols(dataframe, indices):
    df = pd.DataFrame(columns=['Name', 'Date', 'City',
                               'State', 'Country', 'Construction',
                               'Validation', 'Certification'])
    for frame in indices:
        start = frame[0]
        end = frame[1] + 1
        section = dataframe.iloc[start:end]
        col_vals = section['all'].values
        df_section = pd.DataFrame({'Name': [col_vals[0]],
                                   'Date': [col_vals[2]],
                                   'City': [col_vals[3]],
                                   'State': [col_vals[4]],
                                   'Country': [col_vals[5]],
                                   'Construction': [col_vals[6]],
                                   'Validation': [col_vals[7]],
                                   'Certification': [col_vals[8]]})
        df = df.append(df_section)
    df = df.reset_index(drop=True)
    return df


def remove_duplicates(dataframe):
    dataframe = dataframe.drop_duplicates()
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


def fit_encode(dataframe):
    processed = dataframe.copy()
    l_enc = skp.LabelEncoder()
    processed['Construction'] = l_enc.fit_transform(processed['Construction'])
    processed['Validation'] = l_enc.fit_transform(processed['Validation'])
    processed['Certification'] = l_enc.fit_transform(processed['Certification'])
    processed = processed.drop(['Name'], axis=1)
    return processed


def impl():
    dat = read_data_spreadsheet('raw/boston_projects.xlsx')
    dat = add_primary(dat)
    indices = get_valid_frames(dat)
    dat = arrange_cols(dat, indices)
    dat = remove_duplicates(dat)
    proc = fit_encode(dat)
    #print(proc)
    #dat = reformat(dat, indices)
    #print(dat)
    pass


impl()
