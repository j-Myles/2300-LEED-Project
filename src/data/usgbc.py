import data.prepare as prep
import data.process as proc
import data.clean as cl
import data.plot as pl
# TODO Add docstrings
#plt.interactive(False)

if __name__ == '__main__':
    # Get Data
    dpath = 'raw/boston_projects.xlsx'
    data_dir = 'C:\\Users\\Annie Waye\\Desktop\\NEU Sept 5\\EECE 2300\\code\\leed_building_analysis\\data\\'
    filepath = data_dir + dpath

    raw_data = prep.fetch_data(filepath)

    # Arrange Data in Columns
    pre_data = prep.pre_arrange_cols(raw_data)
    valid_frames = prep.get_valid_frames(pre_data)
    real_data = prep.arrange_cols(pre_data, valid_frames)

    # Clean/Format Data
    real_data = cl.remove_duplicates(real_data)
    real_data = cl.convert_dates(real_data)

    # Start Analyzing Data
    proc_data = proc.fit_encode(real_data)
    proc_date_data = proc.analyze_by_date(proc_data)

    # Start Plotting Data
    pl.primary_plot(proc_date_data, 'Certification')
    #pl.primary_plot(proc_date_data, 'Construction')
    #print(proc_data)