import os
import pandas as pd
import numpy as np
from src.utils.molecular_weights import MOLECULAR_WEIGHTS

def create_ascii_plot(data, column, width=80, height=20, title=None):
    """
    為指定列創建 ASCII 圖表
    
    Parameters:
    data (pd.Series): 數據列
    column (str): 列名
    width (int): 圖表寬度
    height (int): 圖表高度
    title (str, optional): 圖表標題
    
    Returns:
    str: ASCII 圖表字符串
    """
    if data.empty:
        return "No data available"
    
    # 計算最小值和最大值
    min_val = data.min()
    max_val = data.max()
    if min_val == max_val:
        return "No variation in data"
    
    # 創建圖表
    chart = []
    for i in range(height):
        row = []
        for j in range(width):
            if j == 0:
                row.append('|')
            else:
                row.append(' ')
        chart.append(row)
    
    # 添加數據點
    for i, val in enumerate(data):
        x = int((i / (len(data) - 1)) * (width - 2)) + 1
        y = int(((val - min_val) / (max_val - min_val)) * (height - 1))
        chart[height - 1 - y][x] = '*'
    
    # 添加底部邊框
    chart.append(['+'] + ['-'] * (width - 1))
    
    # 添加標籤
    if title:
        chart.insert(0, [title.center(width)])
    
    # 轉換為字符串
    return '\n'.join([''.join(row) for row in chart])

def print_ascii_summary(result_df, species_list):
    """
    打印 ASCII 摘要
    
    Parameters:
    result_df (pd.DataFrame): 結果數據框
    species_list (list): 物種列表
    """
    print("\nASCII 摘要:")
    for species in species_list:
        if species in result_df.columns:
            print(f"\n{species}:")
            print(create_ascii_plot(result_df[species], species))
            print(f"起始值: {result_df[species].iloc[0]:.2f}")
            print(f"最終值: {result_df[species].iloc[-1]:.2f}")
            print(f"變化: {result_df[species].iloc[-1] - result_df[species].iloc[0]:.2f}")
            print(f"最小值: {result_df[species].min():.2f}")
            print(f"最大值: {result_df[species].max():.2f}")
            print(f"平均值: {result_df[species].mean():.2f}")

def print_simple_trend_table(result_df, species_list, num_points=10):
    """
    打印簡單的趨勢表
    
    Parameters:
    result_df (pd.DataFrame): 結果數據框
    species_list (list): 物種列表
    num_points (int): 要顯示的點數
    """
    print("\n簡單趨勢表:")
    step = len(result_df) // num_points
    if step == 0:
        step = 1
    
    # 打印表頭
    header = "Time".ljust(10)
    for species in species_list:
        if species in result_df.columns:
            header += f" | {species}".ljust(15)
    print(header)
    print("-" * len(header))
    
    # 打印數據
    for i in range(0, len(result_df), step):
        row = f"{result_df['Time'].iloc[i]:.1f}".ljust(10)
        for species in species_list:
            if species in result_df.columns:
                row += f" | {result_df[species].iloc[i]:.2f}".ljust(15)
        print(row)

def print_terminal_visualizations(result_df):
    """
    打印終端機可視化
    
    Parameters:
    result_df (pd.DataFrame): 結果數據框
    
    Returns:
    str: 格式化後的結果字符串
    """
    # 獲取最後一個時間點
    last_time = result_df['Time'].iloc[-1]
    
    # 獲取最後一個時間點的數據
    last_row = result_df.iloc[-1]
    
    # 構建結果字符串
    result_str = f"{'=' * 60}\n"
    result_str += f"Time: {last_time:.1f} s\n"
    result_str += f"{'-' * 60}\n"
    result_str += "DRY-BASE MOLE FRACTIONS:\n"
    
    # 添加主要物種
    for species in ['O2', 'N2', 'CO2']:
        if f'{species} (%)' in last_row:
            result_str += f"  {species}: {last_row[f'{species} (%)']:6.2f} %\n"
    
    # 添加 CO
    if 'CO (%)' in last_row:
        result_str += f"CO: {last_row['CO (%)'] * 10000:6.2f} ppm\n"
    
    result_str += f"{'-' * 60}\n"
    
    # 添加溫度
    if 'Temperature (K)' in last_row:
        result_str += f"Temperature: {last_row['Temperature (K)']:8.2f} K\n"
        result_str += f"{'-' * 60}\n"
    
    # 添加 NOx 和 NH3
    if 'NOx (ppm)' in last_row:
        result_str += f"NOx: {last_row['NOx (ppm)']:8.2f} ppm\n"
    if 'NH3 (ppm)' in last_row:
        result_str += f"NH3: {last_row['NH3 (ppm)']:8.2f} ppm\n"
    
    # 打印到終端
    print(result_str)
    
    return result_str 