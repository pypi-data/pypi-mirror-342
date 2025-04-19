import os
import sys
import pandas as pd
import numpy as np
from src.utils.molecular_weights import MOLECULAR_WEIGHTS
import glob
import argparse

def find_data_file():
    """
    尋找 surfaceFieldValue.dat 文件
    
    Returns:
    str: 數據文件的路徑
    """
    # 檢查是否通過命令行參數提供文件路徑
    parser = argparse.ArgumentParser(description='處理 OpenFOAM surfaceFieldValue 數據。')
    parser.add_argument('--file', type=str, help='surfaceFieldValue.dat 文件的路徑')
    args, unknown = parser.parse_known_args()
    
    # 如果通過參數提供了文件路徑，使用它
    if args.file and os.path.exists(args.file):
        print(f"使用命令行參數提供的數據文件: {args.file}")
        return args.file
    
    # 檢查當前目錄是否存在 surfaceFieldValue.dat
    if os.path.exists('surfaceFieldValue.dat'):
        print(f"找到文件: surfaceFieldValue.dat")
        return 'surfaceFieldValue.dat'
    
    # 可能的文件位置列表
    possible_locations = [
        'surfaceFieldValue.dat',
        'postProcessing/surfaceFieldValue/surfaceFieldValue.dat',
        'postProcessing/outletSurface/*/surfaceFieldValue.dat',
        'postProcessing/*/surfaceFieldValue.dat',
        '*/surfaceFieldValue.dat',
        '*/**/surfaceFieldValue.dat'
    ]
    
    # 嘗試在每個位置尋找文件
    for pattern in possible_locations:
        try:
            matches = glob.glob(pattern, recursive=True)
            if matches:
                if '*' in pattern and len(matches) > 1:
                    try:
                        time_files = []
                        for file_path in matches:
                            dir_path = os.path.dirname(file_path)
                            time_dir = os.path.basename(dir_path)
                            try:
                                time_files.append((float(time_dir), file_path))
                            except ValueError:
                                time_files.append((float('inf'), file_path))
                        
                        time_files.sort(reverse=True)
                        latest_file = time_files[0][1]
                        print(f"找到多個文件，使用最新的: {latest_file}")
                        return latest_file
                    except (ValueError, IndexError):
                        print(f"找到文件: {matches[0]}")
                        return matches[0]
                else:
                    print(f"找到文件: {matches[0]}")
                    return matches[0]
        except Exception as e:
            print(f"搜索模式 {pattern} 時出錯: {e}")
    
    print("無法自動找到 surfaceFieldValue.dat 文件。")
    file_path = input("請輸入 surfaceFieldValue.dat 文件的路徑: ")
    
    if os.path.exists(file_path):
        return file_path
    else:
        raise FileNotFoundError(f"找不到文件: {file_path}")

