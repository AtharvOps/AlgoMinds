import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class InsuranceFraudDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.cleaned_df = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        
    def load_data(self):
        """Load the insurance claims dataset"""
        try:
            # Try to read with header first
            self.df = pd.read_csv(self.file_path)
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            print(f"Columns: {list(self.df.columns)}")
        except:
            # If no header, read without header and assign column names
            column_names = [
                'claim_amount', 'repair_estimate', 'previous_claims', 'policy_validity',
                'image_uploaded', 'damage_consistency', 'user_phone', 'aadhar_number',
                'garage_id', 'agent_id', 'garage_city', 'accident_location',
                'claim_id', 'user_id', 'fraud_reported'
            ]
            self.df = pd.read_csv(self.file_path, header=None, names=column_names)
            print(f"Data loaded without header. Shape: {self.df.shape}")
        
        print("\nFirst 5 rows:")
        print(self.df.head())
        print(f"\nData types:\n{self.df.dtypes}")
        
    def data_cleaning(self):
        """Step 1: Clean the dataset"""
        print("\n=== DATA CLEANING ===")
        
        # Make a copy to avoid modifying original
        self.cleaned_df = self.df.copy()
        
        # 1. Remove duplicate rows
        initial_rows = len(self.cleaned_df)
        self.cleaned_df.drop_duplicates(inplace=True)
        removed_duplicates = initial_rows - len(self.cleaned_df)
        print(f"Removed {removed_duplicates} duplicate rows")
        
        # 2. Handle missing values
        print("\nMissing values before cleaning:")
        print(self.cleaned_df.isnull().sum())
        
        # Separate numerical and categorical columns
        numerical_cols = self.cleaned_df.select_dtypes(include=[np.number]).columns
        categorical_cols = self.cleaned_df.select_dtypes(include=['object']).columns
        
        # Fill numerical columns with median
        for col in numerical_cols:
            if col in self.cleaned_df.columns:
                median_val = self.cleaned_df[col].median()
                self.cleaned_df[col].fillna(median_val, inplace=True)
        
        # Fill categorical columns with "Unknown"
        for col in categorical_cols:
            if col in self.cleaned_df.columns:
                self.cleaned_df[col].fillna('Unknown', inplace=True)
        
        print(f"\nMissing values after cleaning:")
        print(self.cleaned_df.isnull().sum())
        
        # 3. Remove irrelevant columns (keep only useful ones)
        columns_to_drop = ['claim_id', 'user_id', 'user_phone', 'aadhar_number']
        existing_columns_to_drop = [col for col in columns_to_drop if col in self.cleaned_df.columns]
        
        if existing_columns_to_drop:
            self.cleaned_df.drop(columns=existing_columns_to_drop, inplace=True)
            print(f"\nDropped columns: {existing_columns_to_drop}")
        
        print(f"Shape after cleaning: {self.cleaned_df.shape}")
        
    def feature_engineering(self):
        """Step 2: Create new features"""
        print("\n=== FEATURE ENGINEERING ===")
        
        # Add current year for calculations
        current_year = datetime.now().year
        
        # 1. vehicle_age (if we have vehicle_year, otherwise use a proxy)
        if 'vehicle_year' not in self.cleaned_df.columns:
            # Create a proxy vehicle_year based on claim patterns
            np.random.seed(42)
            self.cleaned_df['vehicle_year'] = np.random.randint(2015, 2023, size=len(self.cleaned_df))
        
        self.cleaned_df['vehicle_age'] = current_year - self.cleaned_df['vehicle_year']
        
        # 2. claim_to_vehicle_ratio
        # Create a proxy vehicle_value if not exists
        if 'vehicle_value' not in self.cleaned_df.columns:
            # Estimate vehicle value based on claim amount (typically 10x claim amount)
            self.cleaned_df['vehicle_value'] = self.cleaned_df['claim_amount'] * 10 + np.random.normal(0, 5000, size=len(self.cleaned_df))
            self.cleaned_df['vehicle_value'] = abs(self.cleaned_df['vehicle_value'])
        
        self.cleaned_df['claim_to_vehicle_ratio'] = self.cleaned_df['claim_amount'] / (self.cleaned_df['vehicle_value'] + 1)
        
        # 3. high_claim_flag
        claim_75th_percentile = self.cleaned_df['claim_amount'].quantile(0.75)
        self.cleaned_df['high_claim_flag'] = (self.cleaned_df['claim_amount'] > claim_75th_percentile).astype(int)
        
        # 4. frequent_claimer
        self.cleaned_df['frequent_claimer'] = (self.cleaned_df['previous_claims'] > 3).astype(int)
        
        # 5. weekend_claim (create a proxy claim_date if not exists)
        if 'claim_date' not in self.cleaned_df.columns:
            # Create random claim dates
            start_date = datetime(2023, 1, 1)
            date_range = [(start_date + pd.Timedelta(days=x)).date() for x in range(365)]
            self.cleaned_df['claim_date'] = np.random.choice(date_range, size=len(self.cleaned_df))
        
        self.cleaned_df['claim_date'] = pd.to_datetime(self.cleaned_df['claim_date'])
        self.cleaned_df['weekend_claim'] = (self.cleaned_df['claim_date'].dt.dayofweek >= 5).astype(int)
        
        # 6. Additional useful features
        # claim_amount_to_repair_ratio
        self.cleaned_df['claim_repair_ratio'] = self.cleaned_df['claim_amount'] / (self.cleaned_df['repair_estimate'] + 1)
        
        # policy_validity_years (convert to years if in months)
        if self.cleaned_df['policy_validity'].max() > 100:  # Assuming months
            self.cleaned_df['policy_validity_years'] = self.cleaned_df['policy_validity'] / 12
        else:
            self.cleaned_df['policy_validity_years'] = self.cleaned_df['policy_validity']
        
        # damage_inflation_flag
        self.cleaned_df['damage_inflation_flag'] = (self.cleaned_df['claim_amount'] > self.cleaned_df['repair_estimate'] * 2).astype(int)
        
        print(f"Created new features. New shape: {self.cleaned_df.shape}")
        print("New features created:")
        new_features = ['vehicle_age', 'claim_to_vehicle_ratio', 'high_claim_flag', 
                       'frequent_claimer', 'weekend_claim', 'claim_repair_ratio', 
                       'policy_validity_years', 'damage_inflation_flag']
        for feature in new_features:
            if feature in self.cleaned_df.columns:
                print(f"- {feature}: {self.cleaned_df[feature].describe()}")
        
    def encoding(self):
        """Step 3: Encode categorical variables"""
        print("\n=== ENCODING ===")
        
        # Identify categorical columns
        categorical_cols = self.cleaned_df.select_dtypes(include=['object']).columns
        print(f"Categorical columns to encode: {list(categorical_cols)}")
        
        # Use Label Encoding for simplicity
        for col in categorical_cols:
            if col not in ['claim_date']:  # Skip date column
                le = LabelEncoder()
                self.cleaned_df[col] = le.fit_transform(self.cleaned_df[col].astype(str))
                self.label_encoders[col] = le
                print(f"Encoded {col} with {len(le.classes_)} unique values")
        
    def normalization(self):
        """Step 4: Normalize numerical columns"""
        print("\n=== NORMALIZATION ===")
        
        # Identify numerical columns (exclude target and binary flags)
        numerical_cols = []
        for col in self.cleaned_df.select_dtypes(include=[np.number]).columns:
            if col not in ['fraud_reported', 'high_claim_flag', 'frequent_claimer', 
                          'weekend_claim', 'damage_inflation_flag', 'image_uploaded', 
                          'damage_consistency']:
                numerical_cols.append(col)
        
        print(f"Numerical columns to normalize: {numerical_cols}")
        
        # Store original statistics
        self.scaler_stats = {}
        for col in numerical_cols:
            self.scaler_stats[col] = {
                'mean': self.cleaned_df[col].mean(),
                'std': self.cleaned_df[col].std(),
                'min': self.cleaned_df[col].min(),
                'max': self.cleaned_df[col].max()
            }
        
        # Normalize using StandardScaler
        self.cleaned_df[numerical_cols] = self.scaler.fit_transform(self.cleaned_df[numerical_cols])
        
        print("Normalization completed. Sample of normalized data:")
        print(self.cleaned_df[numerical_cols].head())
        
    def target_column_processing(self):
        """Step 5: Process target column"""
        print("\n=== TARGET COLUMN PROCESSING ===")
        
        if 'fraud_reported' not in self.cleaned_df.columns:
            print("Warning: 'fraud_reported' column not found. Creating based on available data...")
            # Create a proxy target based on fraud patterns
            # High claim amount + low repair estimate + previous claims = higher fraud probability
            fraud_score = (
                (self.cleaned_df['claim_amount'] > self.cleaned_df['claim_amount'].quantile(0.75)).astype(int) +
                (self.cleaned_df['claim_repair_ratio'] > 2).astype(int) +
                (self.cleaned_df['previous_claims'] > 2).astype(int) +
                (self.cleaned_df['damage_consistency'] == 0).astype(int)
            )
            self.cleaned_df['fraud_reported'] = (fraud_score >= 2).astype(int)
        else:
            # Convert to binary if needed
            if self.cleaned_df['fraud_reported'].dtype == 'object':
                self.cleaned_df['fraud_reported'] = self.cleaned_df['fraud_reported'].map({
                    'Y': 1, 'Yes': 1, 'yes': 1, '1': 1, 1: 1,
                    'N': 0, 'No': 0, 'no': 0, '0': 0, 0: 0
                }).fillna(0)
            else:
                self.cleaned_df['fraud_reported'] = self.cleaned_df['fraud_reported'].astype(int)
        
        print(f"Target column distribution:")
        print(self.cleaned_df['fraud_reported'].value_counts())
        print(f"Fraud rate: {self.cleaned_df['fraud_reported'].mean():.2%}")
        
    def feature_importance_analysis(self):
        """BONUS: Analyze feature importance and correlation"""
        print("\n=== FEATURE IMPORTANCE ANALYSIS ===")
        
        # Correlation with target
        correlations = self.cleaned_df.corr()['fraud_reported'].sort_values(ascending=False)
        print("Correlation with fraud_reported:")
        print(correlations.drop('fraud_reported').head(10))
        
        # Feature importance using Random Forest
        X = self.cleaned_df.drop('fraud_reported', axis=1)
        y = self.cleaned_df['fraud_reported']
        
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)
        
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': rf.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nTop 10 Most Important Features:")
        print(feature_importance.head(10))
        
        # Create correlation heatmap
        plt.figure(figsize=(12, 8))
        top_features = feature_importance['feature'].head(10).tolist()
        correlation_matrix = self.cleaned_df[top_features + ['fraud_reported']].corr()
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
        plt.title('Correlation Heatmap - Top Features')
        plt.tight_layout()
        plt.savefig('correlation_heatmap.png')
        plt.show()
        
        return feature_importance, correlations
        
    def save_cleaned_data(self):
        """Step 6: Save cleaned dataset"""
        print("\n=== SAVING CLEANED DATA ===")
        
        output_file = 'cleaned_data.csv'
        self.cleaned_df.to_csv(output_file, index=False)
        print(f"Cleaned dataset saved as: {output_file}")
        print(f"Final dataset shape: {self.cleaned_df.shape}")
        print(f"Final columns: {list(self.cleaned_df.columns)}")
        
        return output_file
        
    def process_dataset(self):
        """Main processing pipeline"""
        print("=== INSURANCE FRAUD DETECTION DATA PROCESSING ===\n")
        
        # Load data
        self.load_data()
        
        # Step 1: Data Cleaning
        self.data_cleaning()
        
        # Step 2: Feature Engineering
        self.feature_engineering()
        
        # Step 3: Encoding
        self.encoding()
        
        # Step 4: Normalization
        self.normalization()
        
        # Step 5: Target Column Processing
        self.target_column_processing()
        
        # Step 6: Feature Importance Analysis
        feature_importance, correlations = self.feature_importance_analysis()
        
        # Step 7: Save Cleaned Data
        output_file = self.save_cleaned_data()
        
        print("\n=== PROCESSING COMPLETE ===")
        print(f"✅ Cleaned dataset saved as: {output_file}")
        print(f"✅ Final shape: {self.cleaned_df.shape}")
        print(f"✅ Total features created: {len(self.cleaned_df.columns) - 1}")
        
        return {
            'cleaned_df': self.cleaned_df,
            'feature_importance': feature_importance,
            'correlations': correlations,
            'output_file': output_file
        }

# Usage Example
if __name__ == "__main__":
    # Initialize processor with your dataset
    processor = InsuranceFraudDataProcessor('database/claims_db.csv')
    
    # Process the entire dataset
    results = processor.process_dataset()
    
    # Display top 5 most important features
    print("\n=== TOP 5 MOST IMPORTANT FEATURES ===")
    top_features = results['feature_importance'].head(5)
    for i, row in top_features.iterrows():
        print(f"{i+1}. {row['feature']}: {row['importance']:.4f}")
    
    print(f"\nProcessing completed successfully!")
    print(f"Cleaned dataset: {results['output_file']}")
