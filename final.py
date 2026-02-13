from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Literal
from esg_engine import ESGCalculator 
from file_parser import parse_document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
import matplotlib
import matplotlib.pyplot as plt
import io
import datetime

# Use Non-GUI backend for server stability
matplotlib.use('Agg')

app = FastAPI(title="ESG Scorer AI (Final)", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class CompanyProfile(BaseModel):
    industry: Literal["IT/Services", "Manufacturing", "Retail", "Cement/Steel", "Pharma"]
    annual_revenue_inr: float = Field(..., gt=0)
    total_employees: int = Field(..., gt=0)

class EnvironmentalData(BaseModel):
    total_energy_consumption_kwh: float = Field(..., ge=0)
    renewable_energy_kwh: float = Field(..., ge=0)
    total_water_consumption_liters: float = Field(..., ge=0)
    waste_generated_kg: float = Field(..., ge=0)
    waste_recycled_kg: float = Field(..., ge=0)

class SocialData(BaseModel):
    female_employees: int = Field(..., ge=0)
    employees_with_disabilities: int = Field(..., ge=0)
    safety_accidents_count: int = Field(..., ge=0)
    employees_trained_count: int = Field(..., ge=0)
    complaints_received_sexual_harassment: int = Field(..., ge=0)

class GovernanceData(BaseModel):
    has_sustainability_committee: bool
    regulatory_fines_paid_inr: float = Field(..., ge=0)
    policies_implemented: List[str]

class ESGRequest(BaseModel):
    company_profile: CompanyProfile
    environmental: EnvironmentalData
    social: SocialData
    governance: GovernanceData

# --- HELPERS ---
def get_radar_chart_bytes(scores):
    categories = ['Env', 'Social', 'Gov']
    values = [scores['environmental'], scores['social'], scores['governance']]
    values += values[:1]
    angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='#1f77b4', alpha=0.4)
    ax.plot(angles, values, color='#1f77b4', linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticklabels([])
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    return buf

def create_pdf_report(data, filename="esg_audit_report.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFillColor(colors.darkblue)
    c.rect(0, height-100, width, 100, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height-60, "ESG AUDIT REPORT")
    
    # Summary
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height-150, "Executive Summary")
    c.setFont("Helvetica", 14)
    c.drawString(50, height-180, f"Total Score: {data['scores']['total']}")
    c.drawString(50, height-200, f"Industry: {data['company_profile']['industry']}")

    # Embed Graph
    graph_buf = get_radar_chart_bytes(data['scores'])
    c.drawImage(ImageReader(graph_buf), 300, height-350, 250, 250, mask='auto')

    # Recommendations
    y = height-400
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "AI Recommendations:")
    c.setFont("Helvetica", 10)
    y -= 25
    if not data['recommendations']:
        c.drawString(50, y, "• Excellent Compliance.")
    else:
        for rec in data['recommendations']:
            c.drawString(50, y, f"• {rec}")
            y -= 20
    c.save()

# --- ENDPOINTS ---
@app.post("/calculate_score")
def calculate_esg(request: ESGRequest):
    try:
        return ESGCalculator(request.dict()).compute()
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/generate_graph")
def generate_graph(request: ESGRequest):
    try:
        res = ESGCalculator(request.dict()).compute()
        return StreamingResponse(get_radar_chart_bytes(res['scores']), media_type="image/png")
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/generate_report")
def generate_report(request: ESGRequest):
    try:
        req_data = request.dict()
        res = ESGCalculator(req_data).compute()
        res['company_profile'] = req_data['company_profile']
        create_pdf_report(res)
        return FileResponse("esg_audit_report.pdf", media_type='application/pdf', filename="esg_report.pdf")
    except Exception as e:
        raise HTTPException(500, str(e))

@app.post("/extract_from_file")
async def extract_from_file(files: List[UploadFile] = File(...)):
    combined_data = {
        "company_profile": {"industry": "IT/Services", "annual_revenue_inr": 0, "total_employees": 0},
        "environmental": {"total_energy_consumption_kwh": 0, "renewable_energy_kwh": 0, "total_water_consumption_liters": 0, "waste_generated_kg": 0, "waste_recycled_kg": 0},
        "social": {"female_employees": 0, "employees_with_disabilities": 0, "safety_accidents_count": 0, "employees_trained_count": 0, "complaints_received_sexual_harassment": 0},
        "governance": {"has_sustainability_committee": False, "regulatory_fines_paid_inr": 0, "policies_implemented": []}
    }
    
    for file in files:
        content = await file.read()
        extracted = parse_document(content, file.filename)
        
        # Simple Merge Logic
        if 'annual_revenue_inr' in extracted: combined_data['company_profile']['annual_revenue_inr'] = extracted['annual_revenue_inr']
        if 'total_employees' in extracted: combined_data['company_profile']['total_employees'] = extracted['total_employees']
        if 'industry' in extracted: combined_data['company_profile']['industry'] = extracted['industry']
        if 'total_energy_consumption_kwh' in extracted: combined_data['environmental']['total_energy_consumption_kwh'] = extracted['total_energy_consumption_kwh']
        
    return combined_data