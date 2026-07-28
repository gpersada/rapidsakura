import re

with open("extract_adk.py", "r") as f:
    content = f.read()

# Define the new functions
new_funcs = """
# --- Shared Data Loading & Join Functions ---
def load_adk_data():
    import os, pandas as pd
    data = {}
    missing = []
    for prefix in ['d_item', 'd_akun', 'd_skmpnen', 'd_soutput', 'd_cttakun', 'm_item', 'm_akun', 'm_skmpnen','m_soutput']:
        path = f"adk-joined/{prefix}.csv"
        if os.path.exists(path):
            data[prefix] = pd.read_csv(path, sep='|', dtype=str)
            if 'jumlah' in data[prefix].columns:
                data[prefix]['jumlah'] = pd.to_numeric(data[prefix]['jumlah'], errors='coerce').fillna(0)
        else:
            missing.append(prefix)
    return data, missing
    
def load_ref_data():
    import os, pandas as pd
    ref_satker = pd.DataFrame()
    ref_skmpnen = pd.DataFrame()
    ref_dirbag = pd.DataFrame()
    if os.path.exists("reference/ref_satker.xlsx"):
        ref_satker = pd.read_excel("reference/ref_satker.xlsx", dtype=str)
    if os.path.exists("reference/ref_skmpnen.xlsx"):
        ref_skmpnen = pd.read_excel("reference/ref_skmpnen.xlsx", dtype=str)
    if os.path.exists("reference/ref_dirbag.xlsx"):
        ref_dirbag = pd.read_excel("reference/ref_dirbag.xlsx", dtype=str)
        ref_dirbag.columns = ref_dirbag.columns.str.strip().str.lower()
    return ref_satker, ref_skmpnen, ref_dirbag

def build_joined_dataset(item_df, akun_df, skmpnen_df, soutput_df, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=None, source_label=None):
    import pandas as pd
    keys_soutput = ['thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput']
    common_sout = [c for c in keys_soutput if c in item_df.columns and c in soutput_df.columns]
    main_df = pd.merge(item_df, soutput_df, on=common_sout, how='left', suffixes=('', '_sout'))
    
    keys_skmpnen = keys_soutput + ['kdkmpnen', 'kdskmpnen']
    common_skmp = [c for c in keys_skmpnen if c in main_df.columns and c in skmpnen_df.columns]
    main_df = pd.merge(main_df, skmpnen_df, on=common_skmp, how='left', suffixes=('', '_skmp'))
    
    keys_akun = keys_skmpnen + ['kdakun']
    common_akun = [c for c in keys_akun if c in main_df.columns and c in akun_df.columns]
    main_df = pd.merge(main_df, akun_df, on=common_akun, how='left', suffixes=('', '_akun'))
    
    if not ref_satker.empty and 'kdsatker' in main_df.columns and 'kdsatker' in ref_satker.columns:
        main_df = pd.merge(main_df, ref_satker, on='kdsatker', how='left', suffixes=('', '_refsat'))
        
    if not ref_skmpnen.empty:
        possible_keys = ['kdskmpnen', 'kdsmpnen']
        ref_skmp_key = next((k for k in possible_keys if k in ref_skmpnen.columns), None)
        if 'kdskmpnen' in main_df.columns and ref_skmp_key:
             main_df = pd.merge(main_df, ref_skmpnen, left_on='kdskmpnen', right_on=ref_skmp_key, how='left', suffixes=('', '_refskmp'))

    if cttakun_df is not None:
        keys_cttakun = keys_akun + ['kdkmpnen', 'kdskmpnen', 'kdakun']
        common_cttakun = [c for c in keys_cttakun if c in main_df.columns and c in cttakun_df.columns]
        main_df = pd.merge(main_df, cttakun_df, on=common_cttakun, how='left', suffixes=('', '_cttakun'))

    urskmpnen_col = 'urskmpnen' if 'urskmpnen' in main_df.columns else 'urskmpnen_skmp'
    if 'urskmpnen' not in main_df.columns and urskmpnen_col in main_df.columns:
        main_df['urskmpnen'] = main_df[urskmpnen_col]
    elif 'urskmpnen' not in main_df.columns:
        main_df['urskmpnen'] = "N/A"
        
    main_df['kddirbag'] = main_df['urskmpnen'].astype(str).str.strip().str[:5].str.upper()
    if not ref_dirbag.empty and 'kddirbag' in ref_dirbag.columns:
        ref_dirbag['kddirbag'] = ref_dirbag['kddirbag'].astype(str).str.strip().str.upper()
        main_df = pd.merge(main_df, ref_dirbag, on='kddirbag', how='left', suffixes=('', '_refdirbag'))
        if 'nmdirbag' in main_df.columns:
            main_df['nmdirbag'] = main_df['nmdirbag'].fillna("N/A")
            
    ursoutput_col = 'ursoutput' if 'ursoutput' in main_df.columns else 'ursoutput_sout'
    if 'ursoutput' not in main_df.columns and ursoutput_col in main_df.columns:
        main_df['ursoutput'] = main_df[ursoutput_col]
    elif 'ursoutput' not in main_df.columns:
        main_df['ursoutput'] = "N/A"
        
    if source_label:
        if 'thang' in main_df.columns:
            idx = main_df.columns.get_loc('thang')
            main_df.insert(idx, 'source', source_label)
        else:
            main_df.insert(0, 'source', source_label)
            
    return main_df


with tab_dashboard:
    st.header("Alokasi Ditjen Perbendaharaan")
    
    adk_data, missing_files = load_adk_data()
    ref_satker, ref_skmpnen, ref_dirbag = load_ref_data()
    
    if len(missing_files) > 0:
        st.warning(f"Missing processed data for: {', '.join(missing_files)}. Please run ETL Process first.")
    else:
        d_item, d_akun, d_skmpnen, d_soutput, d_cttakun, m_item, m_akun, m_skmpnen, m_soutput = adk_data['d_item'], adk_data['d_akun'], adk_data['d_skmpnen'], adk_data['d_soutput'], adk_data['d_cttakun'], adk_data['m_item'], adk_data['m_akun'], adk_data['m_skmpnen'], adk_data['m_soutput']
        
        main_df = build_joined_dataset(d_item, d_akun, d_skmpnen, d_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=d_cttakun)
"""

# Find the start and end of the block we want to replace
start_marker = "with tab_dashboard:"
end_marker = "        # --- Filters ---"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    content = content[:start_idx] + new_funcs + "\n\n" + content[end_idx:]
    print("Dashboard tab code replaced.")
else:
    print("Failed to find start/end markers for tab_dashboard.")

# Also fix the tab_reporting part where build_joined_dataset is called
reporting_start_idx = content.find("        semula_df = build_joined_dataset(d_item")
if reporting_start_idx != -1:
    reporting_end_idx = content.find("        raw_adk_joined = pd.concat", reporting_start_idx)
    new_reporting = "        semula_df = build_joined_dataset(d_item, d_akun, d_skmpnen, d_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=d_cttakun, source_label=\"semula\")\n"
    new_reporting += "        menjadi_df = build_joined_dataset(m_item, m_akun, m_skmpnen, m_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=None, source_label=\"menjadi\")\n\n"
    content = content[:reporting_start_idx] + new_reporting + content[reporting_end_idx:]
    print("Reporting tab logic replaced.")
else:
    print("Failed to find reporting tab block.")

with open("extract_adk.py", "w") as f:
    f.write(content)

