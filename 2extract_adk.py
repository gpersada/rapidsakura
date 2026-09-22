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
import shutil
import subprocess
from datetime import datetime, timezone, timedelta
import requests
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
    'desember', 'jmltunda', 'kdluncuran', 'jmlabt', 'norev', 'kdubah', 'kurs', 'indexjm'
    # 'kdib' sengaja TIDAK di-drop: kolom ini dipakai sebagai merge key di
    # build_joined_dataset() (lihat keys_soutput) karena d_soutput/d_skmpnen/
    # d_akun bisa punya beberapa baris dengan key lain yang sama tapi kdib
    # berbeda. Kalau di-drop dari d_item, item akan fan-out (match ke semua
    # baris kdib sekaligus) dan menginflasi total jumlah di Summary Metrics.
]

UNNECESSARY_M_ITEM = [
    'kdjnsban', 'kdctarik', 'register', 'carahitung','jumlah2', 'paguphln', 'pagurmp', 'pagurkp', 
    'kdblokir', 'blokirphln', 'blokirrmp', 'blokirrkp', 'kdcopy', 'kdabt', 'kdsbu', 'volsbk', 
    'volrkakl', 'blnkontrak', 'nokontrak', 'tgkontrak', 'nilkontrak', 'januari', 'pebruari', 
    'maret', 'april', 'mei', 'juni', 'juli', 'agustus', 'september', 'oktober', 'nopember', 
    'desember', 'jmltunda', 'kdluncuran', 'jmlabt', 'norev', 'kdubah', 'kurs', 'indexjm', 'kdib'
]

def _extract_with_fallback(file_path, outdir, debug=False):
    """
    Extract an archive, forcing the format by extension if patoolib's
    content-based detection isn't available (e.g. no 'file'/libmagic on
    the host, as can happen on Streamlit Cloud). ADK files are RAR
    archives renamed with non-standard extensions (.sXX, no extension,
    etc.), so we try a plain extract first, then retry after renaming
    a copy with each common archive extension until one works.
    Finally falls back to the 'unar' CLI tool directly, which auto-
    detects format from content and supports RAR5 (unlike unrar-free).
    """
    errors = []

    try:
        patoolib.extract_archive(file_path, outdir=outdir, verbosity=-1)
        return True
    except Exception as e:
        errors.append(f"direct patoolib: {e}")

    for ext in ['.rar', '.zip', '.7z', '.tar', '.tar.gz']:
        renamed_path = file_path + ext
        try:
            shutil.copy(file_path, renamed_path)
            patoolib.extract_archive(renamed_path, outdir=outdir, verbosity=-1)
            return True
        except Exception as e:
            errors.append(f"patoolib as {ext}: {e}")
            continue
        finally:
            if os.path.exists(renamed_path):
                os.remove(renamed_path)

    # Fallback: try unrar directly with stdout captured (unrar often writes
    # its real error - e.g. wrong/missing password - to stdout, not stderr,
    # which patoolib's exception message doesn't surface).
    try:
        result = subprocess.run(
            ["unrar", "x", "-kb", "-or", "-p-", file_path, outdir + os.sep],
            capture_output=True, text=True, timeout=120, encoding='utf-8', errors='replace'
        )
        if result.returncode == 0:
            return True
        errors.append(f"unrar direct (stdout): {result.stdout.strip()}")
        errors.append(f"unrar direct (stderr): {result.stderr.strip()}")
    except FileNotFoundError:
        errors.append("unrar: command not found")
    except Exception as e:
        errors.append(f"unrar direct: {e}")

    # Fallback: call 'unar' directly. It auto-detects the archive format
    # from content (not extension) and supports RAR5, which unrar-free
    # does not. Treat as success even on partial failure (nonzero exit)
    # if at least some files were actually extracted - a few corrupted
    # entries inside the archive shouldn't discard everything else.
    try:
        result = subprocess.run(
            ["unar", "-f", "-o", outdir, file_path],
            capture_output=True, text=True, timeout=120, encoding='utf-8', errors='replace'
        )
        extracted_any = any(
            os.path.getsize(os.path.join(root, f)) > 0
            for root, _dirs, files in os.walk(outdir)
            for f in files
        )
        if result.returncode == 0:
            return True
        if extracted_any:
            errors.append(f"unar: partial extraction (some entries corrupted in source archive): {result.stdout.strip()[-500:]}")
            if debug:
                st.caption("    - unar: partial extraction succeeded (some entries were corrupted in the source archive and skipped):")
                st.caption(f"      {result.stdout.strip()[-500:]}")
            return True
        errors.append(f"unar (stdout): {result.stdout.strip()}")
        errors.append(f"unar (stderr): {result.stderr.strip()}")
    except FileNotFoundError:
        errors.append("unar: command not found (package not installed)")
    except Exception as e:
        errors.append(f"unar: {e}")

    if debug:
        st.caption("    Extraction attempts failed:")
        for err in errors:
            st.caption(f"    - {err}")

    return False


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
        if not _extract_with_fallback(source_path, outer_extraction_dir, debug=True):
            st.error("  - Could not extract outer archive (unrecognized format).")
            return {}
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
        if not _extract_with_fallback(inner_sxx_file, inner_extraction_dir, debug=True):
            st.error("  - Could not extract inner `.sXX` archive (unrecognized format).")
            return {}
        st.info(f"  - Successfully extracted inner archive.")

        # --- Recursively peel any further nested archives ---
        # ADK exports sometimes wrap the actual D_*/M_* CSVs inside one more
        # archive layer with no recognizable extension (e.g. 'd01_...').
        def _is_target_csv(filename):
            low = filename.lower()
            return any(low.startswith(p) for p in TARGET_FILES.keys()) and low.endswith('.csv')

        max_depth = 4
        for depth in range(max_depth):
            all_files = []
            for root, _dirs, files in os.walk(inner_extraction_dir):
                for fname in files:
                    all_files.append(os.path.join(root, fname))

            if any(_is_target_csv(os.path.basename(fp)) for fp in all_files):
                break

            extracted_something = False
            for fp in all_files:
                if _is_target_csv(os.path.basename(fp)):
                    continue
                nested_out = tempfile.mkdtemp(dir=inner_extraction_dir)
                if _extract_with_fallback(fp, nested_out):
                    extracted_something = True

            if not extracted_something:
                break  # nothing more to peel

        # Final inventory across the whole tree (all nesting levels)
        all_files_final = []
        for root, _dirs, files in os.walk(inner_extraction_dir):
            for fname in files:
                all_files_final.append(os.path.join(root, fname))

        st.caption(f"  - Files found after full extraction: {[os.path.basename(f) for f in all_files_final]}")

        # Process each expected data file
        for prefix in TARGET_FILES.keys():
            for file_path in all_files_final:
                extracted_file = os.path.basename(file_path)
                if extracted_file.lower().startswith(prefix.lower()) and extracted_file.lower().endswith('.csv'):
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
                        df = df.apply(lambda col: col.map(lambda x: str(x).replace('^', '') if isinstance(x, str) else x))

                        dataframes[prefix] = df
                        st.success(f"    - Successfully loaded `{extracted_file}` with {df.shape[1]} columns.")

                    except Exception as e:
                        st.error(f"    - Error parsing `{extracted_file}`. Check delimiter. Error: {e}")
                    break

    except Exception as e:
        st.error(f"An error occurred during processing: {e}")

    return dataframes