def parse_openfoam_data(file_path):
    """
    解析 OpenFOAM surfaceFieldValue.dat 文件
    
    Parameters:
    file_path (str): 數據文件的路徑
    
    Returns:
    pd.DataFrame: 解析後的數據框
    str: 時間列的名稱
    """
    print(f"讀取文件: {file_path}")
    
    # 預定義的字段名稱
    expected_fields_12 = ["Time", "O2", "CO", "CO2", "H2", "CH4", "N2", "T", "p", "NO", "NO2", "N2O"]
    expected_fields_13 = ["Time", "O2", "CO", "CO2", "H2", "CH4", "N2", "T", "p", "NO", "NO2", "N2O", "NH3"]
    
    # 讀取數據文件
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # 過濾掉註釋和空行
    data_lines = [line for line in lines if not line.startswith('#') and line.strip()]
    
    if not data_lines:
        raise ValueError("文件中沒有找到數據行")
    
    # 分析數據中的列數
    column_counts = {}
    for line in data_lines:
        cols = len(line.strip().split())
        if cols in column_counts:
            column_counts[cols] += 1
        else:
            column_counts[cols] = 1
    
    print(f"檢測到數據中的列數: {column_counts}")
    
    # 查找列數變化的過渡點（如果有的話）
    has_transition = len(column_counts) > 1
    transition_index = None
    prev_cols = None
    
    if has_transition:
        print("檢測到數據文件中的列數變化！")
        for i, line in enumerate(data_lines):
            cols = len(line.strip().split())
            if prev_cols is not None and cols != prev_cols:
                transition_index = i
                print(f"列數在第 {i} 行從 {prev_cols} 變為 {cols}")
                break
            prev_cols = cols
    
    # 如果有過渡點，將數據分成兩部分
    if transition_index is not None:
        before_transition = data_lines[:transition_index]
        after_transition = data_lines[transition_index:]
        col_count_before = len(before_transition[0].strip().split()) if before_transition else 0
        col_count_after = len(after_transition[0].strip().split()) if after_transition else 0
        print(f"過渡前: {col_count_before} 列, {len(before_transition)} 行")
        print(f"過渡後: {col_count_after} 列, {len(after_transition)} 行")
        
        # 為每個部分選擇適當的字段名稱
        if col_count_before == 12 and col_count_after == 13:
            fields_before = expected_fields_12
            fields_after = expected_fields_13
            print("檢測到從 12 列（無 NH3）到 13 列（有 NH3）的過渡")
        elif col_count_before == 13 and col_count_after == 12:
            fields_before = expected_fields_13
            fields_after = expected_fields_12
            print("檢測到從 13 列（有 NH3）到 12 列（無 NH3）的過渡")
        else:
            fields_before = ["Time"] + [f"Field_{i}" for i in range(1, col_count_before)]
            fields_after = ["Time"] + [f"Field_{i}" for i in range(1, col_count_after)]
            print(f"對未知列結構使用通用字段名稱")
        
        # 分別解析兩個部分
        data_before = []
        for line in before_transition:
            values = line.strip().split()
            if len(values) == len(fields_before):
                data_before.append(values)
            else:
                print(f"警告: 跳過列數意外的行: {line[:40]}...")
        
        data_after = []
        for line in after_transition:
            values = line.strip().split()
            if len(values) == len(fields_after):
                data_after.append(values)
            else:
                print(f"警告: 跳過列數意外的行: {line[:40]}...")
        
        # 為兩個部分創建 DataFrame
        df_before = pd.DataFrame(data_before, columns=fields_before)
        df_after = pd.DataFrame(data_after, columns=fields_after)
        
        # 處理添加 NH3 的情況
        if col_count_before == 12 and col_count_after == 13:
            df_before['NH3'] = 0.0
            print("在過渡前的數據中添加 NH3=0 列")
            df = pd.concat([df_before, df_after], ignore_index=True)
            print(f"合併後的數據: {len(df)} 行")
            field_names = expected_fields_13
        elif col_count_before == 13 and col_count_after == 12:
            df_after['NH3'] = 0.0
            print("在過渡後的數據中添加 NH3=0 列")
            df = pd.concat([df_before, df_after], ignore_index=True)
            print(f"合併後的數據: {len(df)} 行")
            field_names = expected_fields_13
        else:
            if len(data_before) > len(data_after):
                print(f"僅使用過渡前的數據 ({len(data_before)} 行)")
                df = df_before
                field_names = fields_before
            else:
                print(f"僅使用過渡後的數據 ({len(data_after)} 行)")
                df = df_after
                field_names = fields_after
            print("警告: 檢測到不一致的列結構。僅使用一個部分的數據。")
    else:
        # 無過渡 - 使用一個字段列表處理所有數據
        col_count = list(column_counts.keys())[0] if column_counts else 0
        print(f"文件中列數一致 ({col_count})")
        
        if col_count == 12:
            field_names = expected_fields_12
        elif col_count == 13:
            field_names = expected_fields_13
        else:
            field_names = ["Time"] + [f"Field_{i}" for i in range(1, col_count)]
            print(f"對 {col_count} 列使用通用字段名稱")
        
        data = []
        for line in data_lines:
            values = line.strip().split()
            if len(values) == len(field_names):
                data.append(values)
            else:
                print(f"警告: 跳過列數意外的行: {line[:40]}...")
        
        df = pd.DataFrame(data, columns=field_names)
        
        if col_count == 12 and 'NH3' not in field_names:
            df['NH3'] = 0.0
            print("為所有數據添加 NH3=0 列")
            field_names = expected_fields_13
    
    # 轉換數值列
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception as e:
            print(f"警告: 無法將列 '{col}' 轉換為數值: {e}")
    
    # 打印調試信息
    print(f"最終 DataFrame: {len(df)} 行, {len(df.columns)} 列")
    print("最終列名:", df.columns.tolist())
    if len(df) > 0:
        print("\n第一行:")
        print(df.iloc[0].to_string())
        if len(df) > 1:
            print("\n最後一行:")
            print(df.iloc[-1].to_string())
    
    return df, "Time" 