import re

with open("extract_adk.py", "r") as f:
    content = f.read()

# 1. New assign_new_cols function to be inserted right after menjadi_df and semula_df are defined
assignment_code = """
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
                        'PB.11': 'Bagian Organisasi dan Tata Laksana',
                        'PB.12': 'Bagian Sumber Daya Manusia',
                        'PB.13': 'Bagian Keuangan',
                        'PB.14': 'Bagian Umum',
                        'PB.15': 'Bagian Kepatuhan Internal',
                        'PB.16': 'Bagian Komunikasi, Layanan Informasi, dan Kerja Sama Kelembagaan',
                        'PB.20': 'Direktorat Pelaksanaan Anggaran',
                        'PB.30': 'Direktorat Pengelolaan Kas Negara',
                        'PB.40': 'Direktorat Sistem Manajemen Investasi',
                        'PB.50': 'Direktorat Pembinaan Pengelolaan Keuangan Badan Layanan Umum',
                        'PB.60': 'Direktorat Akuntansi dan Pelaporan Keuangan',
                        'PB.70': 'Direktorat Sistem Perbendaharaan',
                        'PB.80': 'Direktorat Sistem Informasi dan Teknologi Perbendaharaan',
                        'PB.TP': 'Tenaga Pengkaji Bidang Perbendaharaan'
                    }
                    return mapping.get(prefix, nmsatker)
                return nmsatker
                
            df['satdirbag'] = df.apply(get_satdirbag, axis=1)
            return df
            
        menjadi_df = assign_new_cols(menjadi_df)
        semula_df = assign_new_cols(semula_df)
"""

old_datasets = """        # Build datasets
        menjadi_df = build_joined_dataset(d_item, d_akun, d_skmpnen, d_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=d_cttakun, source_label="menjadi")
        semula_df = build_joined_dataset(m_item, m_akun, m_skmpnen, m_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=None, source_label="semula")"""

if old_datasets in content:
    content = content.replace(old_datasets, old_datasets + "\n" + assignment_code)

old_d_cols = "d_cols = ['source', 'thang', 'kdjendok', 'kdsatker', 'nmsatker','kddept', 'kdunit', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput', 'kdkmpnen', 'kdskmpnen', 'urskmpnen', 'kdakun', 'header1', 'header2', 'kdheader', 'noitem', 'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 'hargasat', 'volsout', 'jumlah', 'ket']"
old_m_cols = "m_cols = ['source', 'thang', 'kdjendok', 'kdsatker', 'nmsatker', 'kddept', 'kdunit', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput', 'kdkmpnen', 'kdskmpnen', 'urskmpnen', 'kdakun', 'header1', 'header2', 'kdheader', 'noitem', 'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 'hargasat', 'volsout', 'jumlah']"

new_d_cols = "d_cols = ['source', 'thang', 'kdjendok', 'kdsatker', 'nmsatker', 'satdirbag', 'kddept', 'kdunit', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput', 'kdkmpnen', 'kdskmpnen', 'urskmpnen', 'ops/nonops', 'kdakun', 'header1', 'header2', 'kdheader', 'noitem', 'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 'hargasat', 'volsout', 'jumlah', 'ket']"
new_m_cols = "m_cols = ['source', 'thang', 'kdjendok', 'kdsatker', 'nmsatker', 'satdirbag', 'kddept', 'kdunit', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput', 'kdkmpnen', 'kdskmpnen', 'urskmpnen', 'ops/nonops', 'kdakun', 'header1', 'header2', 'kdheader', 'noitem', 'nmitem', 'vol1', 'sat1', 'vol2', 'sat2', 'vol3', 'sat3', 'vol4', 'sat4', 'volkeg', 'satkeg', 'hargasat', 'volsout', 'jumlah']"

content = content.replace(old_d_cols, new_d_cols)
content = content.replace(old_m_cols, new_m_cols)

with open("extract_adk.py", "w") as f:
    f.write(content)

print("Reporting patched!")

