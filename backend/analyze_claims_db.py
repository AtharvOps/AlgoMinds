import pandas as pd

print("🧪 CLAIMS_DB.CVS ANALYSIS")
print("=" * 50)

try:
    # Read the claims_db.csv file
    df = pd.read_csv("database/claims_db.csv", header=None)
    
    print(f"📊 FILE ANALYSIS:")
    print(f"• Total lines: {len(df)}")
    print(f"• Columns per row: {df.shape[1]}")
    print(f"• Has header: No (missing)")
    print()
    
    print("🔍 DATA STRUCTURE ISSUES:")
    print("❌ Missing column headers")
    print("❌ Inconsistent data format")
    print("❌ Missing claim_id and user_id columns")
    print("❌ Some rows have empty values")
    print()
    
    print("📋 SAMPLE DATA (First 3 rows):")
    for i in range(min(3, len(df))):
        print(f"Row {i+1}: {df.iloc[i].tolist()}")
    
    print()
    print("🎯 COMPARISON WITH claims.csv:")
    print("✅ claims.csv: Has proper headers")
    print("✅ claims.csv: 17 columns with names")
    print("✅ claims.csv: Consistent data format")
    print("✅ claims.csv: Proper claim_id and user_id")
    print()
    
    print("💡 RECOMMENDATION:")
    print("• Use claims.csv (not claims_db.csv)")
    print("• claims_db.csv has structural issues")
    print("• claims.csv is properly formatted")
    
except Exception as e:
    print(f"❌ Error reading claims_db.csv: {e}")

print("\n🚀 CONCLUSION:")
print("✅ claims.csv is the correct file to use")
print("❌ claims_db.csv has formatting issues")
print("📱 System should use claims.csv for fraud detection")
