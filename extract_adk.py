# ============================================================
# Project: Extract ADK SAKTI
# File: extract_adk.py
# Author: Budi Prasetyo (bprast1@gmail.com or budi.prasetyo@kemenkeu.go.id)
# Year: 2025
# 
# License: Creative Commons Attribution-NonCommercial-ShareAlike 4.0 
# International (CC BY-NC-SA 4.0)
# 
# Summary of terms:
# - You may use, modify, and share this code for non-commercial purposes.
# - You must give appropriate credit to the author.
# - If you remix, transform, or build upon this code, you must distribute 
#   your contributions under the same license (copyleft condition).
# 
# Full license text: https://creativecommons.org/licenses/by-nc-sa/4.0/
# ============================================================
import streamlit as st
import pandas as pd
import os
import re
import patoolib
import tempfile
import csv
import io
import base64
# pyrefly: ignore [missing-import]
import altair as alt

# --- D_ Header Definitions ---
D_ITEM_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput', 'kdlokasi', 
    'kdkabkota', 'kddekon', 'kdsoutput', 'kdkmpnen', 'kdskmpnen', 'kdakun', 'kdkppn', 'kdbeban', 
    'kdjnsban', 'kdctarik', 'register', 'carahitung', 'header1', 'header2', 'kdheader', 'noitem', 
    'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 
    'hargasat', 'jumlah', 'jumlah2', 'paguphln', 'pagurmp', 'pagurkp', 'kdblokir', 'blokirphln', 
    'blokirrmp', 'blokirrkp', 'rphblokir', 'kdcopy', 'kdabt', 'kdsbu', 'volsbk', 'volrkakl', 
    'blnkontrak', 'nokontrak', 'tgkontrak', 'nilkontrak', 'januari', 'pebruari', 'maret', 'april', 
    'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'nopember', 'desember', 'jmltunda', 
    'kdluncuran', 'jmlabt', 'norev', 'kdubah', 'kurs', 'indexjm', 'kdib'
]

D_AKUN_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput',
    'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'kdkmpnen', 'kdskmpnen', 'kdakun',
    'kdkppn', 'kdbeban', 'kdjnsban', 'kdctarik', 'register', 'carahitung',
    'prosenphln', 'prosenrkp', 'prosenrmp', 'kppnrkp', 'kppnrmp', 'kppnphln',
    'regdam', 'kdluncuran', 'kdblokir', 'uraiblokir', 'kdib'
]

D_SKMPNEN_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput',
    'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'kdkmpnen', 'kdskmpnen',
    'urskmpnen', 'kdib', 'kdlokus', 'reflokus', 'nmlokus', 'refrowid'
]

D_SOUTPUT_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput',
    'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'ursoutput',
    'sbmkvol', 'sbmksat', 'sbmkmin1', 'sbmkket', 'kdsb', 'volsout', 'volsbk', 'kdib'
]

D_CTTAKUN_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 
    'kdoutput', 'kdib', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'kdkmpnen', 
    'kdskmpnen', 'kdakun', 'kdkppn', 'kdbeban', 'kdjnsban', 'kdctarik', 'register',
    'carahitung', 'ket', 'ket2'
]

# --- M_ Header Definitions ---
M_ITEM_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput', 'kdlokasi', 
    'kdkabkota', 'kddekon', 'kdsoutput', 'kdkmpnen', 'kdskmpnen', 'kdakun', 'kdkppn', 'kdbeban', 
    'kdjnsban', 'kdctarik', 'register', 'carahitung', 'header1', 'header2', 'kdheader', 'noitem', 
    'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 
    'hargasat', 'jumlah', 'jumlah2', 'paguphln', 'pagurmp', 'pagurkp', 'kdblokir', 'blokirphln', 
    'blokirrmp', 'blokirrkp', 'rphblokir', 'kdcopy', 'kdabt', 'kdsbu', 'volsbk', 'volrkakl', 
    'blnkontrak', 'nokontrak', 'tgkontrak', 'nilkontrak', 'januari', 'pebruari', 'maret', 'april', 
    'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'nopember', 'desember', 'jmltunda', 
    'kdluncuran', 'jmlabt', 'norev', 'kdubah', 'kurs', 'indexjm', 'kdib'
]

M_AKUN_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput',
    'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'kdkmpnen', 'kdskmpnen', 'kdakun',
    'kdkppn', 'kdbeban', 'kdjnsban', 'kdctarik', 'register', 'carahitung',
    'prosenphln', 'prosenrkp', 'prosenrmp', 'kppnrkp', 'kppnrmp', 'kppnphln',
    'regdam', 'kdluncuran', 'kdblokir', 'uraiblokir', 'kdib'
]

M_SKMPNEN_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput',
    'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'kdkmpnen', 'kdskmpnen',
    'urskmpnen', 'kdib', 'kdlokus', 'reflokus', 'nmlokus', 'refrowid'
]

M_SOUTPUT_HEADERS = [
    'thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput',
    'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'ursoutput',
    'sbmkvol', 'sbmksat', 'sbmkmin1', 'sbmkket', 'kdsb', 'volsout', 'volsbk', 'kdib'
]


HEADERS_MAP = {
    'd_item': D_ITEM_HEADERS,
    'd_akun' : D_AKUN_HEADERS,
    'd_skmpnen': D_SKMPNEN_HEADERS,
    'd_soutput': D_SOUTPUT_HEADERS,
    'd_cttakun': D_CTTAKUN_HEADERS,
    'm_item': M_ITEM_HEADERS,
    'm_akun' : M_AKUN_HEADERS,
    'm_skmpnen': M_SKMPNEN_HEADERS,
    'm_soutput': M_SOUTPUT_HEADERS
}

