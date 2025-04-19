import pandas as pd
import numpy as np
from src.utils.molecular_weights import MOLECULAR_WEIGHTS

def convert_mass_to_mole_fraction(df, species_cols):
    """
    將質量分數轉換為摩爾分數
    
    Parameters:
    df (pd.DataFrame): 包含質量分數的數據框
    species_cols (list): 代表物種的列名列表
    
    Returns:
    pd.DataFrame: 包含摩爾分數的數據框
    """
    # 創建摩爾分數的新數據框
    mole_df = df.copy()
    
    # 計算每個物種的摩爾數
    for col in species_cols:
        if col in df.columns:
            # 從列名中提取物種名稱
            for species in MOLECULAR_WEIGHTS.keys():
                if species in col:
                    mole_df[col] = df[col] / MOLECULAR_WEIGHTS[species]
                    print(f"使用 {species} 的分子量 {MOLECULAR_WEIGHTS[species]} 轉換 {col}")
                    break
    
    # 計算總摩爾數
    mole_df['total_moles'] = sum(mole_df[col] for col in species_cols if col in df.columns)
    
    # 計算摩爾分數
    for col in species_cols:
        if col in df.columns:
            mole_df[col] = mole_df[col] / mole_df['total_moles']
    
    return mole_df

def calculate_dry_base_mole_fraction(mole_df, water_col=None):
    """
    計算乾基摩爾分數
    
    Parameters:
    mole_df (pd.DataFrame): 包含摩爾分數的數據框
    water_col (str, optional): 水的列名。默認為 None。
    
    Returns:
    pd.DataFrame: 包含乾基摩爾分數的數據框
    """
    dry_df = mole_df.copy()
    
    # 如果存在水列，調整為乾基
    if water_col and water_col in mole_df.columns:
        dry_factor = 1 / (1 - mole_df[water_col])
        species_cols = [col for col in mole_df.columns if col != water_col and col != 'total_moles']
        
        for col in species_cols:
            dry_df[col] = mole_df[col] * dry_factor
    
    return dry_df 