import os
import sys
import argparse
import pandas as pd
from src.data_processing.data_parser import find_data_file, parse_openfoam_data
from src.data_processing.conversion import convert_mass_to_mole_fraction, calculate_dry_base_mole_fraction
from src.visualization.gnuplot import create_gnuplot_script, run_gnuplot
from src.visualization.terminal import print_terminal_visualizations
from src.utils.molecular_weights import MOLECULAR_WEIGHTS

def process_data(file_path=None):
    """
    處理 OpenFOAM 數據文件
    
    Parameters:
    file_path (str, optional): 數據文件的路徑。如果為 None，將自動查找。
    
    Returns:
    pd.DataFrame: 處理後的數據框
    """
    # 創建輸出目錄
    output_dir = "gnuplot_results"
    os.makedirs(output_dir, exist_ok=True)
    
    # 查找並解析數據文件
    try:
        if file_path is None:
            file_path = find_data_file()
        df, time_col = parse_openfoam_data(file_path)
        
        # 提取簡化的列名以便處理
        simplified_cols = {}
        for col in df.columns:
            if 'areaAverage' in col:
                var_name = col.replace('areaAverage(', '').replace(')', '')
                simplified_cols[col] = var_name
        
        # 識別物種列
        species_cols = []
        for species in MOLECULAR_WEIGHTS.keys():
            matching_cols = [col for col in df.columns if col == species]
            if matching_cols:
                species_cols.extend(matching_cols)
        
        if not species_cols:
            species_cols = [col for col in df.columns if any(s in col for s in MOLECULAR_WEIGHTS.keys())]
        
        print(f"找到物種列: {species_cols}")
        
        # 檢查溫度列
        has_temperature = False
        temp_col = None
        
        if 'T' in df.columns:
            has_temperature = True
            temp_col = 'T'
            print(f"找到溫度列 (精確匹配): {temp_col}")
        else:
            for col in df.columns:
                if 'T)' in col or 'temperature' in col.lower():
                    has_temperature = True
                    temp_col = col
                    print(f"找到溫度列 (模式匹配): {temp_col}")
                    break
        
        if temp_col:
            temp_values = df[temp_col].astype(float)
            temp_avg = temp_values.mean()
            print(f"溫度列平均值: {temp_avg}")
            
            if temp_avg < 100 or temp_avg > 5000:
                print("警告: 溫度值似乎超出典型範圍 (200-3000K)")
                print(f"前幾個溫度值: {temp_values.head().tolist()}")
        
        # 查找水列
        water_col = None
        if 'H2O' in df.columns:
            water_col = 'H2O'
            print(f"找到 H2O 列 (精確匹配): {water_col}")
        else:
            for col in df.columns:
                if col.lower() == 'h2o' or 'water' in col.lower():
                    water_col = col
                    species_cols.append(col)
                    print(f"使用替代模式找到 H2O 列: {water_col}")
                    break
        
        # 將質量分數轉換為摩爾分數
        mole_df = convert_mass_to_mole_fraction(df, species_cols)
        
        # 計算乾基摩爾分數
        dry_mole_df = calculate_dry_base_mole_fraction(mole_df, water_col)
        
        # 提取關鍵列並轉換為百分比用於繪圖
        result_df = pd.DataFrame()
        result_df['Time'] = df[time_col]
        
        # 處理主要物種 (CO, CO2, O2, N2) - 轉換為百分比
        for species in ['O2', 'CO', 'CO2', 'N2']:
            if species in dry_mole_df.columns:
                result_df[f'{species} (%)'] = dry_mole_df[species] * 100
            else:
                species_cols = [col for col in dry_mole_df.columns if species in col]
                if species_cols:
                    col = species_cols[0]
                    result_df[f'{species} (%)'] = dry_mole_df[col] * 100
                else:
                    print(f"警告: 未找到 {species} 的列")
                    result_df[f'{species} (%)'] = 0
        
        # 檢查 H2O
        has_h2o = False
        if water_col:
            has_h2o = True
            print(f"添加 H2O 列到結果")
            result_df['H2O (%)'] = mole_df[water_col] * 100
        
        # 添加溫度數據（如果可用）
        if has_temperature:
            print(f"添加溫度列到結果")
            result_df['Temperature (K)'] = df[temp_col]
        
        # 檢查 NOx 物種並計算總 NOx（如果存在）
        nox_species = ['NO', 'NO2', 'N2O']
        nox_cols = []
        for nox in nox_species:
            if nox in dry_mole_df.columns:
                nox_cols.append(nox)
            else:
                matching_cols = [col for col in dry_mole_df.columns if nox in col]
                nox_cols.extend(matching_cols)
        
        has_nox = False
        if nox_cols:
            has_nox = True
            print(f"找到 NOx 列: {nox_cols}")
            result_df['NOx (ppm)'] = sum(dry_mole_df[col] * 1e6 for col in nox_cols)
        
        # 檢查 NH3 並添加到結果（如果存在）
        has_nh3 = False
        
        if 'NH3' in dry_mole_df.columns:
            has_nh3 = True
            print(f"找到 NH3 列 (精確匹配)")
            result_df['NH3 (ppm)'] = dry_mole_df['NH3'] * 1e6
        else:
            nh3_cols = [col for col in dry_mole_df.columns if 'NH3' in col]
            if nh3_cols:
                has_nh3 = True
                print(f"找到 NH3 列: {nh3_cols}")
                result_df['NH3 (ppm)'] = dry_mole_df[nh3_cols[0]] * 1e6
            else:
                for col in dry_mole_df.columns:
                    if 'ammonia' in col.lower() or 'nh3' in col.lower():
                        has_nh3 = True
                        print(f"使用替代模式找到 NH3 列: {col}")
                        result_df['NH3 (ppm)'] = dry_mole_df[col] * 1e6
                        break
                
                if not has_nh3 and 'NH3' in df.columns:
                    has_nh3 = True
                    print(f"在原始數據中找到 NH3 列")
                    try:
                        nh3_mole = df['NH3'] / MOLECULAR_WEIGHTS['NH3']
                        species_sum = sum(df[col] / MOLECULAR_WEIGHTS[s] 
                                          for col, s in [(c, m) for c in species_cols 
                                                        for m in MOLECULAR_WEIGHTS.keys() 
                                                        if m in c])
                        if species_sum == 0:
                            print("警告: 無法正確計算總摩爾數。使用近似值。")
                            result_df['NH3 (ppm)'] = df['NH3'] * 1e6
                        else:
                            nh3_fraction = nh3_mole / species_sum
                            result_df['NH3 (ppm)'] = nh3_fraction * 1e6
                    except Exception as e:
                        print(f"計算 NH3 ppm 時出錯: {e}。使用直接轉換。")
                        result_df['NH3 (ppm)'] = df['NH3'] * 1e6
        
        if not has_nh3:
            print("警告: 在數據中未找到 NH3 列")
        
        # 將結果保存為 CSV 以供參考
        csv_path = os.path.join(output_dir, 'species_mole_fractions.csv')
        result_df.to_csv(csv_path, index=False)
        print(f"保存結果到: {csv_path}")
        
        return result_df, has_nox, has_h2o, has_temperature, has_nh3
        
    except Exception as e:
        import traceback
        print(f"錯誤: {e}")
        traceback.print_exc()
        raise