TARGET_FILES = {
    'd_item': 'd_item.csv', 'd_akun': 'd_akun.csv', 'd_skmpnen': 'd_skmpnen.csv', 'd_soutput': 'd_soutput.csv', 'd_cttakun': 'd_cttakun.csv',
    'm_item': 'm_item.csv', 'm_akun': 'm_akun.csv', 'm_skmpnen': 'm_skmpnen.csv', 'm_soutput': 'm_soutput.csv'
}

UNNECESSARY_D_ITEM = [
    'kdjnsban', 'kdctarik', 'register', 'carahitung','jumlah2', 'paguphln', 'pagurmp', 'pagurkp', 
    'kdblokir', 'blokirphln', 'blokirrmp', 'blokirrkp', 'kdcopy', 'kdabt', 'kdsbu', 'volsbk', 
    'volrkakl', 'blnkontrak', 'nokontrak', 'tgkontrak', 'nilkontrak', 'januari', 'pebruari', 
    'maret', 'april', 'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'nopember', 
    'desember', 'jmltunda', 'kdluncuran', 'jmlabt', 'norev', 'kdubah', 'kurs', 'indexjm', 'kdib'
]

UNNECESSARY_M_ITEM = [
    'kdjnsban', 'kdctarik', 'register', 'carahitung','jumlah2', 'paguphln', 'pagurmp', 'pagurkp', 
    'kdblokir', 'blokirphln', 'blokirrmp', 'blokirrkp', 'kdcopy', 'kdabt', 'kdsbu', 'volsbk', 
    'volrkakl', 'blnkontrak', 'nokontrak', 'tgkontrak', 'nilkontrak', 'januari', 'pebruari', 
    'maret', 'april', 'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'nopember', 
    'desember', 'jmltunda', 'kdluncuran', 'jmlabt', 'norev', 'kdubah', 'kurs', 'indexjm', 'kdib'
]