# --- History Management (constants + active-history label helpers,
# defined early so the "active data" caption right under the page header
# can use them) ---
HISTORY_DIR = "history"
MASTER_DIR = "adk-joined"
MANIFEST_PATH = os.path.join(HISTORY_DIR, "manifest.csv")
ACTIVE_HISTORY_FILE = os.path.join(MASTER_DIR, "active_history.txt")

# Server (Streamlit Cloud) runs in UTC; semua timestamp yang ditampilkan/
# disimpan (history_id, waktu_posting, dsb.) memakai WIB (GMT+7) agar sesuai
# waktu lokal, bukan waktu server.
WIB = timezone(timedelta(hours=7))


def now_wib():
    return datetime.now(WIB)


def _read_active_history_label():
    """Reads the persisted label of the history currently active as master
    (adk-joined/), if any has been posted/loaded before."""
    if os.path.exists(ACTIVE_HISTORY_FILE):
        try:
            with open(ACTIVE_HISTORY_FILE, "r", encoding="utf-8") as f:
                label = f.read().strip()
                return label or None
        except Exception:
            return None
    return None


def _write_active_history_label(label):
    """Persists (locally) the label of the history now active as master."""
    os.makedirs(MASTER_DIR, exist_ok=True)
    with open(ACTIVE_HISTORY_FILE, "w", encoding="utf-8") as f:
        f.write(label)


# --- Streamlit App UI ---
st.set_page_config(layout="wide")
st.title("RAPID - Budget Data Processing Platform")
st.subheader("Read Analyze Prepare Integrate Dashboard")

st.session_state.setdefault(
    'active_history_label',
    _read_active_history_label() or "Belum ada data master yang diposting"
)
st.session_state.setdefault('has_unposted_data', False)


def render_active_data_banner():
    """Renders the 'Data aktif saat ini' caption + unposted-data warning.

    Called once at the top of the page (so it's visible on every tab), and
    again immediately after any action that changes active_history_label /
    has_unposted_data (upload+process, Post ke Master, Load History ke
    Master) - so the notification appears right away in the same run,
    instead of only on the next rerun.
    """
    st.caption(f"📌 Data aktif saat ini: **{st.session_state.active_history_label}**")
    if st.session_state.has_unposted_data:
        st.warning("⚠️ Ada data ADK baru yang sudah dimuat & dipakai di semua tab, namun **belum di-Post ke Master** — belum permanen/tersimpan ke GitHub. Kalau app di-redeploy sebelum di-Post, data ini akan hilang. Post di tab **ETL Process** untuk menyimpannya.")


render_active_data_banner()

def apply_stripes(styler):
    import pandas as pd
    styler.set_properties(**{'background-color': 'rgba(128, 128, 128, 0.1)'}, subset=pd.IndexSlice[::2, :])
    return styler


tab_etl, tab_dashboard, tab_office, tab_reporting = st.tabs(["ETL Process", "BI Dashboard", "Office Allocation", "Reporting & Matriks"])


def _github_config():
    """Reads GitHub repo config + token from Streamlit secrets (Settings > Secrets)."""
    try:
        gh = st.secrets["github"]
        token = gh["token"]
        repo = gh["repo"]
        branch = gh.get("branch", "main")
        return token, repo, branch
    except Exception:
        return None, None, None


def commit_to_github(commit_message, files_to_write=None, files_to_delete=None):
    """
    Atomically writes and/or deletes files in the GitHub repo in a single
    commit, using the Git Data API (blob -> tree -> commit -> update ref),
    so changes survive Streamlit Cloud redeploys (which re-clone the repo).

    files_to_write maps repo-relative path -> text content (blobs are
    created and upserted into the tree). files_to_delete is a list of
    repo-relative paths to remove from the tree (their blob sha is set to
    None, which is how the Git Data API deletes a path).

    Returns (success: bool, message: str) - message is the new commit sha
    on success, or an error description on failure.
    """
    files_to_write = files_to_write or {}
    files_to_delete = files_to_delete or []

    token, repo, branch = _github_config()
    if not token:
        return False, "GitHub token belum dikonfigurasi di Secrets (Settings > Secrets)."

    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}
    base_url = f"https://api.github.com/repos/{repo}"

    try:
        ref_resp = requests.get(f"{base_url}/git/ref/heads/{branch}", headers=headers, timeout=30)
        ref_resp.raise_for_status()
        latest_commit_sha = ref_resp.json()["object"]["sha"]

        commit_resp = requests.get(f"{base_url}/git/commits/{latest_commit_sha}", headers=headers, timeout=30)
        commit_resp.raise_for_status()
        base_tree_sha = commit_resp.json()["tree"]["sha"]

        # Only ask the Git Data API to delete paths that actually exist in
        # the remote tree. Requesting sha=None for a path that was never
        # successfully pushed (e.g. an earlier commit failed with 401/403)
        # makes /git/trees return 422, since it can't resolve a delete
        # inside a subtree that doesn't exist remotely.
        if files_to_delete:
            remote_tree_resp = requests.get(
                f"{base_url}/git/trees/{base_tree_sha}", headers=headers,
                params={"recursive": "1"}, timeout=30,
            )
            remote_tree_resp.raise_for_status()
            remote_paths = {
                item["path"] for item in remote_tree_resp.json().get("tree", [])
                if item.get("type") == "blob"
            }
            files_to_delete = [
                p.replace(os.sep, "/") for p in files_to_delete
                if p.replace(os.sep, "/") in remote_paths
            ]

        tree_items = []
        for path, content in files_to_write.items():
            blob_resp = requests.post(
                f"{base_url}/git/blobs", headers=headers,
                json={"content": content, "encoding": "utf-8"}, timeout=30,
            )
            blob_resp.raise_for_status()
            tree_items.append({
                "path": path.replace(os.sep, "/"),
                "mode": "100644",
                "type": "blob",
                "sha": blob_resp.json()["sha"],
            })

        for path in files_to_delete:
            # Setting sha to None tells the Git Data API to remove this
            # path from the resulting tree.
            tree_items.append({
                "path": path.replace(os.sep, "/"),
                "mode": "100644",
                "type": "blob",
                "sha": None,
            })

        if not tree_items:
            return True, latest_commit_sha  # nothing to commit

        tree_resp = requests.post(
            f"{base_url}/git/trees", headers=headers,
            json={"base_tree": base_tree_sha, "tree": tree_items}, timeout=30,
        )
        tree_resp.raise_for_status()
        new_tree_sha = tree_resp.json()["sha"]

        new_commit_resp = requests.post(
            f"{base_url}/git/commits", headers=headers,
            json={"message": commit_message, "tree": new_tree_sha, "parents": [latest_commit_sha]}, timeout=30,
        )
        new_commit_resp.raise_for_status()
        new_commit_sha = new_commit_resp.json()["sha"]

        update_ref_resp = requests.patch(
            f"{base_url}/git/refs/heads/{branch}", headers=headers,
            json={"sha": new_commit_sha}, timeout=30,
        )
        update_ref_resp.raise_for_status()

        return True, new_commit_sha

    except requests.exceptions.RequestException as e:
        return False, str(e)


def commit_files_to_github(files_dict, commit_message):
    """Backward-compatible wrapper around commit_to_github (write-only)."""
    return commit_to_github(commit_message, files_to_write=files_dict)



