import streamlit as st
import pandas as pd
import numpy as np
import json
from pathlib import Path
from datetime import datetime
from io import BytesIO

try:
    import pydeck as pdk
    HAS_PYDECK = True
except Exception:
    HAS_PYDECK = False

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
CSV_PATH = DATA_DIR / "demo_records.csv"
JSON_PATH = DATA_DIR / "demo_licences.json"

st.set_page_config(
    page_title="CarbonLink Exploration Intelligence",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Demo data (fictional, not real Botswana exploration information) ----------
def seed_data():
    records = [
        ["REC-001","PL-DEMO-001","Copper","Drilling","Copper Exploration Programme A",1998,"Demo Exploration Ltd",-22.42,25.88,"UTM 35S","12","Verified","Historical_Report_001.pdf"],
        ["REC-002","PL-DEMO-001","Copper","Geochemical sampling","Soil Sampling Campaign",2001,"Demo Exploration Ltd",-22.45,25.91,"UTM 35S","45","Verified","Sampling_Report_002.pdf"],
        ["REC-003","PL-DEMO-001","Copper","Geophysical survey","Magnetic Survey",2002,"Demo Exploration Ltd",-22.39,25.84,"UTM 35S","","Review","Magnetic_Report_003.pdf"],
        ["REC-004","PL-DEMO-002","Nickel","Drilling","Nickel Reconnaissance",2005,"Example Minerals",-21.90,26.10,"Unknown CRS","8","Review","Nickel_Report_004.pdf"],
        ["REC-005","PL-DEMO-002","Nickel","Geological mapping","Regional Mapping",2004,"Example Minerals",-21.95,26.08,"UTM 35S","0","Verified","Mapping_Report_005.pdf"],
        ["REC-006","PL-DEMO-003","Manganese","Geochemical sampling","Manganese Sampling",1996,"Sample Resources",-23.10,24.70,"UTM 35S","30","Verified","Mn_Report_006.pdf"],
        ["REC-007","PL-DEMO-003","Manganese","Drilling","Follow-up Drilling",1997,"Sample Resources",-23.12,24.73,"UTM 35S","6","Review","Drilling_Report_007.pdf"],
        ["REC-008","PL-DEMO-004","Gold","Geophysical survey","Gold Target Survey",2010,"Fictional Prospecting",-20.80,27.20,"UTM 35S","0","Verified","Gold_Report_008.pdf"],
        ["REC-009","PL-DEMO-004","Gold","Drilling","Target Testing",2011,None,-20.82,27.18,"UTM 35S","4","Review","Target_Report_009.pdf"],
        ["REC-010","PL-DEMO-005","Coal","Geological mapping","Coal Basin Mapping",1989,"Demo Energy",-21.30,25.40,"UTM 35S","0","Verified","Coal_Report_010.pdf"],
        ["REC-011","PL-DEMO-005","Coal","Drilling","Coal Exploration",1990,"Demo Energy",-21.32,25.42,"UTM 35S","15","Verified","Coal_Report_011.pdf"],
        ["REC-012","PL-DEMO-006","Copper","Geochemical sampling","Copper Soil Survey",2016,"Example Minerals",-22.00,26.50,"UTM 35S","60","Review","Soil_Report_012.pdf"],
    ["REC-013","PL-DEMO-006","Copper","Drilling","Exploration Drilling",2017,"Example Minerals",-22.03,26.52,"UTM 35S","10","Verified","Drill_Report_013.pdf"],
        ["REC-014","PL-DEMO-007","Lithium","Geological mapping","Pegmatite Mapping",2020,"Demo Lithium",-23.50,25.10,"UTM 35S","0","Review","Lithium_Report_014.pdf"],
        ["REC-015","PL-DEMO-007","Lithium","Geochemical sampling","Pegmatite Sampling",2021,"Demo Lithium",-23.53,25.13,"UTM 35S","25","Verified","Lithium_Sampling_015.pdf"],
    ["REC-016","PL-DEMO-008","Iron","Drilling","Iron Ore Drilling",2008,"Sample Resources",-20.50,26.00,"UTM 35S","9","Verified","Iron_Report_016.pdf"],
    ["REC-017","PL-DEMO-008","Iron","Geophysical survey","Magnetic Survey",2007,"Sample Resources",-20.48,26.02,"UTM 35S","0","Review","Iron_Geophysics_017.pdf"],
    ["REC-018","PL-DEMO-009","Copper","Drilling","Copper Drill Programme",2014,"Demo Exploration Ltd",-22.70,25.20,"UTM 35S","11","Verified","Copper_Report_018.pdf"],
    ["REC-019","PL-DEMO-009","Copper","Drilling","Copper Drill Programme",2014,"Demo Exploration Ltd",-22.70,25.20,"UTM 35S","11","Review","Copper_Report_018_copy.pdf"],
    ["REC-020","PL-DEMO-010","Silver","Geochemical sampling","Silver Sampling",2003,"Fictional Prospecting",None,None,"Unknown CRS","20","Review","Silver_Report_020.pdf"],
    ["REC-021","PL-DEMO-010","Silver","Geological mapping","Silver Mapping",2002,"Fictional Prospecting",-21.10,24.90,"UTM 35S","0","Verified","Silver_Map_021.pdf"],
    ["REC-022","PL-DEMO-011","Uranium","Geophysical survey","Radiometric Survey",1982,"Demo Energy",-19.90,25.90,"UTM 35S","0","Review","Uranium_Report_022.pdf"],
    ["REC-023","PL-DEMO-011","Uranium","Drilling","Uranium Follow-up",1983,"Demo Energy",-19.92,25.92,"UTM 35S","5","Verified","Uranium_Drill_023.pdf"],
    ["REC-024","PL-DEMO-012","Rare earths","Geochemical sampling","REE Reconnaissance",2022,"Demo Minerals",-22.20,26.20,"UTM 35S","35","Verified","REE_Report_024.pdf"],
    ["REC-025","PL-DEMO-012","Rare earths","Geological mapping","REE Mapping",2022,"Demo Minerals",-22.22,26.22,"UTM 35S","0","Review","REE_Map_025.pdf"],
    ["REC-026","PL-DEMO-001","Copper","Drilling","Copper Exploration Programme A",1998,"Demo Exploration Ltd",-22.42,25.88,"UTM 35S","12","Review","Historical_Report_001_copy.pdf"],
    ["REC-027","PL-DEMO-004","Gold","Geochemical sampling","Gold Soil Sampling",2009,"Fictional Prospecting",-20.78,27.23,"UTM 35S","40","Verified","Gold_Sampling_027.pdf"],
    ["REC-028","PL-DEMO-006","Copper","Geophysical survey","IP Survey",2015,"Example Minerals",-22.01,26.48,"UTM 35S","0","Review","IP_Report_028.pdf"],
    ["REC-029","PL-DEMO-008","Iron","Geological mapping","Iron Mapping",2006,"Sample Resources",-20.51,26.01,"UTM 35S","0","Verified","Iron_Map_029.pdf"],
    ["REC-030","PL-DEMO-009","Copper","Geochemical sampling","Copper Sampling",2013,"Demo Exploration Ltd",-22.68,25.18,"UTM 35S","50","Verified","Copper_Sampling_030.pdf"],
    ["REC-031","PL-DEMO-003","Manganese","Drilling","Follow-up Drilling",1997,"Sample Resources",-23.12,24.73,"UTM 35S","6","Review","Drilling_Report_007_copy.pdf"],
    ["REC-032","PL-DEMO-007","Lithium","Drilling","Lithium Target Testing",2023,"Demo Lithium",-23.55,25.15,"UTM 35S","3","Review","Lithium_Drill_032.pdf"],
    ["REC-033","PL-DEMO-002","Nickel","Geochemical sampling","Nickel Sampling",2006,"Example Minerals",-21.91,26.12,"UTM 35S","28","Verified","Nickel_Sampling_033.pdf"],
    ["REC-034","PL-DEMO-005","Coal","Geophysical survey","Coal Seismic Survey",1988,"Demo Energy",-21.28,25.39,"UTM 35S","0","Verified","Coal_Seismic_034.pdf"],
    ["REC-035","PL-DEMO-010","Silver","Drilling","Silver Drill Testing",2004,"Fictional Prospecting",-21.12,24.92,"UTM 35S","7","Review","Silver_Drill_035.pdf"],
    ["REC-036","PL-DEMO-012","Rare earths","Drilling","REE Drill Testing",2023,"Demo Minerals",-22.24,26.24,"UTM 35S","4","Verified","REE_Drill_036.pdf"],
    ["REC-037","PL-DEMO-001","Copper","Geological mapping","Copper Mapping",1997,"Demo Exploration Ltd",-22.40,25.86,"UTM 35S","0","Verified","Copper_Map_037.pdf"],
    ["REC-038","PL-DEMO-004","Gold","Geophysical survey","Gold Magnetic Survey",2008,"Fictional Prospecting",-20.76,27.21,"UTM 35S","0","Review","Gold_Mag_038.pdf"],
    ["REC-039","PL-DEMO-006","Copper","Drilling","Copper Drill Programme",2017,"Example Minerals",-22.03,26.52,"UTM 35S","10","Review","Drill_Report_013_copy.pdf"],
    ["REC-040","PL-DEMO-011","Uranium","Geochemical sampling","Uranium Sampling",1981,"Demo Energy",-19.88,25.88,"UTM 35S","22","Verified","Uranium_Sampling_040.pdf"],
    ]
    cols = ["record_id","licence_id","mineral","activity","title","year","company","latitude","longitude","crs","drill_holes","review_status","source_file"]
    df = pd.DataFrame(records, columns=cols)
    df.to_csv(CSV_PATH, index=False)
    licences = {
        "PL-DEMO-001":{"name":"Copper Demonstration Block A","mineral":"Copper","lat":-22.42,"lon":25.88},
        "PL-DEMO-002":{"name":"Nickel Demonstration Block","mineral":"Nickel","lat":-21.90,"lon":26.10},
        "PL-DEMO-003":{"name":"Manganese Demonstration Block","mineral":"Manganese","lat":-23.10,"lon":24.70},
        "PL-DEMO-004":{"name":"Gold Demonstration Block","mineral":"Gold","lat":-20.80,"lon":27.20},
        "PL-DEMO-005":{"name":"Coal Demonstration Block","mineral":"Coal","lat":-21.30,"lon":25.40},
        "PL-DEMO-006":{"name":"Copper Demonstration Block B","mineral":"Copper","lat":-22.00,"lon":26.50},
        "PL-DEMO-007":{"name":"Lithium Demonstration Block","mineral":"Lithium","lat":-23.50,"lon":25.10},
        "PL-DEMO-008":{"name":"Iron Demonstration Block","mineral":"Iron","lat":-20.50,"lon":26.00},
        "PL-DEMO-009":{"name":"Copper Demonstration Block C","mineral":"Copper","lat":-22.70,"lon":25.20},
        "PL-DEMO-010":{"name":"Silver Demonstration Block","mineral":"Silver","lat":-21.10,"lon":24.90},
        "PL-DEMO-011":{"name":"Uranium Demonstration Block","mineral":"Uranium","lat":-19.90,"lon":25.90},
        "PL-DEMO-012":{"name":"Rare Earth Demonstration Block","mineral":"Rare earths","lat":-22.20,"lon":26.20},
    }
    JSON_PATH.write_text(json.dumps(licences, indent=2), encoding="utf-8")

if not CSV_PATH.exists():
    seed_data()

@st.cache_data
def load_records():
    return pd.read_csv(CSV_PATH)

df = load_records()
licences = json.loads(JSON_PATH.read_text(encoding="utf-8"))

# ---------- helpers ----------
def quality_flags(row):
    flags = []
    if pd.isna(row.get("latitude")) or pd.isna(row.get("longitude")):
        flags.append("Missing coordinates")
    if str(row.get("crs","")).strip().lower() in ["unknown crs","unknown",""]:
        flags.append("Unknown coordinate reference system")
    if pd.isna(row.get("company")) or str(row.get("company","")).strip() == "":
        flags.append("Missing company")
    if pd.isna(row.get("year")):
        flags.append("Missing report year")
    if pd.isna(row.get("mineral")) or str(row.get("mineral","")).strip() == "":
        flags.append("Missing mineral")
    return flags

def flagged_df(data):
    out = data.copy()
    out["quality_flags"] = out.apply(lambda r: "; ".join(quality_flags(r)), axis=1)
    out["quality_issue_count"] = out["quality_flags"].apply(lambda x: 0 if not x else len(x.split("; ")))
    return out

def safe_num(v):
    try: return float(v)
    except: return None

# ---------- styling ----------
st.markdown("""
<style>
.block-container {padding-top: 1.6rem; padding-bottom: 2rem;}
[data-testid="stSidebar"] {background-color: #10251e;}
[data-testid="stSidebar"] * {color: #f3f7f4;}
div[data-testid="stMetric"] {background: #f4f7f5; border: 1px solid #dbe5df; padding: 14px; border-radius: 10px;}
.small-note {color:#64748b;font-size:0.85rem;}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("# 🧭 CarbonLink")
st.sidebar.caption("EXPLORATION INTELLIGENCE")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", [
    "Overview",
    "Upload & Enrich",
    "Historical Records",
    "Exploration Map",
    "Data Quality",
    "Evidence Analysis",
    "Context Brief",
    "Portal Integration Demo",
])
st.sidebar.markdown("---")
st.sidebar.warning("DEMO ENVIRONMENT\n\nAll records and locations are fictional. No live government portal is connected.")

st.title("CarbonLink Exploration Intelligence")
st.caption("From historical records to spatially contextualised exploration evidence")

# ---------- Overview ----------
if page == "Overview":
    st.markdown("### Exploration information, made discoverable")
    st.write("A demonstration intelligence layer for enriching, searching, checking and spatially reviewing historical mineral exploration records.")
    total = len(df)
    licences_n = df["licence_id"].nunique()
    review_n = (df["review_status"].str.lower() == "review").sum()
    qdf = flagged_df(df)
    issues_n = (qdf["quality_issue_count"] > 0).sum()
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Historical records", total)
    c2.metric("Demo licences", licences_n)
    c3.metric("Records flagged for review", int(review_n))
    c4.metric("Records with data-quality flags", int(issues_n))
    st.markdown("### Workflow")
    st.info("Upload / enrich → Search records → Review spatial context → Identify data gaps → Generate a source-linked context brief")
    left,right = st.columns([1.15,1])
    with left:
        st.markdown("#### Records by mineral")
        st.bar_chart(df["mineral"].value_counts())
    with right:
        st.markdown("#### Records by activity")
        st.bar_chart(df["activity"].value_counts())
    st.markdown("#### Recent demonstration records")
    st.dataframe(df.head(8), use_container_width=True, hide_index=True)
    st.caption("Illustrative dashboard metrics only. Dataset is synthetic.")

# ---------- Upload & Enrich ----------
elif page == "Upload & Enrich":
    st.header("Historical Record Enrichment")
    st.write("Upload a report and capture its metadata. This demonstration stores the uploaded file locally and allows manual metadata entry.")
    uploaded = st.file_uploader("Upload a historical exploration report (PDF, DOCX, TXT)", type=["pdf","docx","txt"])
    with st.form("metadata_form"):
        a,b = st.columns(2)
        with a:
            title = st.text_input("Report title")
            licence = st.text_input("Licence reference")
            mineral = st.selectbox("Mineral", ["Copper","Nickel","Gold","Lithium","Manganese","Iron","Coal","Uranium","Silver","Rare earths","Other"])
            year = st.number_input("Report year", min_value=1900, max_value=2026, value=2000)
        with b:
            company = st.text_input("Exploration company / author")
            activity = st.selectbox("Exploration activity", ["Drilling","Geological mapping","Geochemical sampling","Geophysical survey","Other"])
            crs = st.selectbox("Coordinate reference system", ["UTM 35S","UTM 34S","WGS84","Unknown CRS"])
            lat = st.text_input("Latitude (optional)")
            lon = st.text_input("Longitude (optional)")
        submitted = st.form_submit_button("Save enriched record")
    if submitted:
        if not uploaded:
            st.error("Upload a source document before saving.")
        elif not title or not licence:
            st.error("Please provide at least a report title and licence reference.")
        else:
            file_path = DATA_DIR / uploaded.name
            file_path.write_bytes(uploaded.getvalue())
            new_id = f"REC-{datetime.now().strftime('%y%m%d%H%M%S')}"
            new_row = {
                "record_id":new_id,"licence_id":licence,"mineral":mineral,"activity":activity,
                "title":title,"year":int(year),"company":company or None,
                "latitude":safe_num(lat),"longitude":safe_num(lon),"crs":crs,
                "drill_holes":None,"review_status":"Review","source_file":uploaded.name
            }
            updated = pd.concat([load_records(),pd.DataFrame([new_row])],ignore_index=True)
            updated.to_csv(CSV_PATH,index=False)
            load_records.clear()
            st.success(f"Record saved as {new_id}. Metadata is user-entered; automated OCR/AI extraction is not connected in this version.")
            st.json(new_row)
    st.markdown("#### Extraction status")
    st.warning("OCR and AI extraction are not yet connected. This screen demonstrates the ingestion and metadata-review workflow.")

# ---------- Historical Records ----------
elif page == "Historical Records":
    st.header("Historical Records Search")
    x,y,z = st.columns(3)
    search = x.text_input("Search title, licence, company or source")
    minerals = y.multiselect("Mineral", sorted(df["mineral"].dropna().unique()))
    activities = z.multiselect("Activity", sorted(df["activity"].dropna().unique()))
    result = df.copy()
    if search:
        mask = result.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
        result = result[mask]
    if minerals: result = result[result["mineral"].isin(minerals)]
    if activities: result = result[result["activity"].isin(activities)]
    st.caption(f"{len(result)} matching records")
    st.dataframe(result, use_container_width=True, hide_index=True)
    st.download_button("Download search results (CSV)", result.to_csv(index=False).encode("utf-8"), "carbonlink_search_results.csv", "text/csv")

# ---------- Exploration Map ----------
elif page == "Exploration Map":
    st.header("Exploration Footprint Quality Assurance")
    st.write("Visualise synthetic historical exploration record locations. Points are approximate demo coordinates, not verified licence boundaries.")
    lic = st.selectbox("Filter by licence", ["All licences"] + sorted(df["licence_id"].unique()))
    mapdf = df.dropna(subset=["latitude","longitude"]).copy()
    if lic != "All licences": mapdf = mapdf[mapdf["licence_id"] == lic]
    if mapdf.empty:
        st.info("No coordinate records available for this filter.")
    else:
        st.map(mapdf.rename(columns={"latitude":"lat","longitude":"lon"})[["lat","lon"]], zoom=5)
        st.dataframe(mapdf[["record_id","licence_id","title","activity","latitude","longitude","crs","source_file"]], use_container_width=True, hide_index=True)
    st.warning("This prototype uses point locations only. Licence polygons, CRS transformation and geometry validation require verified spatial source data.")

# ---------- Data Quality ----------
elif page == "Data Quality":
    st.header("Exploration Evidence Gap Analysis")
    qdf = flagged_df(df)
    flagged = qdf[qdf["quality_issue_count"] > 0]
    m1,m2,m3 = st.columns(3)
    m1.metric("Records assessed", len(qdf))
    m2.metric("Records with flags", len(flagged))
    m3.metric("Total field-level flags", int(qdf["quality_issue_count"].sum()))
    counts = {}
    for flags in qdf["quality_flags"]:
        if flags:
            for f in flags.split("; "): counts[f] = counts.get(f,0)+1
    st.markdown("#### Quality issues by type")
    if counts: st.bar_chart(pd.Series(counts).sort_values(ascending=False))
    st.markdown("#### Records requiring review")
    st.dataframe(flagged[["record_id","licence_id","title","source_file","quality_flags","review_status"]], use_container_width=True, hide_index=True)
    st.caption("Rules-based checks only. Flags identify items for human review; they do not automatically establish that a record is wrong.")

# ---------- Evidence Analysis ----------
elif page == "Evidence Analysis":
    st.header("Historical Evidence Analysis")
    lic = st.selectbox("Select a demonstration licence", sorted(df["licence_id"].unique()))
    selected = df[df["licence_id"] == lic]
    st.subheader(f"{lic} | {licences.get(lic,{}).get('name','Demo licence')}")
    a,b,c = st.columns(3)
    a.metric("Associated records", len(selected))
    b.metric("Activity types", selected["activity"].nunique())
    c.metric("Years represented", f"{selected['year'].min():.0f}–{selected['year'].max():.0f}")
    st.markdown("#### Evidence inventory")
    st.dataframe(selected[["record_id","year","mineral","activity","title","source_file","review_status"]], use_container_width=True, hide_index=True)
    st.markdown("#### Coverage indicators")
    st.write("Activity types documented:", ", ".join(sorted(selected["activity"].unique())))
    st.write("Records with coordinates:", int(selected[["latitude","longitude"]].notna().all(axis=1).sum()), "of", len(selected))
    st.write("Records marked for review:", int((selected["review_status"]=="Review").sum()))
    st.warning("These are evidence inventory indicators, not an assessment of mineral potential or exploration success.")

# ---------- Context Brief ----------
elif page == "Context Brief":
    st.header("Historical Exploration Context Brief")
    lic = st.selectbox("Choose licence / area", sorted(df["licence_id"].unique()))
    selected = df[df["licence_id"] == lic].copy()
    flagged = flagged_df(selected)
    if st.button("Generate demonstration brief", type="primary"):
        info = licences.get(lic,{})
        minerals = ", ".join(sorted(selected["mineral"].dropna().unique()))
        activities = ", ".join(sorted(selected["activity"].dropna().unique()))
        years = f"{int(selected['year'].min())}–{int(selected['year'].max())}" if selected["year"].notna().any() else "Not available"
        coords = int(selected[["latitude","longitude"]].notna().all(axis=1).sum())
        review = int((selected["review_status"]=="Review").sum())
        issue_count = int(flagged["quality_issue_count"].sum())
        brief = f"""# Historical Exploration Context Brief: {lic}

**Demonstration status:** Synthetic dataset. Not an official geological assessment.

## Area and record overview
- Demonstration area: {info.get('name','Not supplied')}
- Mineral commodities represented: {minerals}
- Records associated with area: {len(selected)}
- Reporting period represented: {years}
- Exploration activities documented: {activities}

## Historical evidence inventory
- Records with coordinate pairs: {coords} of {len(selected)}
- Records marked for review: {review}
- Field-level data quality flags: {issue_count}

## Data limitations and review priorities
- Confirm licence-to-record associations against authoritative records.
- Verify coordinate reference systems and spatial locations.
- Review incomplete metadata and potential duplicates.
- Confirm document provenance, ownership and disclosure permissions.
- Treat extracted statements as requiring source-document verification.

## Sources
{chr(10).join('- '+str(x) for x in selected['source_file'].tolist())}

**Interpretation boundary:** This brief summarises the availability and quality of historical information. It does not infer mineral prospectivity, establish discoveries or replace qualified geological interpretation.
"""
        st.markdown(brief)
        st.download_button("Download brief (Markdown)", brief, f"{lic}_context_brief.md", "text/markdown")
    st.caption("This is a rules-based template. Source-grounded AI summarisation can be added after document text extraction and retrieval are implemented.")

# ---------- Portal Integration Demo ----------
elif page == "Portal Integration Demo":
    st.header("Mining Cadastre Integration Demonstrator")
    st.write("A simulated workflow showing how a historical exploration intelligence layer could be accessed alongside licence information.")
    lic = st.selectbox("Select demonstration licence", sorted(df["licence_id"].unique()))
    info = licences.get(lic,{})
    selected = df[df["licence_id"]==lic]
    left,right = st.columns([1,1])
    with left:
        st.markdown("#### Licence panel (mock)")
        st.text_input("Licence reference", lic, disabled=True)
        st.text_input("Demonstration area name", info.get("name",""), disabled=True)
        st.text_input("Primary mineral (demo)", info.get("mineral",""), disabled=True)
        st.success("Licence selected")
    with right:
        st.markdown("#### CarbonLink intelligence layer")
        st.metric("Historical records linked", len(selected))
        st.metric("Records requiring review", int((selected["review_status"]=="Review").sum()))
        st.metric("Document sources", selected["source_file"].nunique())
        if st.button("Open historical intelligence panel"):
            st.session_state["portal_open"] = True
    if st.session_state.get("portal_open",False):
        st.markdown("### Historical intelligence panel")
        st.dataframe(selected[["record_id","title","year","activity","source_file","review_status"]], use_container_width=True, hide_index=True)
        st.info("Concept demonstration only. No connection, API access or data exchange with Botswana's live Mining Cadastre Portal has been established.")
    st.markdown("---")
    st.caption("Production integration would require institutional approval, agreed data standards, APIs or another approved interface, access controls and security review.")

st.sidebar.caption("CarbonLink Technologies | Prototype v0.1 | Synthetic data")
