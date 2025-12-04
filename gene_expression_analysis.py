import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
# 嘗試匯入 Scikit-learn，如果未安裝則會在後面處理
try:
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


# ==========================================================
# 階段一：讀取檔案 (使用你的完整路徑)
# ==========================================================
# 完整檔案路徑 (請確認這個路徑是正確的)
full_file_path = r"D:\UserData\Desktop\Sylveon\My_Bio_Project\1-U133AGNF1B.gcrma.avg.csv"

print(f"Attempting to read file from path: {full_file_path}")

try:
    # index_col=0 確保將第一欄 (Probe ID) 設為索引
    df = pd.read_csv(full_file_path, index_col=0) 
    print("\n✅ Stage 1: Data reading successful!")
    
except Exception as e:
    print(f"\n❌ Error during file reading: {e}")
    # 如果讀取失敗，則終止程式
    exit() 

# ==========================================================
# 階段二：資料轉置與準備 (EDA Preparation)
# ==========================================================
# 轉置資料，讓 Rows 是組織 (Samples)，Columns 是基因 (Features)
df_data = df.T 

print("\n--- Stage 2: Data Transposition ---")
print("Data Dimensions (Samples x Features):", df_data.shape)
print("First 5 rows (Rows are Tissues, Columns are Gene Expression):")
print(df_data.head())


# ==========================================================
# 階段三：特定基因表達視覺化 (使用修正後的 Probe ID 和英文標籤)
# ==========================================================
# 修正後的目標 Probe ID (確保存在於 GNF1H 晶片上)
actb_probe = '200001_at'  # ACTB (Housekeeping)
ins_probe = '203002_at'   # INS (Insulin/Pancreas marker)
myh11_probe = '201886_at' # MYL6B/Myosin related (Smooth Muscle marker substitute) 

target_probes = [actb_probe, ins_probe, myh11_probe] 
target_names = ['ACTB (Housekeeping)', 'INS (Pancreas Marker)', 'MYOSIN/MYL6B (Muscle Related)']

# 繪製條形圖 (Bar Plot)
plt.figure(figsize=(15, 12)) 
sns.set_style("whitegrid") 

for i, probe in enumerate(target_probes):
    # 檢查基因是否存在
    if probe not in df_data.columns:
        print(f"Warning: Probe ID not found: {probe}")
        continue
        
    # 建立子圖
    plt.subplot(3, 1, i + 1) # 3 Rows, 1 Column
    
    # 繪製條形圖
    sns.barplot(x=df_data.index, y=df_data[probe], color='deepskyblue')
    
    # 使用英文標籤
    plt.title(f'Gene {target_names[i]} ({probe}) Expression Across Tissues', fontsize=14)
    plt.ylabel('Expression Level (GCRMA)', fontsize=12)
    plt.xlabel('')
    
    # 旋轉 x 軸標籤以避免重疊
    plt.xticks(rotation=90, fontsize=8) 
    plt.tight_layout()

# 顯示條形圖
plt.show()

print("\n--- Stage 3 Complete: Specific gene expression plots generated ---")


# ==========================================================
# 階段四與五：機器學習 (PCA 降維與視覺化)
# ==========================================================
if ML_AVAILABLE:
    
    # 1. 標準化資料 (Standardization)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df_data) 

    # 2. 執行 PCA，降維到 2 個主成分
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(data_scaled)

    # 3. 將結果轉換回 DataFrame 方便畫圖
    pca_df = pd.DataFrame(data = principal_components, 
                          columns = ['PC1', 'PC2'], 
                          index = df_data.index)

    print("\n--- Stage 4 Complete: PCA data preparation finished ---")
    print("PCA Reduced Data (Samples x 2 Components):")
    print(pca_df.head())


    # 階段五：PCA 視覺化組織聚類
    plt.figure(figsize=(12, 10))
    sns.scatterplot(x='PC1', y='PC2', data=pca_df, s=100) 

    # 在每個點旁邊標註組織名稱
    for i in range(pca_df.shape[0]):
        plt.text(pca_df['PC1'][i] + 0.1, 
                 pca_df['PC2'][i] - 0.1, 
                 pca_df.index[i], 
                 fontsize=8)

    # 使用英文標籤
    plt.title('PCA Visualization of Tissue Gene Expression Profiles (PC1 vs PC2)', fontsize=16)
    plt.xlabel(f'Principal Component 1 (PC1 - Variance Explained: {pca.explained_variance_ratio_[0]*100:.1f}%)')
    plt.ylabel(f'Principal Component 2 (PC2 - Variance Explained: {pca.explained_variance_ratio_[1]*100:.1f}%)')
    plt.grid(True)
    plt.show()

    print("\n--- Project Complete: All figures generated ---")

else:
    print("\nWarning: scikit-learn not installed. Please run 'pip install scikit-learn' in your CMD and re-run the script to complete the PCA analysis.")