def load_history_manifest():
    """Returns the history manifest as a DataFrame (empty if none exists yet)."""
    if os.path.exists(MANIFEST_PATH):
        manifest_df = pd.read_csv(MANIFEST_PATH, sep='|', dtype=str)
        # Backward-compat: older manifest.csv files predate the
        # source_filenames column - add it (empty) so downstream code can
        # always rely on it being present.
        if 'source_filenames' not in manifest_df.columns:
            manifest_df['source_filenames'] = ''
        return manifest_df
    return pd.DataFrame(columns=['history_id', 'nama_history', 'catatan_history', 'waktu_posting', 'source_filenames'])


def post_to_master(master_data_dict, nama_history, catatan_history, source_filenames=""):
    """
    Archives the currently processed data under history/{history_id}/,
    writes it to adk-joined/ (the active master read by all other tabs),
    and commits both to GitHub (if configured) so it survives redeploys.
    source_filenames: display string (e.g. comma-separated) of the ADK
    file names that were uploaded & processed to produce this data,
    recorded in the manifest so it can be shown in "Load Data History".
    Returns (history_id, github_ok, github_msg).
    """
    timestamp = now_wib().strftime('%Y%m%d_%H%M%S')
    safe_name = re.sub(r'[^A-Za-z0-9_-]+', '_', nama_history.strip()) or 'history'
    history_id = f"{timestamp}_{safe_name}"

    hist_folder = os.path.join(HISTORY_DIR, history_id)
    os.makedirs(hist_folder, exist_ok=True)
    os.makedirs(MASTER_DIR, exist_ok=True)

    files_to_commit = {}

    for prefix, df in master_data_dict.items():
        if df is not None and not df.empty:
            csv_text = df.to_csv(sep='|', index=False)
            hist_path = os.path.join(hist_folder, f"{prefix}.csv")
            master_path = os.path.join(MASTER_DIR, f"{prefix}.csv")
            with open(hist_path, "w", encoding="utf-8") as f:
                f.write(csv_text)
            with open(master_path, "w", encoding="utf-8") as f:
                f.write(csv_text)
            files_to_commit[hist_path] = csv_text
            files_to_commit[master_path] = csv_text

    manifest = load_history_manifest()
    new_row = pd.DataFrame([{
        'history_id': history_id,
        'nama_history': nama_history.strip(),
        'catatan_history': catatan_history.strip(),
        'waktu_posting': now_wib().strftime('%Y-%m-%d %H:%M:%S'),
        'source_filenames': source_filenames.strip() if isinstance(source_filenames, str) else source_filenames,
    }])
    manifest = pd.concat([manifest, new_row], ignore_index=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)
    manifest_text = manifest.to_csv(sep='|', index=False)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(manifest_text)
    files_to_commit[MANIFEST_PATH] = manifest_text

    # Mark this history as the active one shown across all tabs.
    active_label = nama_history.strip()
    _write_active_history_label(active_label)
    files_to_commit[ACTIVE_HISTORY_FILE] = active_label

    github_ok, github_msg = commit_files_to_github(
        files_to_commit,
        commit_message=f"Post history: {nama_history.strip()} ({history_id})"
    )

    return history_id, github_ok, github_msg


def load_history_to_master(history_id):
    """
    Copies a history entry's files into adk-joined/ (making it the active
    master), persists + commits the active-history label, and returns the
    loaded dataframes.
    Returns (loaded: dict, active_label: str, github_ok: bool, github_msg: str).
    """
    hist_folder = os.path.join(HISTORY_DIR, history_id)
    os.makedirs(MASTER_DIR, exist_ok=True)
    loaded = {}
    files_to_commit = {}
    for prefix in TARGET_FILES.keys():
        src = os.path.join(hist_folder, f"{prefix}.csv")
        if os.path.exists(src):
            dst = os.path.join(MASTER_DIR, f"{prefix}.csv")
            shutil.copy(src, dst)
            with open(src, "r", encoding="utf-8") as f:
                files_to_commit[dst] = f.read()
            loaded[prefix] = pd.read_csv(src, sep='|', dtype=str)
            if 'jumlah' in loaded[prefix].columns:
                loaded[prefix]['jumlah'] = pd.to_numeric(loaded[prefix]['jumlah'], errors='coerce').fillna(0)

    manifest = load_history_manifest()
    match = manifest.loc[manifest['history_id'].astype(str) == str(history_id), 'nama_history']
    active_label = match.iloc[0] if not match.empty else history_id
    _write_active_history_label(active_label)
    files_to_commit[ACTIVE_HISTORY_FILE] = active_label

    github_ok, github_msg = commit_to_github(
        commit_message=f"Load history to master: {history_id}",
        files_to_write=files_to_commit,
    )

    return loaded, active_label, github_ok, github_msg


def delete_history(history_id):
    """
    Hard-deletes a posted history entry:
      - removes its row from history/manifest.csv,
      - deletes its local folder history/{history_id}/,
      - deletes its files from the GitHub repo (permanent, not recoverable
        from GitHub history/reflog via the UI).

    Does NOT touch adk-joined/ (the active master data). If this history
    happens to be the one currently active as master, adk-joined/ is left
    untouched - post a new history or load a different one to change it.

    Returns (ok: bool, github_ok: bool, msg: str).
    """
    manifest = load_history_manifest()
    if history_id not in manifest['history_id'].astype(str).values:
        return False, False, f"History '{history_id}' tidak ditemukan di manifest."

    hist_folder = os.path.join(HISTORY_DIR, history_id)

    # Collect repo-relative paths of files to delete from GitHub.
    paths_to_delete = []
    if os.path.isdir(hist_folder):
        for fname in os.listdir(hist_folder):
            paths_to_delete.append(os.path.join(hist_folder, fname))

    # Rewrite the manifest without this history_id.
    manifest = manifest[manifest['history_id'].astype(str) != str(history_id)]
    os.makedirs(HISTORY_DIR, exist_ok=True)
    manifest_text = manifest.to_csv(sep='|', index=False)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write(manifest_text)

    # Remove the local history folder.
    if os.path.isdir(hist_folder):
        shutil.rmtree(hist_folder)

    # Push the deletion + updated manifest to GitHub as a single commit.
    github_ok, github_msg = commit_to_github(
        commit_message=f"Hard delete history: {history_id}",
        files_to_write={MANIFEST_PATH: manifest_text},
        files_to_delete=paths_to_delete,
    )

    return True, github_ok, github_msg


