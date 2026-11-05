# CarbonLink Exploration Intelligence | Streamlit prototype

## Important
This is a demonstration prototype using fictional/synthetic exploration records and approximate coordinates. It is not connected to Botswana's Department of Mines, Mining Cadastre Portal or Botswana Geoscience Institute. Do not use real/confidential data unless you have authorisation.

## Windows installation
1. Install Python 3.11+ from https://www.python.org/downloads/ (tick **Add Python to PATH**).
2. Extract this folder to Documents or another working directory.
3. Open Command Prompt in this folder.
4. Create and activate a virtual environment:

   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install packages:

   ```bat
   python -m pip install -r requirements.txt
   ```

6. Launch:

   ```bat
   python -m streamlit run app.py
   ```

7. Open http://localhost:8501 in Chrome/Edge. Keep the terminal open while using the app.

## Features included
- Overview dashboard and synthetic data
- Upload a report and manually enrich metadata
- Search and filter historical records
- Map record coordinates
- Rules-based data quality flags
- Evidence inventory by demonstration licence
- Template context brief with Markdown download
- Simulated Mining Cadastre integration panel

## Not yet implemented
- OCR/AI extraction from uploaded files
- Live portal/API integration
- Verified licence polygons or coordinate transformations
- Authentication, role-based permissions, audit logs or production security
- Geological interpretation/mineral prospectivity prediction

## Data
The demo CSV and licence JSON are created automatically on first run in `data/`.
