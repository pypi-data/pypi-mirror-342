from multiprocessing_manager import MultiprocessingManager


if __name__ == "__main__":
    # 设置参数
    mgf_folder = r"D:\work\WT2.0\WT_2\test_data\CRL_SIF_P_1"  # 单个样本文件夹路径
    outer_max_workers = 2  # 每次处理一个文件夹（一个样本处理完再处理下一个样本）
    inner_max_workers = 4 # 每个文件夹内并行处理 5 个 MGF 文件，每个文件内的多个 pepmass 也使用多进程处理
    out_dir = r"D:\work\WT2.0\WT_2\test_data"

    # 创建并启动多进程任务
    manager = MultiprocessingManager(outer_max_workers=outer_max_workers,
                                     inner_max_workers=inner_max_workers,
                                     mgf_folder=mgf_folder,
                                     out_dir=out_dir)
    manager.process_mgf_files()