with tab_etl:
    st.markdown("""
    This tool as a part of ETL process to prepare ADK data for BI tools (like Tableau, Looker Studio).  
    Steps:
    1. **Extracts & parses** data using your chosen delimiter.  
    2. **Cleans** all caret (`^`) characters after parsing.
    """)

    # --- Opsi: Load dari History ---
    with st.expander("📂 Atau: Load Data dari History yang Sudah Diposting"):
        manifest_df = load_history_manifest()
        if manifest_df.empty:
            st.info("Belum ada history yang diposting.")
        else:
            st.dataframe(
                manifest_df[['nama_history', 'catatan_history', 'source_filenames', 'waktu_posting']].rename(columns={
                    'nama_history': 'Nama History',
                    'catatan_history': 'Catatan',
                    'source_filenames': 'Nama File Sumber',
                    'waktu_posting': 'Waktu Posting',
                }).iloc[::-1],
                use_container_width=True
            )
            hist_options = [
                f"{row['nama_history']} | {row['history_id']} | {row['waktu_posting']}"
                for _, row in manifest_df.iloc[::-1].iterrows()
            ]
            sel_hist = st.selectbox("Pilih History untuk di-Load", hist_options)
            if st.button("🔄 Load History ke Master"):
                chosen_id = sel_hist.split(" | ")[1]
                with st.spinner("Meload history & mengirim ke GitHub..."):
                    loaded, active_label, github_ok, github_msg = load_history_to_master(chosen_id)
                st.session_state.master_data = {
                    prefix: loaded.get(prefix, pd.DataFrame()) for prefix in TARGET_FILES.keys()
                }
                st.session_state.active_history_label = active_label
                st.session_state.has_unposted_data = False
                st.success(f"History '{chosen_id}' berhasil di-load ke Master. Tab lain (BI Dashboard, dsb.) sekarang menggunakan data ini.")
                if github_ok:
                    st.success(f"✅ Tersimpan permanen ke GitHub (commit `{github_msg[:7]}`).")
                else:
                    st.warning(f"⚠️ Termuat lokal, tapi GAGAL push ke GitHub: {github_msg}\n\nStatus ini **tidak akan bertahan** setelah app di-redeploy sampai push berhasil.")
                render_active_data_banner()

            st.write("---")
            st.markdown("**🗑️ Hard Delete History**")
            st.caption(
                "Menghapus history secara PERMANEN dari lokal & GitHub (tidak bisa dibatalkan). "
                "Data master aktif (`adk-joined/`) tidak ikut terhapus/berubah oleh aksi ini."
            )
            confirm_delete = st.checkbox(
                f"Saya yakin ingin menghapus history `{sel_hist.split(' | ')[1]}` secara permanen",
                key="confirm_delete_history"
            )
            if st.button("🗑️ Hard Delete History Terpilih", disabled=not confirm_delete):
                chosen_id_del = sel_hist.split(" | ")[1]
                with st.spinner("Menghapus history & mengirim ke GitHub..."):
                    ok, github_ok, msg = delete_history(chosen_id_del)
                if ok:
                    st.success(f"History '{chosen_id_del}' dihapus dari manifest & folder lokal.")
                    if github_ok:
                        st.success(f"✅ Berhasil dihapus permanen dari GitHub (commit `{msg[:7]}`). App akan otomatis redeploy dalam ~1 menit.")
                    else:
                        st.warning(f"⚠️ Terhapus lokal, tapi GAGAL dihapus di GitHub: {msg}\n\nFile ini akan **muncul kembali** setelah app di-redeploy sampai penghapusan berhasil di-push.")
                else:
                    st.error(msg)

    st.write("---")

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
        # Remember which ADK files were uploaded for this processing run, so
        # it can be recorded in history when/if the user Posts ke Master.
        st.session_state.uploaded_filenames = [f.name for f in uploaded_files]
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
        
        # Apply headers and clean columns (staged in session_state only -
        # not written to adk-joined/ yet; use "Post ke Master" below to
        # commit this as the active master data).
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

        # --- Fallback: derive missing M_* data from its D_* counterpart ---
        # If an M_ file wasn't present in the uploaded ADK, use the D_ file
        # instead (M_ and D_ share identical column schemas for item/akun/
        # skmpnen/soutput), but zero out pagu (jumlah) and volume (volsout)
        # since those M_-specific "semula" values weren't actually provided.
        FALLBACK_M_FROM_D = {
            'm_item': 'd_item',
            'm_akun': 'd_akun',
            'm_skmpnen': 'd_skmpnen',
            'm_soutput': 'd_soutput',
        }
        for m_prefix, d_prefix in FALLBACK_M_FROM_D.items():
            m_df = st.session_state.master_data.get(m_prefix, pd.DataFrame())
            d_df = st.session_state.master_data.get(d_prefix, pd.DataFrame())
            if m_df.empty and not d_df.empty:
                fallback_df = d_df.copy()
                if 'jumlah' in fallback_df.columns:
                    fallback_df['jumlah'] = 0
                if 'volsout' in fallback_df.columns:
                    fallback_df['volsout'] = 0
                st.session_state.master_data[m_prefix] = fallback_df
                st.info(
                    f"ℹ️ `{m_prefix}` tidak ditemukan di file upload — menggunakan data "
                    f"`{d_prefix}` sebagai fallback, dengan pagu/volume (jumlah/volsout) = 0."
                )

        # Mark this as unposted data actively in use for the current
        # session (all other tabs read from st.session_state.master_data
        # first - see load_adk_data() - so it's already live without
        # needing "Post ke Master"). Only flag it if something was
        # actually extracted, so a failed/empty upload doesn't overwrite
        # a perfectly good existing active-data label.
        if any(not df.empty for df in st.session_state.master_data.values()):
            st.session_state.active_history_label = (
                f"🆕 Data ADK baru hasil upload — diproses {now_wib().strftime('%Y-%m-%d %H:%M:%S')}"
            )
            st.session_state.has_unposted_data = True

        st.write("---")
        st.header("✅ Processing Complete!")
        # Show the active-data / belum-di-post notification right away in
        # this same run, instead of waiting for the next rerun.
        render_active_data_banner()

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

        st.write("---")
        st.subheader("📤 Post ke Master")
        st.caption("Data di atas sudah langsung dipakai tab BI Dashboard, Office Allocation, dan Reporting & Matriks di sesi ini. Post ke Master bersifat opsional: gunakan untuk memberi nama & catatan history, serta menyimpannya secara permanen ke GitHub agar bertahan setelah app di-redeploy / dipakai sesi lain.")
        nama_history = st.text_input("Nama History (Format YYYY-KodeHistorySAKTI, misal 2026-B00)", key="nama_history_input")
        catatan_history = st.text_area("Catatan History", key="catatan_history_input")
        if st.button("📤 Post ke Master", type="primary"):
            if not nama_history.strip():
                st.error("Nama History wajib diisi.")
            else:
                with st.spinner("Menyimpan & mengirim ke GitHub..."):
                    history_id, github_ok, github_msg = post_to_master(
                        st.session_state.master_data,
                        nama_history,
                        catatan_history,
                        source_filenames=", ".join(st.session_state.get('uploaded_filenames', [])),
                    )
                st.session_state.active_history_label = nama_history.strip()
                st.session_state.has_unposted_data = False
                st.success(f"Berhasil diposting ke Master dengan ID history: `{history_id}`")
                if github_ok:
                    st.success(f"✅ Tersimpan permanen ke GitHub (commit `{github_msg[:7]}`). App akan otomatis redeploy dalam ~1 menit.")
                else:
                    st.warning(f"⚠️ Data tersimpan lokal, tapi GAGAL push ke GitHub: {github_msg}\n\nHistory ini **tidak akan bertahan** setelah app di-redeploy sampai push berhasil.")
                # Reflect the new active-data label immediately (label is
                # now the just-posted history's name; no more "belum di
                # post" warning since has_unposted_data is now False).
                render_active_data_banner()
    else:
        st.info("No data has been processed yet.")



