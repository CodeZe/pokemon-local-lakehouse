# Local Data Lakehouse System Architecture

This repository contains the complete implementation of a localized, production-grade **Medallion Data Lakehouse** engineered for **zero-Docker execution** on highly resource-constrained host hardware (**8 GB RAM Laptop**). 

The pipeline ingests raw REST API payloads, processes transactional tables using Apache Iceberg storage layouts via PySpark, runs low-latency analytical queries using DuckDB, and exposes a decoupled metric layer via the Cube.dev semantic framework.

---

## 🗺️ System Architecture

```
[Pokemon API] ──(Python: Requests)──> [Bronze Layer: Raw JSON]
                                              │
                                       (PySpark Engine)
                                              │
                                              ▼
                                 [Iceberg Lakehouse Warehouse]
                                 ├── Silver (Cleaned Tables)
                                 └── Gold (Star Schema Fact/Dims)
                                              │
                                        (DuckDB Engine)
                                              │
                                              ▼
                                   [Cube.dev Semantic Layer]
                                              │
                                        (BI Analytics)
                                              ▼
                                     [Apache Superset]
```

---

## ⚙️ OS & Environment Optimization (WSL 2)

To bypass cross-OS translation layer lag and constrain virtualization engine RAM usage (`vmmem`), you must implement these host performance optimizations.

### 1. File System Path Placement
All work must execute within the native Linux directory structure. Avoid mounting scripts out of `/mnt/c/`.
```bash
cd ~
mkdir pokemon_lakehouse && cd pokemon_lakehouse
```

### 2. Virtual Subsystem Resource Caping (`.wslconfig`)
Create a configuration file at `C:\Users\<Your_Windows_Username>\.wslconfig` within your Windows host filesystem and paste the following parameters to ensure both operating environments stay stable:
```ini
[wsl2]
memory=3GB
processors=2
```
Apply the hard hardware constraint via Windows PowerShell:
```powershell
wsl --shutdown
```

---

## 📁 Repository Directory Layout

```text
pokemon_lakehouse/
│
├── 📁 data/
│   ├── 📁 bronze/                      # Raw JSON files extracted from API
│   └── 📁 iceberg_warehouse/           # PySpark managed Silver & Gold Iceberg tables
│       └── 📁 default/                 # PySpark default storage namespace
│           ├── 📁 silver_pokemon/      # Cleaned Silver Iceberg table
│           ├── 📁 dim_pokemon_types/   # Gold Dimension Iceberg table
│           └── 📁 fct_pokemon_metrics/ # Gold Fact Iceberg table
│
├── 📁 cube_semantic/                   # Node.js / NPM Cube.dev semantic layer project
│   ├── 📁 data/                        # Symlink pointing back to root data/ folder
│   └── 📁 model/                       # Semantic definitions root
│       ├── 📁 cubes/                   # Core data models folder
│       │   ├── 📄 pokemon_metrics.yml  # Fact table declarations & joins
│       │   └── 📄 pokemon_types.yml    # Dimension table declarations
│       └── 📁 views/                   # User-facing security/aggregation layers
│
├── 📄 .gitignore                       # Explicit Git folder exclusion rules
├── 📄 README.md                        # Project documentation handbook
├── 📄 ingest_bronze.py                 # Phase 1: API parsing & extraction
├── 📄 transform_medallion.py           # Phase 2: PySpark Medallion Iceberg execution
├── 📄 test_duckdb.py                   # Phase 3: Analytical snapshot tests
└── 📄 test_duckdb_join.py              # Phase 4: Embedded Star-Schema validation joins
```

---

## 📥 Prerequisite Runtime Installations

### 1. Java 17 & Node.js Environment
PySpark 3.5.0 requires Java 17 execution support. Run these commands inside your WSL terminal to pull verified packages:
```bash
# Install OpenJDK 17
sudo apt update && sudo apt install -y openjdk-17-jdk
sudo update-java-alternatives --set java-1.17.0-openjdk-amd64

# Install Node Version Manager (NVM) & Long-Term Support Node
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
source ~/.bashrc
nvm install --lts
```

### 2. Python Virtual Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install pyspark==3.5.0 pyiceberg duckdb requests apache-superset
```

### 3. Cube.js Global CLI Installation
```bash
npm install -g cubejs-cli --allow-scripts=@cubejs-backend/native,es5-ext
```

---

## 🏗️ Execution Blueprint

### Step 1: Raw Ingestion to Bronze Layer
```bash
python ingest_bronze.py
```

### Step 2: Medallion Processing via PySpark
Clear out cached Ivy runtime directory objects before executing to prevent engine initialization failures:
```bash
rm -rf ~/.ivy2/cache/org.apache.iceberg/
python transform_medallion.py
```

### Step 3: High-Speed Embedded Verification via DuckDB
Test multi-directory analytical folder schema scanning natively without database storage server management layers:
```bash
python test_duckdb_join.py
```

### Step 4: Semantic Layer Bootstrap & Initialization
```bash
# Setup semantic project workspace
cubejs create cube_semantic -d duckdb
cd cube_semantic

# Apply directory symlink fix to handle relative metadata paths
ln -s /home/\(USER/pokemon_lakehouse/data /home/\)USER/pokemon_lakehouse/cube_semantic/data
```

Configure your environment properties within `cube_semantic/.env` using the absolute parameter blocks defined below:
```env
CUBEJS_DEV_MODE=true
CUBEJS_DB_TYPE=duckdb
CUBEJS_EXTERNAL_DEFAULT=true
CUBEJS_SCHEDULED_REFRESH_DEFAULT=true
CUBEJS_SCHEMA_PATH=model
CUBEJS_WEB_SOCKETS=true
CUBEJS_API_SECRET=XXXXX
CUBEJS_DB_INIT_SQL=INSTALL iceberg; LOAD iceberg; SET unsafe_enable_version_guessing = true;
```

Deploy your semantic structure models within `cube_semantic/model/cubes/` and trigger execution:
```bash
# Boot Cube.dev playground engine
npm run dev
```
Open `http://localhost:4000` inside your web browser to test metric aggregation layers within the interface sandbox environment.