def visualize_results(result_df, output_dir="gnuplot_results", has_nox=False, has_h2o=False, has_temperature=False, has_nh3=False):
    """
    生成可視化結果
    
    Parameters:
    result_df (pd.DataFrame): 處理後的數據框
    output_dir (str): 輸出目錄
    has_nox (bool): 是否有 NOx 數據
    has_h2o (bool): 是否有 H2O 數據
    has_temperature (bool): 是否有溫度數據
    has_nh3 (bool): 是否有 NH3 數據
    """
    # 創建 gnuplot 腳本並運行
    scripts = create_gnuplot_script(result_df, output_dir, has_nox, has_h2o, has_temperature, has_nh3)
    for script in scripts:
        run_gnuplot(script)
    
    # 添加終端機可視化以便在終端機環境中更好地查看
    print("\n" + "="*80)
    print("NOx、O2、CO2、NH3 的終端機可視化")
    print("="*80)
    print("(可視化已針對終端機查看進行優化)")
    
    # 打印終端機友好的可視化
    result_str = print_terminal_visualizations(result_df)
    
    # 將結果添加到 readme.txt
    with open('readme.txt', 'a') as f:
        f.write('\n' + result_str)
    
    print("\n" + "="*60)
    print(f"圖表保存在目錄: {os.path.abspath(output_dir)}")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(description='OpenFOAM 數據處理與可視化工具')
    parser.add_argument('--file', '-f', help='surfaceFieldValue.dat 文件的路徑')
    args = parser.parse_args()
    
    try:
        result_df, has_nox, has_h2o, has_temperature, has_nh3 = process_data(args.file)
        visualize_results(result_df, has_nox=has_nox, has_h2o=has_h2o, 
                         has_temperature=has_temperature, has_nh3=has_nh3)
    except Exception as e:
        import traceback
        print(f"發生錯誤: {e}")
        print("回溯:")
        traceback.print_exc()
        print("\n請使用 --file 選項提供 surfaceFieldValue.dat 的正確路徑:")
        print("示例: openfoam-postprocess --file /path/to/surfaceFieldValue.dat")

if __name__ == "__main__":
    main() 