# --- Shared Data Loading & Join Functions ---
def load_adk_data():
    """
    Loads data for all tabs, preferring the ADK just processed in the
    current session (st.session_state.master_data - staged there right
    after "Process Uploaded Files", before any "Post ke Master") over the
    persisted master in adk-joined/. This lets a freshly uploaded ADK show
    up immediately in BI Dashboard / Office Allocation / Reporting &
    Matriks, without requiring a Post first. Falls back to adk-joined/ for
    any prefix not (yet) processed in this session - e.g. right after
    opening the app, or for prefixes untouched by the latest upload.
    """
    import os, pandas as pd
    data = {}
    missing = []
    session_master = st.session_state.get('master_data', {})
    for prefix in ['d_item', 'd_akun', 'd_skmpnen', 'd_soutput', 'd_cttakun', 'm_item', 'm_akun', 'm_skmpnen','m_soutput']:
        session_df = session_master.get(prefix)
        if session_df is not None and not session_df.empty:
            df = session_df.copy()
            if 'jumlah' in df.columns:
                df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce').fillna(0)
            data[prefix] = df
            continue
        path = os.path.join(MASTER_DIR, f"{prefix}.csv")
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
    keys_soutput = ['thang', 'kdjendok', 'kdsatker', 'kddept', 'kdunit', 'kdprogram', 'kdgiat', 'kdoutput', 'kdlokasi', 'kdkabkota', 'kddekon', 'kdsoutput', 'kdib']
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


def assign_new_cols(df):
    """Adds 'ops/nonops' (from kdkmpnen) and 'satdirbag' (from urskmpnen /
    nmsatker) columns. Shared by the BI Dashboard and Reporting & Matriks
    tabs so both use the same categorization logic."""
    if 'kdkmpnen' in df.columns:
        df['ops/nonops'] = df['kdkmpnen'].apply(lambda x: 'Operasional' if str(x).strip() in ['001', '002'] else 'Nonoperasional')
    else:
        df['ops/nonops'] = 'Nonoperasional'

    def get_satdirbag(row):
        urs = str(row.get('urskmpnen', '')).strip().upper()
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
            # If it starts with PB. but doesn't match a known code, still
            # flag it explicitly rather than silently falling back to the
            # satker name (which looks like a legitimate value).
            return mapping.get(prefix, f"{nmsatker} (Belum Tertandai - {prefix})")
        return f"{nmsatker} (Belum Tertandai)"

    df['satdirbag'] = df.apply(get_satdirbag, axis=1)
    return df


def load_history_d_files(history_id):
    """Loads the d_item/d_akun/d_skmpnen/d_soutput/d_cttakun files of a
    posted history entry directly from history/{history_id}/, for use as
    an alternate "ADK Semula" source in the BI Dashboard tab (instead of
    the m_* files bundled with the currently active ADK).
    Returns (data: dict[prefix, DataFrame], missing: list[str])."""
    hist_folder = os.path.join(HISTORY_DIR, history_id)
    prefixes = ['d_item', 'd_akun', 'd_skmpnen', 'd_soutput', 'd_cttakun']
    data = {}
    missing = []
    for prefix in prefixes:
        path = os.path.join(hist_folder, f"{prefix}.csv")
        if os.path.exists(path):
            df = pd.read_csv(path, sep='|', dtype=str)
            if 'jumlah' in df.columns:
                df['jumlah'] = pd.to_numeric(df['jumlah'], errors='coerce').fillna(0)
            data[prefix] = df
        else:
            data[prefix] = pd.DataFrame()
            missing.append(prefix)
    return data, missing


