import os
import subprocess
import pandas as pd
import numpy as np
from src.utils.molecular_weights import MOLECULAR_WEIGHTS

def create_gnuplot_script(result_df, output_dir, has_nox=False, has_h2o=False, has_temperature=False, has_nh3=False):
    """
    創建 gnuplot 繪圖腳本
    
    Parameters:
    result_df (pd.DataFrame): 結果數據框
    output_dir (str): 保存圖片的目錄
    has_nox (bool): 是否有 NOx 數據
    has_h2o (bool): 是否有 H2O 數據
    has_temperature (bool): 是否有溫度數據
    has_nh3 (bool): 是否有 NH3 數據
    
    Returns:
    list: gnuplot 腳本的路徑列表
    """
    # 確保輸出目錄存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 創建 gnuplot 的數據文件
    data_file = os.path.join(output_dir, "plot_data.dat")
    result_df.to_csv(data_file, sep='\t', index=False)
    
    # 保存列名和列位置用於調試
    print(f"gnuplot 數據列:")
    for i, col in enumerate(result_df.columns):
        print(f"  {i+1}: {col}")
    
    scripts = []
    
    # 創建 O2、N2、CO2 的 gnuplot 腳本
    main_species_script = os.path.join(output_dir, "plot_main_species.gp")
    with open(main_species_script, 'w') as f:
        f.write(f"""set terminal pngcairo enhanced font "Arial,12" size 800,600
set output "{os.path.join(output_dir, 'O2_N2_CO2.png')}"
set title "O2, N2, CO2 乾基摩爾分數 (%)" font "Arial,14"
set xlabel "時間 (s)" font "Arial,12"
set ylabel "摩爾分數 (%)" font "Arial,12"
set grid
set key outside top center horizontal
set style line 1 lc rgb "red" lw 2
set style line 3 lc rgb "green" lw 2
set style line 4 lc rgb "purple" lw 2
plot "{data_file}" using 1:2 with lines ls 1 title "O2 (%)", \\
     "{data_file}" using 1:4 with lines ls 3 title "CO2 (%)", \\
     "{data_file}" using 1:5 with lines ls 4 title "N2 (%)"
""")
    scripts.append(main_species_script)
    
    # 創建 CO 的 gnuplot 腳本（ppm）
    co_script = os.path.join(output_dir, "plot_co.gp")
    with open(co_script, 'w') as f:
        f.write(f"""set terminal pngcairo enhanced font "Arial,12" size 800,600
set output "{os.path.join(output_dir, 'CO_ppm.png')}"
set title "CO 濃度 (ppm)" font "Arial,14"
set xlabel "時間 (s)" font "Arial,12"
set ylabel "濃度 (ppm)" font "Arial,12"
set grid
set key outside top center horizontal
set style line 1 lc rgb "blue" lw 2
plot "{data_file}" using 1:($3*10000) with lines ls 1 title "CO (ppm)"
""")
    scripts.append(co_script)
    
    # 創建 NOx 的 gnuplot 腳本（如果可用）
    if has_nox:
        nox_col = None
        for i, col in enumerate(result_df.columns):
            if 'NOx' in col:
                nox_col = i + 1  # gnuplot 使用 1 索引列
                break
                
        if nox_col:
            nox_script = os.path.join(output_dir, "plot_nox.gp")
            with open(nox_script, 'w') as f:
                f.write(f"""set terminal pngcairo enhanced font "Arial,12" size 800,600
set output "{os.path.join(output_dir, 'NOx_ppm.png')}"
set title "NOx 濃度 (ppm)" font "Arial,14"
set xlabel "時間 (s)" font "Arial,12"
set ylabel "濃度 (ppm)" font "Arial,12"
set grid
set key outside top center horizontal
set style line 1 lc rgb "orange" lw 2
plot "{data_file}" using 1:{nox_col} with lines ls 1 title "NOx (ppm)"
""")
            scripts.append(nox_script)
            print(f"使用列 {nox_col} 創建 NOx 繪圖腳本")
    
    # 創建 NH3 的 gnuplot 腳本（如果可用）
    if has_nh3:
        nh3_col = None
        for i, col in enumerate(result_df.columns):
            if 'NH3' in col:
                nh3_col = i + 1  # gnuplot 使用 1 索引列
                break
                
        if nh3_col:
            nh3_script = os.path.join(output_dir, "plot_nh3.gp")
            with open(nh3_script, 'w') as f:
                f.write(f"""set terminal pngcairo enhanced font "Arial,12" size 800,600
set output "{os.path.join(output_dir, 'NH3_ppm.png')}"
set title "NH3 濃度 (ppm)" font "Arial,14"
set xlabel "時間 (s)" font "Arial,12"
set ylabel "濃度 (ppm)" font "Arial,12"
set grid
set key outside top center horizontal
set style line 1 lc rgb "magenta" lw 2
plot "{data_file}" using 1:{nh3_col} with lines ls 1 title "NH3 (ppm)"
""")
            scripts.append(nh3_script)
            print(f"使用列 {nh3_col} 創建 NH3 繪圖腳本")
    
    # 創建溫度的 gnuplot 腳本（如果可用）
    if has_temperature:
        temp_col = None
        # 查找溫度列
        for i, col in enumerate(result_df.columns):
            if 'Temperature' in col or 'temp' in col.lower():
                temp_col = i + 1  # gnuplot 使用 1 索引列
                break
        
        if temp_col:
            temp_script = os.path.join(output_dir, "plot_temperature.gp")
            with open(temp_script, 'w') as f:
                f.write(f"""set terminal pngcairo enhanced font "Arial,12" size 800,600
set output "{os.path.join(output_dir, 'Temperature.png')}"
set title "溫度 (K)" font "Arial,14"
set xlabel "時間 (s)" font "Arial,12"
set ylabel "溫度 (K)" font "Arial,12"
set grid
set key outside top center horizontal
set style line 1 lc rgb "red" lw 2
plot "{data_file}" using 1:{temp_col} with lines ls 1 title "溫度 (K)"
""")
            scripts.append(temp_script)
            print(f"使用列 {temp_col} 創建溫度繪圖腳本")
        else:
            print("警告: 在結果數據框中未找到溫度列")
    
    # 創建 H2O 的 gnuplot 腳本（如果可用）
    if has_h2o:
        h2o_col = None
        # 查找 H2O 列
        for i, col in enumerate(result_df.columns):
            if 'H2O' in col:
                h2o_col = i + 1  # gnuplot 使用 1 索引列
                break
                
        if h2o_col:
            h2o_script = os.path.join(output_dir, "plot_h2o.gp")
            with open(h2o_script, 'w') as f:
                f.write(f"""set terminal pngcairo enhanced font "Arial,12" size 800,600
set output "{os.path.join(output_dir, 'H2O.png')}"
set title "H2O 摩爾分數 (%)" font "Arial,14"
set xlabel "時間 (s)" font "Arial,12"
set ylabel "摩爾分數 (%)" font "Arial,12"
set grid
set key outside top center horizontal
set style line 1 lc rgb "blue" lw 2
plot "{data_file}" using 1:{h2o_col} with lines ls 1 title "H2O (%)"
""")
            scripts.append(h2o_script)
            print(f"使用列 {h2o_col} 創建 H2O 繪圖腳本")
    
    return scripts

def run_gnuplot(script_path):
    """
    運行 gnuplot 腳本
    
    Parameters:
    script_path (str): gnuplot 腳本的路徑
    """
    try:
        subprocess.run(['gnuplot', script_path], check=True)
        print(f"成功使用腳本生成圖表: {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"運行 gnuplot 時出錯: {e}")
    except FileNotFoundError:
        print("錯誤: 未安裝 gnuplot 或不在 PATH 中") 