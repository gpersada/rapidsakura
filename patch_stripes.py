import re

with open('extract_adk.py', 'r') as f:
    content = f.read()

# 1. Insert apply_stripes after st.subheader("Read Analyze...")
helper = """
def apply_stripes(styler):
    import pandas as pd
    styler.set_properties(**{'background-color': 'rgba(128, 128, 128, 0.1)'}, subset=pd.IndexSlice[::2, :])
    return styler
"""
if "def apply_stripes(styler):" not in content:
    content = content.replace('st.subheader("Read Analyze Prepare Integrate Dashboard")', 
                              'st.subheader("Read Analyze Prepare Integrate Dashboard")\n' + helper)

# 2. Patch .style.format(...) to append .pipe(apply_stripes)
# Be careful not to replace it if it's already there
content = re.sub(r'\.style\.format\((.*?)\)(?!\.pipe\(apply_stripes\))', r'.style.format(\1).pipe(apply_stripes)', content)

# 3. Patch specific plain dataframes
content = content.replace('st.dataframe(master_df.head(5))', 'st.dataframe(master_df.head(5).style.pipe(apply_stripes))')
content = content.replace('st.dataframe(raw_adk_joined.head())', 'st.dataframe(raw_adk_joined.head().style.pipe(apply_stripes))')

with open('extract_adk.py', 'w') as f:
    f.write(content)

print("Patch applied")
