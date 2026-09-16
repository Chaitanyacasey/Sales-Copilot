import pandas as pd
import numpy as np

def get_system_kpis():
    """Returns top-level key performance metrics for AXIO REI Sales Copilot."""
    return {
        "active_listings": "10,248",
        "pre_call_research_time": "0 mins (down from 30 mins)",
        "p99_latency": "342 ms (target <800ms)",
        "conversion_rate_lift": "+67.6% (14.2% → 23.8%)",
        "gke_pods_active": "12 / 16 (HPA Auto-scaled)",
        "airflow_dag_success": "99.94%"
    }

def get_conversion_rate_data():
    """Generates monthly conversion rate trend before and after Sales Copilot RAG deployment."""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    before_rag = [13.8, 14.1, 14.2, 14.0, 14.3, 14.2, 13.9, 14.1, 14.2]
    after_rag = [14.0, 14.2, 14.5, 17.8, 20.4, 22.1, 23.2, 23.6, 23.8] # RAG launched in Apr
    
    df = pd.DataFrame({
        "Month": months,
        "Legacy Manual Process (%)": before_rag,
        "AXIO Sales-Copilot RAG (%)": after_rag
    })
    return df

def get_latency_distribution_data():
    """Generates p50, p90, p95, p99 latency data for GKE FastAPI microservices."""
    endpoints = ["/api/v1/rag/copilot", "/api/v1/validator/langgraph", "/api/v1/briefs/nightly", "/api/v1/listings/hnsw-search"]
    p50 = [120, 45, 210, 85]
    p90 = [240, 95, 380, 160]
    p99 = [342, 140, 520, 290]
    
    df = pd.DataFrame({
        "Microservice Endpoint": endpoints,
        "p50 Latency (ms)": p50,
        "p90 Latency (ms)": p90,
        "p99 Latency (ms)": p99,
        "SLA Target": ["<800 ms"] * 4,
        "Status": ["PASS", "PASS", "PASS", "PASS"]
    })
    return df

def get_airflow_dag_runs():
    """Generates recent Airflow DAG run telemetry for nightly RAG Agent Brief generation."""
    runs = [
        {"dag_id": "nightly_polyglot_ingestion", "execution_date": "2026-09-15 02:00:00", "duration_sec": 412, "records_processed": 10248, "status": "SUCCESS"},
        {"dag_id": "nightly_rag_brief_synth", "execution_date": "2026-09-15 02:15:00", "duration_sec": 680, "briefs_generated": 1420, "status": "SUCCESS"},
        {"dag_id": "hnsw_index_rebuild", "execution_date": "2026-09-15 03:00:00", "duration_sec": 195, "vector_dim": 1536, "status": "SUCCESS"},
        {"dag_id": "langgraph_zoning_audit", "execution_date": "2026-09-15 03:30:00", "duration_sec": 310, "discrepancies_fixed": 14, "status": "SUCCESS"},
    ]
    return pd.DataFrame(runs)
