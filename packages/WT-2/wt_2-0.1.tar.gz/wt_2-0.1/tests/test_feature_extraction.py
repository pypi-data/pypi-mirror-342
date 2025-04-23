from mass_spec_processing.feature_extraction import FeatureExtractor
from mass_spec_processing.peak_grouping import PeakGroup


# 特征提取
feature_extractor = FeatureExtractor(mgf_file='sample.mgf', db_file='db_file.db', noise_threshold=200, Q3_cycles=5)
feature_extractor.create_intensity_table()
feature_extractor.insert_mz_data_to_database()

# 峰值分组
peak_group = PeakGroup(intensity_df, mz_df, rt_df, wid=6, sigma=2, min_noise=200, pepmass=500)
peak_df = peak_group.find_peak()