def process_uploaded_rar(uploaded_file, temp_dir, selected_delimiter):
    """
    Extracts a .rar ADK archive, parses CSVs with user-selected delimiter,
    and cleans caret characters AFTER parsing.
    """
    st.write(f"---")
    st.write(f"**Processing file: `{uploaded_file.name}`**")
    dataframes = {}

    try:
        # Extract outer archive
        outer_extraction_dir = tempfile.mkdtemp(dir=temp_dir)
        source_path = os.path.join(temp_dir, uploaded_file.name)
        with open(source_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        patoolib.extract_archive(source_path, outdir=outer_extraction_dir, verbosity=-1)
        st.info(f"  - Successfully extracted outer archive.")

        # Find inner .sXX file
        inner_sxx_file = None
        for item in os.listdir(outer_extraction_dir):
            if re.match(r'.*\.s\d{2}$', item):
                inner_sxx_file = os.path.join(outer_extraction_dir, item)
                break
        if not inner_sxx_file:
            st.warning(f"  - No inner `.sXX` file found. Skipping.")
            return {}

        # Extract inner archive
        inner_extraction_dir = tempfile.mkdtemp(dir=temp_dir)
        patoolib.extract_archive(inner_sxx_file, outdir=inner_extraction_dir, verbosity=-1)
        st.info(f"  - Successfully extracted inner archive.")

        # Process each expected data file
        for prefix in TARGET_FILES.keys():
            for extracted_file in os.listdir(inner_extraction_dir):
                if extracted_file.startswith(prefix) and extracted_file.endswith('.csv'):
                    file_path = os.path.join(inner_extraction_dir, extracted_file)
                    if os.path.getsize(file_path) == 0:
                        st.warning(f"    - Found empty file: `{extracted_file}`. Skipping.")
                        continue

                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            raw_content = f.read()

                        # --- Optional: detect if user might have chosen wrong delimiter ---
                        sample = raw_content[:1000]
                        likely_delim = max(['|', ';', ','], key=lambda d: sample.count(d))
                        if likely_delim != selected_delimiter:
                            st.warning(f"    ⚠️ File `{extracted_file}` seems to use '{likely_delim}' delimiter (not '{selected_delimiter}'). Parsing anyway...")

                        # --- FIXED LOGIC: Parse always using '|' because ADK data is pipe-separated ---
                        df = pd.read_csv(
                            io.StringIO(raw_content),
                            delimiter='|',        # always correct for ADK files
                            header=None,
                            engine='python',
                            quoting=csv.QUOTE_NONE,
                            on_bad_lines='skip'
                        )

                        # Clean caret characters AFTER parsing
                        df = df.applymap(lambda x: str(x).replace('^', '') if isinstance(x, str) else x)

                        dataframes[prefix] = df
                        st.success(f"    - Successfully loaded `{extracted_file}` with {df.shape[1]} columns.")

                    except Exception as e:
                        st.error(f"    - Error parsing `{extracted_file}`. Check delimiter. Error: {e}")
                    break

    except Exception as e:
        st.error(f"An error occurred during processing: {e}")

    return dataframes


# --- Streamlit App UI ---
st.set_page_config(layout="wide")
st.title("RAPID - Budget Data Processing Platform")
st.subheader("Read Analyze Prepare Integrate Dashboard")

def apply_stripes(styler):
    import pandas as pd
    styler.set_properties(**{'background-color': 'rgba(128, 128, 128, 0.1)'}, subset=pd.IndexSlice[::2, :])
    return styler


tab_etl, tab_dashboard, tab_office, tab_reporting = st.tabs(["ETL Process", "BI Dashboard", "Office Allocation", "Reporting & Matriks"])

with tab_etl:
    st.markdown("""
    This tool as a part of ETL process to prepare ADK data for BI tools (like Tableau, Looker Studio).  
    Steps:
    1. **Extracts & parses** data using your chosen delimiter.  
    2. **Cleans** all caret (`^`) characters after parsing.
    """)

    delimiter = st.selectbox(
        '1. Select the delimiter to use on the CLEANED data',
        ('|', ',', ';'),
        index=0,
        help="Choose the field separator used inside the extracted CSV data."
    )

    st.session_state.setdefault('master_data', {prefix: pd.DataFrame() for prefix in TARGET_FILES.keys()})

    uploaded_files = st.file_uploader(
        "2. Choose your .rar files", type=['rar'], accept_multiple_files=True
    )

    if st.button("Process Uploaded Files", disabled=(not uploaded_files)):
        st.session_state.master_data = {prefix: pd.DataFrame() for prefix in TARGET_FILES.keys()}
        with tempfile.TemporaryDirectory() as temp_dir:
            progress_bar = st.progress(0)
            for i, uploaded_file in enumerate(uploaded_files):
                extracted_data = process_uploaded_rar(uploaded_file, temp_dir, delimiter)
                for prefix, df in extracted_data.items():
                    if not df.empty:
                        st.session_state.master_data[prefix] = pd.concat(
                            [st.session_state.master_data[prefix], df],
                            ignore_index=True
                        )
                progress_bar.progress((i + 1) / len(uploaded_files))
        
        # Apply headers, drop columns, and save to adk-joined
        join_dir = "adk-joined"
        if not os.path.exists(join_dir):
            os.makedirs(join_dir)

        for prefix in TARGET_FILES.keys():
            master_df = st.session_state.master_data.get(prefix, pd.DataFrame())
            if not master_df.empty:
                cleaned_df = master_df.copy()
                if prefix in HEADERS_MAP:
                    headers = HEADERS_MAP[prefix]
                    num_cols_to_keep = min(len(headers), cleaned_df.shape[1])
                    cleaned_df = cleaned_df.iloc[:, :num_cols_to_keep]
                    cleaned_df.columns = headers[:num_cols_to_keep]
                else:
                    cleaned_df.columns = [f'Column_{j+1}' for j in range(cleaned_df.shape[1])]
                
                # Drop unnecessary columns for d_item
                if prefix == 'd_item':
                    cols_to_drop = [c for c in UNNECESSARY_D_ITEM if c in cleaned_df.columns]
                    cleaned_df.drop(columns=cols_to_drop, inplace=True, errors='ignore')
                
                # Convert amounts safely
                if 'jumlah' in cleaned_df.columns:
                    cleaned_df['jumlah'] = pd.to_numeric(cleaned_df['jumlah'], errors='coerce').fillna(0)

                st.session_state.master_data[prefix] = cleaned_df
                
                # Save as CSV
                output_path = os.path.join(join_dir, f"{prefix}.csv")
                cleaned_df.to_csv(output_path, index=False, sep='|')
                st.success(f"Saved {prefix} to {output_path}")

        st.write("---")
        st.header("✅ Processing Complete!")

    # --- Consolidated Data Display ---
    st.header("Consolidated & Cleaned Data Summary")

    if any(not df.empty for df in st.session_state.master_data.values()):
        cols = st.columns(len(TARGET_FILES))
        for i, (prefix, output_name) in enumerate(TARGET_FILES.items()):
            master_df = st.session_state.master_data.get(prefix, pd.DataFrame())
            with cols[i]:
                st.subheader(output_name)
                if not master_df.empty:
                    st.metric(label="Total Rows", value=f"{len(master_df):,}")
                    st.dataframe(master_df.head(5).style.pipe(apply_stripes))
                    
                    csv_output = master_df.to_csv(index=False, sep=delimiter, quoting=csv.QUOTE_MINIMAL).encode('utf-8')
                    st.download_button(
                       f"📥 Download {output_name}",
                       csv_output,
                       file_name=output_name,
                       mime='text/csv',
                       key=f"download_{prefix}"
                    )
                else:
                    st.warning("No data found for this file type.")
    else:
        st.info("No data has been processed yet.")



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


        # --- Filters ---
        st.subheader("Filter Data")
        row1_c1, row1_c2, row1_c3 = st.columns(3)
        with row1_c1:
            opts_thang = ['All'] + sorted(main_df['thang'].dropna().unique().tolist()) if 'thang' in main_df.columns else ['All']
            sel_thang = st.selectbox("Tahun (thang)", opts_thang)
        with row1_c2:
            opts_beban = ['All'] + sorted(main_df['kdbeban'].dropna().unique().tolist()) if 'kdbeban' in main_df.columns else ['All']
            sel_beban = st.selectbox("Kode Beban (kdbeban)", opts_beban)
        with row1_c3:
            if 'kdsatker' in main_df.columns:
                if 'nmsatker' in main_df.columns:
                    satker_pairs = main_df[['kdsatker', 'nmsatker']].dropna(subset=['kdsatker']).drop_duplicates()
                    satker_pairs['nmsatker'] = satker_pairs['nmsatker'].fillna("N/A")
                    opts_satker = ['All'] + sorted([f"{row['kdsatker']} - {row['nmsatker']}" for idx, row in satker_pairs.iterrows()])
                else:
                    opts_satker = ['All'] + sorted(main_df['kdsatker'].dropna().unique().tolist())
            else:
                opts_satker = ['All']
            sel_satker = st.selectbox("Kode Satker (kdsatker)", opts_satker)
            
        k_sat = sel_satker.split(" - ")[0] if sel_satker != 'All' else ''
        
        row2_c1, row2_c2, row2_c3 = st.columns(3)
        with row2_c1:
            if 'kdskmpnen' in main_df.columns:
                skmp_pairs = main_df[['kdskmpnen', 'urskmpnen']].dropna().drop_duplicates()
                skmp_list = ['All'] + [f"{row['kdskmpnen']} - {row['urskmpnen']}" for idx, row in skmp_pairs.iterrows()]
            else:
                skmp_list = ['All']
            sel_skmpnen = st.selectbox("Subkomponen", skmp_list)
            
        with row2_c2:
            sel_dirbag = 'All'
            if k_sat == '527010' and 'kddirbag' in main_df.columns:
                mask = (main_df['kdsatker'] == '527010') & (main_df['kddirbag'].astype(str).str.startswith('PB.'))
                if 'nmdirbag' in main_df.columns:
                    dirbag_pairs = main_df[mask][['kddirbag', 'nmdirbag']].dropna(subset=['kddirbag']).drop_duplicates()
                    dirbag_pairs['nmdirbag'] = dirbag_pairs['nmdirbag'].fillna("N/A")
                    opts_dirbag = ['All'] + sorted([f"{row['kddirbag']} - {row['nmdirbag']}" for idx, row in dirbag_pairs.iterrows()])
                else:
                    opts_dirbag = ['All'] + sorted(main_df[mask]['kddirbag'].dropna().unique().tolist())
                sel_dirbag = st.selectbox("Direktorat/Bagian", opts_dirbag)
                
        with row2_c3:
            if all(c in main_df.columns for c in ['kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput']):
                ro_pairs = main_df[['kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput']].dropna().drop_duplicates()
                ro_list = ['All'] + sorted([f"{row['kdprogram']}.{row['kdgiat']}.{row['kdoutput']}.{row['kdsoutput']} - {row['ursoutput']}" for idx, row in ro_pairs.iterrows()])
            else:
                ro_list = ['All']
            sel_ro = st.selectbox("Rincian Output", ro_list)
            
        # Apply filters
        f_df = main_df.copy()
        if sel_thang != 'All': f_df = f_df[f_df['thang'] == sel_thang]
        if sel_beban != 'All': f_df = f_df[f_df['kdbeban'] == sel_beban]
        if k_sat != '': f_df = f_df[f_df['kdsatker'] == k_sat]
        if sel_skmpnen != 'All':
            k_val = sel_skmpnen.split(" - ")[0]
            f_df = f_df[f_df['kdskmpnen'] == k_val]
        if sel_dirbag != 'All':
            k_dir = sel_dirbag.split(" - ")[0]
            f_df = f_df[f_df['kddirbag'] == k_dir]
        if sel_ro != 'All':
            k_ro_parts = sel_ro.split(" - ")[0].split(".")
            if len(k_ro_parts) == 4:
                k_prog, k_giat, k_out, k_sout = k_ro_parts
                f_df = f_df[(f_df['kdprogram'] == k_prog) & 
                            (f_df['kdgiat'] == k_giat) & 
                            (f_df['kdoutput'] == k_out) & 
                            (f_df['kdsoutput'] == k_sout)]

        # Ensure amounts are properly aggregated
        if 'jumlah' in f_df.columns:
            f_df['jumlah'] = pd.to_numeric(f_df['jumlah'], errors='coerce').fillna(0)

        st.write("---")
        
        # --- Metrics ---
        st.subheader("Summary Metrics")
        m1, m2, m3 = st.columns(3)
        
        if 'jumlah' in f_df.columns:
            pagu_total = f_df['jumlah'].sum()
            
            pagu_op = 0
            pagu_non_op = 0
            if 'kdkmpnen' in f_df.columns:
                pagu_op = f_df[f_df['kdkmpnen'].isin(['001', '002'])]['jumlah'].sum()
                pagu_non_op = f_df[f_df['kdkmpnen'].isin(['005', '100'])]['jumlah'].sum()
                
            with m1:
                st.metric("Pagu Total", f"{pagu_total:,.0f}".replace(",", "."))
            with m2:
                st.metric("Pagu Belanja Operasional", f"{pagu_op:,.0f}".replace(",", "."))
            with m3:
                st.metric("Pagu Belanja Nonoperasional", f"{pagu_non_op:,.0f}".replace(",", "."))
                
        st.write("---")
        
        # --- Charts ---
        if f_df.empty:
            st.warning("No data based on the current filters.")
        else:
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("**Pagu per Rincian Output**")
                if all(c in f_df.columns for c in ['kdprogram', 'kdgiat','kdoutput', 'kdsoutput','ursoutput']):
                    out_df = f_df.groupby(['kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput','ursoutput'])['jumlah'].sum().reset_index()
                    st.dataframe(
                        out_df.style.format(thousands=".", precision=0).pipe(apply_stripes),
                        column_config={
                            "kdprogram": st.column_config.Column(width="15px"),
                            "kdgiat": st.column_config.Column(width="15px"),
                            "kdoutput": st.column_config.Column(width="15px"),
                            "kdsoutput": st.column_config.Column(width="15px"),
                            "ursoutput": st.column_config.Column(width="large"),
                            "jumlah": st.column_config.Column(width="small"),
                        }
                        # use_container_width=True
                        )
                else:
                    st.error("Missing columns for Rincian Output.")
                    
                st.markdown("**Pagu per BKPK**")
                if 'kdakun' in f_df.columns:
                    f_df['BKPK'] = f_df['kdakun'].astype(str).str[:4]
                    akun_df = f_df.groupby('BKPK')['jumlah'].sum().reset_index()
                    # sort by descending
                    akun_df = akun_df.sort_values(by='BKPK', ascending=False)
                    # st.bar_chart(akun_df, x='BKPK', y='jumlah', tooltip=["BKPK", alt.Tooltip("jumlah", format=",.0f")]).interactive()
                    chart = alt.Chart(akun_df).mark_bar().encode(
                        x='BKPK', 
                        y='jumlah', 
                        tooltip=["BKPK", alt.Tooltip("jumlah", format=",.0f")]
                    ).interactive()
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.error("Missing kdakun column.")

            with c2:
                st.markdown("**Pagu per Kode Kegiatan**")
                if 'kdgiat' in f_df.columns:
                    giat_df = f_df.groupby('kdgiat')['jumlah'].sum().reset_index()
                    st.dataframe(
                        giat_df.style.format(thousands=".", precision=0).pipe(apply_stripes), 
                        use_container_width=True
                        )
                else:
                    st.error("Missing kdgiat column.")
                    
                st.markdown("**Pagu per Komponen**")
                if 'kdkmpnen' in f_df.columns:
                    kmp_df = f_df.groupby('kdkmpnen')['jumlah'].sum().reset_index()
                    st.dataframe(
                        kmp_df.style.format(thousands=".", precision=0).pipe(apply_stripes), 
                        use_container_width=True
                    )
                else:
                    st.error("Missing kdkmpnen column.")
                    
                st.markdown("**Pagu per Subkomponen**")
                if all(c in f_df.columns for c in ['kdskmpnen','urskmpnen']):
                    skmp_df = f_df.groupby(['kdskmpnen','urskmpnen'])['jumlah'].sum().reset_index()
                    st.dataframe(
                        skmp_df.style.format(thousands=".", precision=0).pipe(apply_stripes), 
                        use_container_width=True
                        )
                else:
                    st.error("Missing kdskmpnen or urskmpnen column.")

with tab_office:
    st.header("Office Allocation Dashboard")
    
    if 'main_df' not in locals() or main_df.empty:
        st.warning("Please run ETL Process and wait for data to load.")
    else:
        if 'nmsatker' not in main_df.columns:
            st.error("Column 'nmsatker' not found. Ensure ref_satker.xlsx is loaded correctly.")
        else:
            # Filter Data (matching both literal request and actual abbreviations found in the data)
            df_kanwil = main_df[main_df['nmsatker'].str.contains('^Kantor Wilayah|^KANWIL', case=False, na=False)]
            df_kppn = main_df[main_df['nmsatker'].str.contains('^Kantor Pelayanan Perbendaharaan Negara|^KPPN', case=False, na=False)]
            
            def display_office_table(df_subset, title):
                st.subheader(title)
                if df_subset.empty:
                    st.info(f"No data available for {title}.")
                    return
                
                # Pre-calculate office data for statistics and table
                office_df = df_subset.groupby(['kdsatker', 'nmsatker'])['jumlah'].sum().reset_index()
                office_df = office_df.rename(columns={'kdsatker': 'Kode Satker', 'nmsatker': 'Nama Satker', 'jumlah': 'Jumlah Pagu'})
                office_df = office_df.sort_values(by='Jumlah Pagu', ascending=False)
                
                # Statistics
                if not office_df.empty:
                    st.markdown("**Statistik Jumlah Pagu**")
                    min_idx = office_df['Jumlah Pagu'].idxmin()
                    max_idx = office_df['Jumlah Pagu'].idxmax()
                    
                    min_val = office_df.loc[min_idx, 'Jumlah Pagu']
                    min_name = office_df.loc[min_idx, 'Nama Satker']
                    
                    max_val = office_df.loc[max_idx, 'Jumlah Pagu']
                    max_name = office_df.loc[max_idx, 'Nama Satker']
                    
                    mean_val = office_df['Jumlah Pagu'].mean()
                    q25 = office_df['Jumlah Pagu'].quantile(0.25)
                    q50 = office_df['Jumlah Pagu'].quantile(0.50)
                    q75 = office_df['Jumlah Pagu'].quantile(0.75)

                    val_counts = office_df['Jumlah Pagu'].value_counts()
                    if not val_counts.empty and val_counts.iloc[0] > 1:
                        mode_val = val_counts.index[0]
                        mode_str = f"{mode_val:,.0f}".replace(',', '.')
                    else:
                        mode_str = "N/A"
                    
                    c1, c2, c3, c4 = st.columns(4)
                    with c1:
                        st.metric("Minimum", f"{min_val:,.0f}".replace(',', '.'), help=min_name)
                    with c2:
                        st.metric("Maximum", f"{max_val:,.0f}".replace(',', '.'), help=max_name)
                    with c3:
                        st.metric("Mean (Rata-rata)", f"{mean_val:,.0f}".replace(',', '.'))
                    with c4:
                        st.metric("Mode (Terbanyak)", mode_str)
                        
                    c4, c5, c6, c7 = st.columns(4)
                    with c4:
                        st.metric("Percentile 25%", f"{q25:,.0f}".replace(',', '.'))
                    with c5:
                        st.metric("Median (50%)", f"{q50:,.0f}".replace(',', '.'))
                    with c6:
                        st.metric("Percentile 75%", f"{q75:,.0f}".replace(',', '.'))
                    with c7:
                        st.metric("Pagu Total", f"{office_df['Jumlah Pagu'].sum():,.0f}".replace(',', '.'))
                        
                    st.write("---")

                # Regional summary (nmlokasi)
                if 'nmlokasi' in df_subset.columns:
                    loc_df = df_subset.groupby('nmlokasi')['jumlah'].sum().reset_index()
                    loc_df = loc_df.rename(columns={'nmlokasi': 'Wilayah', 'jumlah': 'Jumlah Pagu'})
                    loc_df = loc_df.sort_values(by='Jumlah Pagu', ascending=False)
                    st.markdown("**Alokasi per Wilayah**")
                    st.dataframe(loc_df.style.format({'Jumlah Pagu': '{:,.0f}'}).pipe(apply_stripes), use_container_width=True)
                
                # Office Table
                st.markdown("**Alokasi per Kantor**")
                st.dataframe(office_df.style.format({'Jumlah Pagu': '{:,.0f}'}).pipe(apply_stripes), use_container_width=True)
                
                st.write("---")

            # Display sections
            display_office_table(df_kanwil, "Kantor Wilayah")
            display_office_table(df_kppn, "Kantor Pelayanan Perbendaharaan Negara")

with tab_reporting:
    st.header("Reporting & Matriks")

    if 'adk_data' not in locals() or 'ref_satker' not in locals():
        adk_data, missing_files = load_adk_data()
        ref_satker, ref_skmpnen, ref_dirbag = load_ref_data()
    else:
        missing_files = [] if adk_data else ['All']
    
    if len(missing_files) > 0:
        st.warning(f"Missing processed data for: {', '.join(missing_files)}. Please run ETL Process first.")
    else:
        d_item, d_akun, d_skmpnen, d_soutput, d_cttakun = adk_data['d_item'], adk_data['d_akun'], adk_data['d_skmpnen'], adk_data['d_soutput'], adk_data['d_cttakun']
        m_item, m_akun, m_skmpnen, m_soutput = adk_data['m_item'], adk_data['m_akun'], adk_data['m_skmpnen'], adk_data['m_soutput']
        
        # Build datasets - Menjadi from d_ and semula from m_
        menjadi_df = build_joined_dataset(d_item, d_akun, d_skmpnen, d_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=d_cttakun, source_label="menjadi")
        semula_df = build_joined_dataset(m_item, m_akun, m_skmpnen, m_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=None, source_label="semula")

        def assign_new_cols(df):
            if 'kdkmpnen' in df.columns:
                df['ops/nonops'] = df['kdkmpnen'].apply(lambda x: 'Operasional' if str(x).strip() in ['001', '002'] else 'Nonoperasional')
            else:
                df['ops/nonops'] = 'Nonoperasional'
                
            def get_satdirbag(row):
                urs = str(row.get('urskmpnen', ''))
                nmsatker = row.get('nmsatker', '')
                if urs.startswith('PB.'):
                    prefix = urs[:5]
                    mapping = {
                        'PB.11': 'PB.11 Bagian Organisasi dan Tata Laksana',
                        'PB.12': 'PB.12 Bagian Sumber Daya Manusia',
                        'PB.13': 'PB.13 Bagian Keuangan',
                        'PB.14': 'PB.14 Bagian Umum',
                        'PB.15': 'PB.15 Bagian Kepatuhan Internal',
                        'PB.16': 'PB.16 Bagian Komunikasi, Layanan Informasi, dan Kerja Sama Kelembagaan',
                        'PB.20': 'PB.20 Direktorat Pelaksanaan Anggaran',
                        'PB.30': 'PB.30 Direktorat Pengelolaan Kas Negara',
                        'PB.40': 'PB.40 Direktorat Sistem Manajemen Investasi',
                        'PB.50': 'PB.50 Direktorat Pembinaan Pengelolaan Keuangan Badan Layanan Umum',
                        'PB.60': 'PB.60 Direktorat Akuntansi dan Pelaporan Keuangan',
                        'PB.70': 'PB.70 Direktorat Sistem Perbendaharaan',
                        'PB.80': 'PB.80 Direktorat Sistem Informasi dan Teknologi Perbendaharaan',
                        'PB.TP': 'PB.TP Tenaga Pengkaji Bidang Perbendaharaan'
                    }
                    return mapping.get(prefix, nmsatker)
                return nmsatker
                
            df['satdirbag'] = df.apply(get_satdirbag, axis=1)
            return df
            
        menjadi_df = assign_new_cols(menjadi_df)
        semula_df = assign_new_cols(semula_df)


        d_cols = ['source', 'thang', 'kdjendok', 'kdsatker', 'nmsatker', 'satdirbag', 'kddept', 'kdunit', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput', 'kdkmpnen', 'kdskmpnen', 'urskmpnen', 'ops/nonops', 'kdakun', 'header1', 'header2', 'kdheader', 'noitem', 'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 'hargasat', 'volsout', 'jumlah', 'ket','ket2']
        m_cols = ['source', 'thang', 'kdjendok', 'kdsatker', 'nmsatker', 'satdirbag', 'kddept', 'kdunit', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput', 'kdkmpnen', 'kdskmpnen', 'urskmpnen', 'ops/nonops', 'kdakun', 'header1', 'header2', 'kdheader', 'noitem', 'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 'hargasat', 'volsout', 'jumlah']

        # Filter the columns strictly as requested
        d_cols_available = [c for c in d_cols if c in menjadi_df.columns]
        m_cols_available = [c for c in m_cols if c in semula_df.columns]
        
        raw_menjadi = menjadi_df[d_cols_available].copy()
        raw_semula = semula_df[m_cols_available].copy()

        raw_adk_joined = pd.concat([raw_semula, raw_menjadi], ignore_index=True)
        if 'jumlah' in raw_adk_joined.columns:
            raw_adk_joined['jumlah'] = pd.to_numeric(raw_adk_joined['jumlah'], errors='coerce').fillna(0)
            
        st.subheader("Raw Data ADK Joined")
        st.dataframe(pd.concat([raw_adk_joined.head(), raw_adk_joined.tail()]))
        
        # Export Raw Data to Excel (using BytesIO)
        @st.cache_data
        def convert_df_to_excel(df):
            output = io.BytesIO()
            # Removed engine='xlsxwriter' to let pandas fallback to default (openpyxl)
            with pd.ExcelWriter(output) as writer:
                df.to_excel(writer, index=False, sheet_name='Raw_ADK')
            return output.getvalue()
        
        st.write("---")
        st.subheader("Matriks Semula Menjadi")
        
        # Prepare components for Matriks grouping by kdsatker
        matriks_data = []
        
        # Group grouped components
        if not ref_satker.empty:
            all_satker = raw_adk_joined['kdsatker'].dropna().unique()
            satker_dict = dict(zip(ref_satker['kdsatker'], ref_satker['nmsatker']))
        else:
            all_satker = []
            satker_dict = {}

        for satker in all_satker:
            nmsatker = satker_dict.get(satker, "N/A")
            
            # Subsets for satker
            semula_s = semula_df[semula_df['kdsatker'] == satker]
            menjadi_s = menjadi_df[menjadi_df['kdsatker'] == satker]
            
            def safe_num(df_sub):
                if 'jumlah' in df_sub.columns:
                    return pd.to_numeric(df_sub['jumlah'], errors='coerce').fillna(0).sum()
                return 0
                
            # PPKNR (CD)
            semula_ppknr = semula_s[(semula_s['kdprogram'] == 'CD') & (semula_s['kdakun'].astype(str).str.startswith('52'))]
            menjadi_ppknr = menjadi_s[(menjadi_s['kdprogram'] == 'CD') & (menjadi_s['kdakun'].astype(str).str.startswith('52'))]
            val_ppknr_semula = safe_num(semula_ppknr)
            val_ppknr_menjadi = safe_num(menjadi_ppknr)
            val_ppknr_selisih = val_ppknr_menjadi - val_ppknr_semula
            
            # WA Pegawai
            semula_wa_peg = semula_s[(semula_s['kdprogram'] == 'WA') & (semula_s['kdkmpnen'] == '001') & (semula_s['kdakun'].astype(str).str.startswith('51'))]
            menjadi_wa_peg = menjadi_s[(menjadi_s['kdprogram'] == 'WA') & (menjadi_s['kdkmpnen'] == '001') & (menjadi_s['kdakun'].astype(str).str.startswith('51'))]
            val_wa_peg_semula = safe_num(semula_wa_peg)
            val_wa_peg_menjadi = safe_num(menjadi_wa_peg)
            val_wa_peg_selisih = val_wa_peg_menjadi - val_wa_peg_semula
            
            # WA Barang Ops
            semula_wa_ops = semula_s[(semula_s['kdprogram'] == 'WA') & (semula_s['kdkmpnen'] == '002') & (semula_s['kdakun'].astype(str).str.startswith('52'))]
            menjadi_wa_ops = menjadi_s[(menjadi_s['kdprogram'] == 'WA') & (menjadi_s['kdkmpnen'] == '002') & (menjadi_s['kdakun'].astype(str).str.startswith('52'))]
            val_wa_ops_semula = safe_num(semula_wa_ops)
            val_wa_ops_menjadi = safe_num(menjadi_wa_ops)
            val_wa_ops_selisih = val_wa_ops_menjadi - val_wa_ops_semula

            # WA Barang NonOps
            semula_wa_nops = semula_s[(semula_s['kdprogram'] == 'WA') & (semula_s['kdkmpnen'].isin(['100', '005'])) & (semula_s['kdakun'].astype(str).str.startswith('52'))]
            menjadi_wa_nops = menjadi_s[(menjadi_s['kdprogram'] == 'WA') & (menjadi_s['kdkmpnen'].isin(['100', '005'])) & (menjadi_s['kdakun'].astype(str).str.startswith('52'))]
            val_wa_nops_semula = safe_num(semula_wa_nops)
            val_wa_nops_menjadi = safe_num(menjadi_wa_nops)
            val_wa_nops_selisih = val_wa_nops_menjadi - val_wa_nops_semula
            
            # WA Modal
            semula_wa_mod = semula_s[(semula_s['kdprogram'] == 'WA') & (semula_s['kdkmpnen'] == '100') & (semula_s['kdakun'].astype(str).str.startswith('53'))]
            menjadi_wa_mod = menjadi_s[(menjadi_s['kdprogram'] == 'WA') & (menjadi_s['kdkmpnen'] == '100') & (menjadi_s['kdakun'].astype(str).str.startswith('53'))]
            val_wa_mod_semula = safe_num(semula_wa_mod)
            val_wa_mod_menjadi = safe_num(menjadi_wa_mod)
            val_wa_mod_selisih = val_wa_mod_menjadi - val_wa_mod_semula
            
            # WA Total
            val_wa_tot_semula = val_wa_peg_semula + val_wa_ops_semula + val_wa_nops_semula + val_wa_mod_semula
            val_wa_tot_menjadi = val_wa_peg_menjadi + val_wa_ops_menjadi + val_wa_nops_menjadi + val_wa_mod_menjadi
            val_wa_tot_selisih = val_wa_peg_selisih + val_wa_ops_selisih + val_wa_nops_selisih + val_wa_mod_selisih
            
            # Total DIPA
            val_tot_semula = safe_num(semula_s)
            val_tot_menjadi = safe_num(menjadi_s)
            val_tot_selisih = val_tot_menjadi - val_tot_semula
            
            row = {
                'KODE SATKER': satker,
                'NAMA SATKER': nmsatker,
                'PPKNR - BELANJA BARANG NONOPERASIONAL - SEMULA': val_ppknr_semula,
                'PPKNR - BELANJA BARANG NONOPERASIONAL - MENJADI': val_ppknr_menjadi,
                'PPKNR - SELISIH BELANJA BARANG NONOPERASIONAL': val_ppknr_selisih,
                'WA - BELANJA PEGAWAI - SEMULA': val_wa_peg_semula,
                'WA - BELANJA PEGAWAI - MENJADI': val_wa_peg_menjadi,
                'WA - SELISIH BELANJA PEGAWAI': val_wa_peg_selisih,
                'WA - BELANJA BARANG OPERASIONAL - SEMULA': val_wa_ops_semula,
                'WA - BELANJA BARANG OPERASIONAL - MENJADI': val_wa_ops_menjadi,
                'WA - SELISIH BELANJA BARANG OPERASIONAL': val_wa_ops_selisih,
                'WA - BELANJA BARANG NONOPERASIONAL - SEMULA': val_wa_nops_semula,
                'WA - BELANJA BARANG NONOPERASIONAL - MENJADI': val_wa_nops_menjadi,
                'WA - SELISIH BELANJA BARANG NONOPERASIONAL': val_wa_nops_selisih,
                'WA - BELANJA MODAL - SEMULA': val_wa_mod_semula,
                'WA - BELANJA MODAL - MENJADI': val_wa_mod_menjadi,
                'WA - SELISIH BELANJA MODAL': val_wa_mod_selisih,
                'WA - TOTAL DUKUNGAN MANAJEMEN - SEMULA': val_wa_tot_semula,
                'WA - TOTAL DUKUNGAN MANAJEMEN - MENJADI': val_wa_tot_menjadi,
                'WA - SELISIH TOTAL DUKUNGAN MANAJEMEN': val_wa_tot_selisih,
                'TOTAL DIPA - SEMULA': val_tot_semula,
                'TOTAL DIPA - MENJADI': val_tot_menjadi,
                'TOTAL DIPA - SELISIH': val_tot_selisih,
            }
            matriks_data.append(row)
            
        matriks_df = pd.DataFrame(matriks_data)
        
        # Append Grand Total Row
        if not matriks_df.empty:
            sums = matriks_df.drop(columns=['KODE SATKER', 'NAMA SATKER']).sum()
            grand_total_row = {'KODE SATKER': 'TOTAL', 'NAMA SATKER': ''}
            grand_total_row.update(sums.to_dict())
            matriks_df = pd.concat([matriks_df, pd.DataFrame([grand_total_row])], ignore_index=True)
            
        st.dataframe(matriks_df.style.format(precision=0, thousands=".").pipe(apply_stripes))
        
        # Export Matriks to Excel
        # Create 2 columns for the side-by-side buttons
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.download_button(
                label="📥 Download Matriks Report (Excel)",
                data=convert_df_to_excel(matriks_df),
                file_name='matriks_semula_menjadi.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        with col2:
            st.download_button(
                label="📥 Download Raw Data ADK Joined (Excel)",
                data=convert_df_to_excel(raw_adk_joined),
                file_name='raw_adk_joined.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

# --- Sticky footer (copyleft notice) ---

# Load copyleft image from local 'images' directory
with open("images/64px-Copyleft.svg.png", "rb") as f:
    img_data = f.read()
img_base64 = base64.b64encode(img_data).decode()

# --- Copyleft footer with image and dark gradient ---
st.markdown(f"""
    <style>
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background: linear-gradient(90deg, rgba(25,25,25,0.95), rgba(45,45,45,0.95));
            color: #e0e0e0;
            text-align: center;
            padding: 8px 0;
            font-size: 0.9rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            backdrop-filter: blur(6px);
            z-index: 100;
            letter-spacing: 0.2px;
        }}
        .footer img {{
            height: 18px;
            vertical-align: middle;
            margin-right: 6px;
            filter: brightness(1.2);
        }}
        .footer b {{
            color: #ffffff;
        }}
        .footer a {{
            color: #00b4d8;
            text-decoration: none;
            font-weight: 500;
        }}
        .footer a:hover {{
            color: #90e0ef;
            text-decoration: underline;
        }}
    </style>

    <div class="footer">
        <em>Copyleft</em>  
        <img src="data:image/png;base64,{img_base64}">
        <b>Extract ADK SAKTI</b> 2025<br>
        Licensed under 
        <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank">
        CC BY-NC-SA 4.0 International</a>
    </div>
""", unsafe_allow_html=True)