with tab_dashboard:
    st.header("Alokasi Ditjen Perbendaharaan")
    
    adk_data, missing_files = load_adk_data()
    ref_satker, ref_skmpnen, ref_dirbag = load_ref_data()
    
    if len(missing_files) > 0:
        st.warning(f"Missing processed data for: {', '.join(missing_files)}. Please run ETL Process first.")
    else:
        d_item, d_akun, d_skmpnen, d_soutput, d_cttakun, m_item, m_akun, m_skmpnen, m_soutput = adk_data['d_item'], adk_data['d_akun'], adk_data['d_skmpnen'], adk_data['d_soutput'], adk_data['d_cttakun'], adk_data['m_item'], adk_data['m_akun'], adk_data['m_skmpnen'], adk_data['m_soutput']
        
        main_df = build_joined_dataset(d_item, d_akun, d_skmpnen, d_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=d_cttakun, source_label="menjadi")
        main_df = assign_new_cols(main_df)

        # --- Sumber ADK Semula ---
        # Default: "ADK Terkini" - m_* files bundled with the currently
        # active ADK (existing behavior). Alternative: a posted history's
        # d_* files, restricted to histories whose nama_history shares the
        # same 4-char tahun (thang) prefix as the active ADK - a given ADK
        # always has exactly one thang value, so this is an exact match,
        # not a multi-year lookup.
        st.subheader("Sumber ADK Semula")
        active_thang = (
            str(d_item['thang'].dropna().iloc[0])
            if 'thang' in d_item.columns and not d_item['thang'].dropna().empty
            else None
        )
        semula_source_mode = st.radio(
            "Pilih sumber data Pagu/Volume Semula",
            options=["ADK Terkini", "History (d_file)"],
            horizontal=True,
            key="semula_source_mode"
        )

        selected_history_id = None
        if semula_source_mode == "History (d_file)":
            manifest_df = load_history_manifest()
            if active_thang is None or manifest_df.empty:
                st.info("Tidak ada history yang tersedia untuk dijadikan ADK Semula.")
            else:
                matching_hist = manifest_df[manifest_df['nama_history'].astype(str).str[:4] == active_thang]
                if matching_hist.empty:
                    st.info(f"Tidak ada history dengan tahun {active_thang} yang bisa dipakai sebagai ADK Semula.")
                else:
                    hist_options = matching_hist.apply(
                        lambda r: f"{r['nama_history']} | {r['history_id']} | {r['waktu_posting']}", axis=1
                    ).tolist()
                    sel_hist_label = st.selectbox("Pilih History sebagai ADK Semula", hist_options, key="semula_source_history")
                    selected_history_id = sel_hist_label.split(" | ")[1]

        # Semula (pre-revision) dataset, built for the Semula/Menjadi
        # comparison table shown below the filters, sourced according to
        # the selector above.
        if semula_source_mode == "History (d_file)" and selected_history_id:
            hist_data, hist_missing = load_history_d_files(selected_history_id)
            if hist_missing:
                st.warning(f"File tidak lengkap pada history terpilih: {', '.join(hist_missing)}. Menggunakan ADK Terkini sebagai fallback.")
                semula_dash_df = build_joined_dataset(m_item, m_akun, m_skmpnen, m_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=None, source_label="semula")
            else:
                semula_dash_df = build_joined_dataset(
                    hist_data['d_item'], hist_data['d_akun'], hist_data['d_skmpnen'], hist_data['d_soutput'],
                    ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=hist_data['d_cttakun'], source_label="semula"
                )
        else:
            semula_dash_df = build_joined_dataset(m_item, m_akun, m_skmpnen, m_soutput, ref_satker, ref_skmpnen, ref_dirbag, cttakun_df=None, source_label="semula")
        semula_dash_df = assign_new_cols(semula_dash_df)


        # --- Filters ---
        st.subheader("Filter Data")
        row1_c1, row1_c2, row1_c3 = st.columns(3)
        with row1_c1:
            opts_thang = sorted(main_df['thang'].dropna().unique().tolist()) if 'thang' in main_df.columns else []
            sel_thang = st.multiselect("Tahun (thang)", opts_thang)
        with row1_c2:
            opts_beban = sorted(main_df['kdbeban'].dropna().unique().tolist()) if 'kdbeban' in main_df.columns else []
            sel_beban = st.multiselect("Kode Beban (kdbeban)", opts_beban)
        with row1_c3:
            if 'kdsatker' in main_df.columns:
                if 'nmsatker' in main_df.columns:
                    satker_pairs = main_df[['kdsatker', 'nmsatker']].dropna(subset=['kdsatker']).drop_duplicates()
                    satker_pairs['nmsatker'] = satker_pairs['nmsatker'].fillna("N/A")
                    opts_satker = sorted([f"{row['kdsatker']} - {row['nmsatker']}" for idx, row in satker_pairs.iterrows()])
                else:
                    opts_satker = sorted(main_df['kdsatker'].dropna().unique().tolist())
            else:
                opts_satker = []
            sel_satker = st.multiselect("Kode Satker (kdsatker)", opts_satker)
            
        k_sat_list = [s.split(" - ")[0] for s in sel_satker]
        show_dirbag = ('527010' in k_sat_list)
        
        row2_c1, row2_c2, row2_c3 = st.columns(3)
        with row2_c1:
            if 'kdskmpnen' in main_df.columns:
                skmp_pairs = main_df[['kdskmpnen', 'urskmpnen']].dropna().drop_duplicates()
                skmp_list = [f"{row['kdskmpnen']} - {row['urskmpnen']}" for idx, row in skmp_pairs.iterrows()]
            else:
                skmp_list = []
            sel_skmpnen = st.multiselect("Subkomponen", skmp_list)
            
        with row2_c2:
            sel_dirbag = []
            if show_dirbag and 'kddirbag' in main_df.columns:
                base_527010 = main_df[main_df['kdsatker'] == '527010']
                mask_tagged = base_527010['kddirbag'].astype(str).str.upper().str.startswith('PB.')

                if 'nmdirbag' in base_527010.columns:
                    dirbag_pairs = base_527010[mask_tagged][['kddirbag', 'nmdirbag']].dropna(subset=['kddirbag']).drop_duplicates()
                    dirbag_pairs['nmdirbag'] = dirbag_pairs['nmdirbag'].fillna("N/A")
                    opts_dirbag = sorted([f"{row['kddirbag']} - {row['nmdirbag']}" for idx, row in dirbag_pairs.iterrows()])
                else:
                    opts_dirbag = sorted(base_527010[mask_tagged]['kddirbag'].dropna().unique().tolist())

                # Explicit bucket for rows that don't map to any known
                # PB.xx code, so they're selectable/inspectable instead of
                # silently vanishing from the filter while still showing
                # up (as "Belum Tertandai") in the summary table below.
                if (~mask_tagged).any():
                    opts_dirbag.append('UNTAGGED - Belum Tertandai')

                sel_dirbag = st.multiselect("Direktorat/Bagian", opts_dirbag)
                
        with row2_c3:
            if all(c in main_df.columns for c in ['kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput']):
                ro_pairs = main_df[['kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput']].dropna().drop_duplicates()
                ro_list = sorted([f"{row['kdprogram']}.{row['kdgiat']}.{row['kdoutput']}.{row['kdsoutput']} - {row['ursoutput']}" for idx, row in ro_pairs.iterrows()])
            else:
                ro_list = []
            sel_ro = st.multiselect("Rincian Output", ro_list)

        row3_c1, row3_c2, row3_c3 = st.columns(3)
        with row3_c1:
            opts_akun = sorted(main_df['kdakun'].dropna().unique().tolist()) if 'kdakun' in main_df.columns else []
            sel_akun = st.multiselect("Kode Akun (kdakun)", opts_akun)

        # Apply filters
        f_df = main_df.copy()
        if sel_akun and 'kdakun' in f_df.columns:
            f_df = f_df[f_df['kdakun'].isin(sel_akun)]
        if sel_thang:
            f_df = f_df[f_df['thang'].isin(sel_thang)]
        if sel_beban:
            f_df = f_df[f_df['kdbeban'].isin(sel_beban)]
        if k_sat_list:
            f_df = f_df[f_df['kdsatker'].isin(k_sat_list)]
        if sel_skmpnen:
            k_vals = [s.split(" - ")[0] for s in sel_skmpnen]
            f_df = f_df[f_df['kdskmpnen'].isin(k_vals)]
        if sel_dirbag:
            untagged_selected = 'UNTAGGED - Belum Tertandai' in sel_dirbag
            tagged_codes = [s.split(" - ")[0] for s in sel_dirbag if s != 'UNTAGGED - Belum Tertandai']
            mask = pd.Series(False, index=f_df.index)
            if tagged_codes:
                mask |= f_df['kddirbag'].isin(tagged_codes)
            if untagged_selected:
                mask |= ~f_df['kddirbag'].astype(str).str.upper().str.startswith('PB.')
            f_df = f_df[mask]
        if sel_ro:
            ro_keys = []
            for s in sel_ro:
                parts = s.split(" - ")[0].split(".")
                if len(parts) == 4:
                    ro_keys.append(tuple(parts))
            if ro_keys:
                ro_series = (
                    f_df['kdprogram'].astype(str) + '|' + f_df['kdgiat'].astype(str) + '|' +
                    f_df['kdoutput'].astype(str) + '|' + f_df['kdsoutput'].astype(str)
                )
                valid_keys = ['|'.join(t) for t in ro_keys]
                f_df = f_df[ro_series.isin(valid_keys)]

        # Ensure amounts are properly aggregated
        if 'jumlah' in f_df.columns:
            f_df['jumlah'] = pd.to_numeric(f_df['jumlah'], errors='coerce').fillna(0)

        st.write("---")

        def _apply_dashboard_filters(df):
            d = df.copy()
            if sel_thang and 'thang' in d.columns:
                d = d[d['thang'].isin(sel_thang)]
            if sel_beban and 'kdbeban' in d.columns:
                d = d[d['kdbeban'].isin(sel_beban)]
            if k_sat_list and 'kdsatker' in d.columns:
                d = d[d['kdsatker'].isin(k_sat_list)]
            if sel_skmpnen and 'kdskmpnen' in d.columns:
                k_vals = [s.split(" - ")[0] for s in sel_skmpnen]
                d = d[d['kdskmpnen'].isin(k_vals)]
            if sel_dirbag and 'kddirbag' in d.columns:
                untagged_selected = 'UNTAGGED - Belum Tertandai' in sel_dirbag
                tagged_codes = [s.split(" - ")[0] for s in sel_dirbag if s != 'UNTAGGED - Belum Tertandai']
                mask = pd.Series(False, index=d.index)
                if tagged_codes:
                    mask |= d['kddirbag'].isin(tagged_codes)
                if untagged_selected:
                    mask |= ~d['kddirbag'].astype(str).str.upper().str.startswith('PB.')
                d = d[mask]
            if sel_ro and all(c in d.columns for c in ['kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput']):
                ro_keys = []
                for s in sel_ro:
                    parts = s.split(" - ")[0].split(".")
                    if len(parts) == 4:
                        ro_keys.append(tuple(parts))
                if ro_keys:
                    ro_series = (
                        d['kdprogram'].astype(str) + '|' + d['kdgiat'].astype(str) + '|' +
                        d['kdoutput'].astype(str) + '|' + d['kdsoutput'].astype(str)
                    )
                    valid_keys = ['|'.join(t) for t in ro_keys]
                    d = d[ro_series.isin(valid_keys)]
            if sel_akun and 'kdakun' in d.columns:
                d = d[d['kdakun'].isin(sel_akun)]
            return d

        compare_df = pd.concat([main_df, semula_dash_df], ignore_index=True)
        compare_df = _apply_dashboard_filters(compare_df)
        if 'jumlah' in compare_df.columns:
            compare_df['jumlah'] = pd.to_numeric(compare_df['jumlah'], errors='coerce').fillna(0)

        group_cols = ['kdsatker', 'nmsatker']
        if show_dirbag and 'satdirbag' in compare_df.columns:
            group_cols.append('satdirbag')

        # --- Metrics ---
        st.subheader("Summary Metrics")
        m1, m2, m3 = st.columns(3)

        # Semula reference totals (filtered by everything except the
        # Source selector, so the comparison holds regardless of which
        # source is currently selected for the main metric).
        pagu_total_semula = 0
        pagu_op_semula = 0
        pagu_non_op_semula = 0
        if all(c in compare_df.columns for c in ['source', 'jumlah']):
            semula_only = compare_df[compare_df['source'] == 'semula']
            pagu_total_semula = semula_only['jumlah'].sum()
            if 'kdkmpnen' in semula_only.columns:
                pagu_op_semula = semula_only[semula_only['kdkmpnen'].isin(['001', '002'])]['jumlah'].sum()
                # Nonoperasional = semua komponen SELAIN 001 (Pegawai) dan 002 (Barang Operasional)
                pagu_non_op_semula = semula_only[~semula_only['kdkmpnen'].isin(['001', '002'])]['jumlah'].sum()

        def _fmt_id(v):
            return f"{v:,.0f}".replace(",", ".")

        def _fmt_delta(v):
            return f"{v:+,.0f}".replace(",", ".")

        def _fmt_delta_pct(current, semula):
            """Delta text with the percentage change appended in
            parentheses, e.g. '+1.234.567 (+12,34%)', so it renders right
            next to the value inside st.metric's delta slot. Falls back to
            '(N/A)' when Pagu/Volume Semula is 0 to avoid dividing by zero."""
            diff = current - semula
            base = _fmt_delta(diff)
            if semula == 0:
                return f"{base} (N/A)"
            pct = diff / semula * 100
            return f"{base} ({pct:+.2f}%)"

        if 'jumlah' in f_df.columns:
            pagu_total = f_df['jumlah'].sum()
            
            pagu_op = 0
            pagu_non_op = 0
            if 'kdkmpnen' in f_df.columns:
                pagu_op = f_df[f_df['kdkmpnen'].isin(['001', '002'])]['jumlah'].sum()
                # Nonoperasional = semua komponen SELAIN 001 (Pegawai) dan 002 (Barang Operasional)
                pagu_non_op = f_df[~f_df['kdkmpnen'].isin(['001', '002'])]['jumlah'].sum()
                
            with m1:
                st.metric("Pagu Total", _fmt_id(pagu_total), delta=_fmt_delta_pct(pagu_total, pagu_total_semula))
                st.caption(f"Pagu Semula: {_fmt_id(pagu_total_semula)}")
            with m2:
                st.metric("Pagu Belanja Operasional", _fmt_id(pagu_op), delta=_fmt_delta_pct(pagu_op, pagu_op_semula))
                st.caption(f"Pagu Semula: {_fmt_id(pagu_op_semula)}")
            with m3:
                st.metric("Pagu Belanja Nonoperasional", _fmt_id(pagu_non_op), delta=_fmt_delta_pct(pagu_non_op, pagu_non_op_semula))
                st.caption(f"Pagu Semula: {_fmt_id(pagu_non_op_semula)}")

            st.markdown("**Pagu per Program**")
            if all(c in compare_df.columns for c in ['kdprogram', 'source', 'jumlah']):
                prog_pivot = (
                    compare_df.groupby(['kdprogram', 'source'])['jumlah']
                    .sum()
                    .unstack('source', fill_value=0)
                    .reset_index()
                )
                for col in ['semula', 'menjadi']:
                    if col not in prog_pivot.columns:
                        prog_pivot[col] = 0
                prog_pivot['perubahan'] = prog_pivot['menjadi'] - prog_pivot['semula']
                prog_pivot = prog_pivot.sort_values('kdprogram')

                prog_cols = st.columns(len(prog_pivot)) if len(prog_pivot) > 0 else []
                for col, (_, prow) in zip(prog_cols, prog_pivot.iterrows()):
                    with col:
                        st.metric(
                            f"Pagu Program {prow['kdprogram']}",
                            _fmt_id(prow['menjadi']),
                            delta=_fmt_delta_pct(prow['menjadi'], prow['semula'])
                        )
                        st.caption(f"Pagu Semula: {_fmt_id(prow['semula'])}")
            else:
                st.error("Missing kdprogram column.")

            st.markdown("**Monitoring Pagu Perjadin**")
            PERJADIN_AKUN = ['524111', '524113', '524114', '524119', '524211']
            if all(c in compare_df.columns for c in ['kdakun', 'source', 'jumlah']):
                perjadin_df = compare_df[compare_df['kdakun'].astype(str).isin(PERJADIN_AKUN)]
                pj_semula = perjadin_df[perjadin_df['source'] == 'semula']['jumlah'].sum()
                pj_menjadi = perjadin_df[perjadin_df['source'] == 'menjadi']['jumlah'].sum()
                pj_perubahan = pj_menjadi - pj_semula
                st.metric("Total Pagu Perjadin", _fmt_id(pj_menjadi), delta=_fmt_delta_pct(pj_menjadi, pj_semula))
                st.caption(f"Pagu Semula: {_fmt_id(pj_semula)}")
            else:
                st.error("Missing kdakun column.")

            st.markdown("**Metadata Satker**")
            if 'kdsatker' in f_df.columns and 'nmsatker' in f_df.columns:
                satker_unique = f_df[['kdsatker', 'nmsatker']].dropna(subset=['kdsatker']).drop_duplicates(subset=['kdsatker'])
                nm_upper = satker_unique['nmsatker'].astype(str).str.upper()

                def _contains_any(names):
                    mask = pd.Series(False, index=nm_upper.index)
                    for name in names:
                        mask |= nm_upper.str.contains(name.upper(), regex=False, na=False)
                    return mask

                total_satker = satker_unique['kdsatker'].nunique()
                mask_kppn_khusus = _contains_any(['KPPN Khusus'])
                mask_kppn = _contains_any(['KPPN']) & ~mask_kppn_khusus
                mask_kanwil = _contains_any(['Kanwil'])
                mask_blu = _contains_any([
                    'BADAN PENGELOLA DANA LINGKUNGAN HIDUP (BPDLH)',
                    'PUSAT INVESTASI PEMERINTAH',
                    'BADAN PENGELOLA DANA PERKEBUNAN (BPDP)',
                ])
                mask_satker_khusus = _contains_any([
                    'KOMITE STANDAR AKUNTANSI PEMERINTAH (KSAP)',
                    'KOMITE INVESTASI PEMERINTAH (KIP)',
                ])

                sm1, sm2, sm3 = st.columns(3)
                sm4, sm5, sm6 = st.columns(3)
                with sm1:
                    st.metric("Total Satker", total_satker)
                with sm2:
                    st.metric("Jumlah Satker KPPN Khusus", satker_unique[mask_kppn_khusus]['kdsatker'].nunique())
                with sm3:
                    st.metric("Jumlah KPPN", satker_unique[mask_kppn]['kdsatker'].nunique())
                with sm4:
                    st.metric("Jumlah Satker Kanwil", satker_unique[mask_kanwil]['kdsatker'].nunique())
                with sm5:
                    st.metric("Jumlah BLU", satker_unique[mask_blu]['kdsatker'].nunique())
                with sm6:
                    st.metric("Jumlah Satker Khusus", satker_unique[mask_satker_khusus]['kdsatker'].nunique())
            else:
                st.error("Missing kdsatker/nmsatker column.")
                
        st.write("---")
        
        # --- Ringkasan Pagu Semula vs Menjadi per Satker ---
        st.subheader("Ringkasan Pagu Semula vs Menjadi per Satker")

        if compare_df.empty or 'jumlah' not in compare_df.columns or not all(c in compare_df.columns for c in group_cols):
            st.info("No data based on the current filters.")
        else:
            pivot = (
                compare_df.groupby(group_cols + ['source'])['jumlah']
                .sum()
                .unstack('source', fill_value=0)
                .reset_index()
            )
            for col in ['semula', 'menjadi']:
                if col not in pivot.columns:
                    pivot[col] = 0
            pivot['perubahan'] = pivot['menjadi'] - pivot['semula']

            rename_map = {
                'kdsatker': 'Kode Satker',
                'nmsatker': 'Nama Satker',
                'satdirbag': 'Satker/Direktorat/Bagian',
                'semula': 'Pagu Semula',
                'menjadi': 'Pagu Menjadi',
                'perubahan': 'Perubahan',
            }
            display_cols = group_cols + ['semula', 'menjadi', 'perubahan']
            pivot = pivot[display_cols].rename(columns=rename_map)

            st.dataframe(
                pivot.style.format(
                    {'Pagu Semula': '{:,.0f}', 'Pagu Menjadi': '{:,.0f}', 'Perubahan': '{:,.0f}'}
                ).pipe(apply_stripes),
                use_container_width=True
            )

        st.write("---")
        
        # --- Charts ---
        if f_df.empty:
            st.warning("No data based on the current filters.")
        else:
            st.markdown("**Pagu per Rincian Output**")
            ro_cols = ['kdprogram', 'kdgiat', 'kdoutput', 'kdsoutput', 'ursoutput', 'kdsatker', 'source', 'jumlah']
            if all(c in compare_df.columns for c in ro_cols):
                ro_base = compare_df.copy()
                ro_base['Full RO'] = (
                    ro_base['kdprogram'].astype(str) + '.' +
                    ro_base['kdgiat'].astype(str) + '.' +
                    ro_base['kdoutput'].astype(str) + '.' +
                    ro_base['kdsoutput'].astype(str)
                )

                ro_pivot = (
                    ro_base.groupby(['Full RO', 'ursoutput', 'source'])['jumlah']
                    .sum()
                    .unstack('source', fill_value=0)
                    .reset_index()
                )
                for col in ['semula', 'menjadi']:
                    if col not in ro_pivot.columns:
                        ro_pivot[col] = 0
                ro_pivot['perubahan'] = ro_pivot['menjadi'] - ro_pivot['semula']

                # volsout is repeated across every item row sharing the same
                # RO+satker, so average per (Full RO, satker) first to collapse
                # duplicates, then sum across satkers per Full RO.
                if 'volsout' in ro_base.columns:
                    ro_base['volsout'] = pd.to_numeric(ro_base['volsout'], errors='coerce')
                    vol_per_satker = (
                        ro_base.groupby(['Full RO', 'kdsatker', 'source'])['volsout']
                        .mean()
                        .reset_index()
                    )
                    vol_pivot = (
                        vol_per_satker.groupby(['Full RO', 'source'])['volsout']
                        .sum()
                        .unstack('source', fill_value=0)
                        .reset_index()
                    )
                    for col in ['semula', 'menjadi']:
                        if col not in vol_pivot.columns:
                            vol_pivot[col] = 0
                    vol_pivot['perubahan_vol'] = vol_pivot['menjadi'] - vol_pivot['semula']
                    vol_pivot = vol_pivot.rename(columns={
                        'semula': 'Volume Semula', 'menjadi': 'Volume Menjadi', 'perubahan_vol': 'Perubahan Volume'
                    })
                    ro_pivot = ro_pivot.merge(vol_pivot, on='Full RO', how='left')
                else:
                    ro_pivot['Volume Semula'] = 0
                    ro_pivot['Volume Menjadi'] = 0
                    ro_pivot['Perubahan Volume'] = 0

                out_df = ro_pivot[['Full RO', 'ursoutput', 'semula', 'menjadi', 'perubahan',
                                    'Volume Semula', 'Volume Menjadi', 'Perubahan Volume']].rename(columns={
                    'ursoutput': 'Uraian Rincian Output',
                    'semula': 'Pagu Semula',
                    'menjadi': 'Pagu Menjadi',
                    'perubahan': 'Perubahan',
                })
                st.dataframe(
                    out_df.style.format(
                        {'Pagu Semula': '{:,.0f}', 'Pagu Menjadi': '{:,.0f}', 'Perubahan': '{:,.0f}',
                         'Volume Semula': '{:,.0f}', 'Volume Menjadi': '{:,.0f}', 'Perubahan Volume': '{:,.0f}'}
                    ).pipe(apply_stripes),
                    column_config={
                        "Full RO": st.column_config.Column(width="small"),
                        "Uraian Rincian Output": st.column_config.Column(width="large"),
                        "Pagu Semula": st.column_config.Column(width="small"),
                        "Pagu Menjadi": st.column_config.Column(width="small"),
                        "Perubahan": st.column_config.Column(width="small"),
                        "Volume Semula": st.column_config.Column(width="small"),
                        "Volume Menjadi": st.column_config.Column(width="small"),
                        "Perubahan Volume": st.column_config.Column(width="small"),
                    },
                    use_container_width=True
                    )
            else:
                st.error("Missing columns for Rincian Output.")

            st.write("---")

            c1, c2 = st.columns(2)

            with c1:
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

        # --- Metadata Satker ---
        # Kategorisasi berdasarkan nmsatker (distinct per kdsatker yang
        # muncul di data ADK aktif). Urutan pengecekan penting: KPPN Khusus
        # dicek dan dikeluarkan dulu sebelum menghitung KPPN biasa, supaya
        # tidak dobel hitung.
        satker_names_upper = pd.Series(
            [str(satker_dict.get(s, "")) for s in all_satker]
        ).str.upper()

        mask_kppn_khusus = satker_names_upper.str.contains("KPPN KHUSUS", na=False)
        mask_kppn = satker_names_upper.str.contains("KPPN", na=False) & ~mask_kppn_khusus
        mask_kanwil = satker_names_upper.str.contains("KANWIL", na=False)

        blu_keywords = [
            "BADAN PENGELOLA DANA LINGKUNGAN HIDUP",
            "PUSAT INVESTASI PEMERINTAH",
            "BADAN PENGELOLA DANA PERKEBUNAN",
        ]
        mask_blu = satker_names_upper.str.contains("|".join(blu_keywords), na=False)

        satker_khusus_keywords = [
            "KOMITE STANDAR AKUNTANSI PEMERINTAH",
            "KOMITE INVESTASI PEMERINTAH",
        ]
        mask_satker_khusus = satker_names_upper.str.contains("|".join(satker_khusus_keywords), na=False)

        meta_cols = st.columns(6)
        meta_cols[0].metric("Total Satker", len(all_satker))
        meta_cols[1].metric("KPPN Khusus", int(mask_kppn_khusus.sum()))
        meta_cols[2].metric("KPPN", int(mask_kppn.sum()))
        meta_cols[3].metric("Kanwil", int(mask_kanwil.sum()))
        meta_cols[4].metric("BLU", int(mask_blu.sum()))
        meta_cols[5].metric("Satker Khusus", int(mask_satker_khusus.sum()))

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
