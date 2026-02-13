import json
import joblib
import pandas as pd
import numpy as np

class ESGCalculator:
    def __init__(self, data):
        self.data = data
        self.scores = {"environmental": 0, "social": 0, "governance": 0, "total": 0}
        self.recommendations = []
        
        # --- LOAD AI ---
        try:
            self.model = joblib.load('esg_benchmark_model.pkl')
            self.model_loaded = True
        except:
            print("WARNING: Model not found. Using fallbacks.")
            self.model_loaded = False

        self.industry_map = {
            "IT/Services": 0, "Manufacturing": 1, "Retail": 2, 
            "Cement/Steel": 3, "Pharma": 4
        }
        
        # Default Weights
        self.base_weights = {"E": 0.4, "S": 0.3, "G": 0.3}
        self._adjust_weights_for_industry()

    def _adjust_weights_for_industry(self):
        # Dynamic Weighting based on Industry Risk
        ind = self.data['company_profile']['industry']
        if ind in ["Cement/Steel", "Pharma"]:
            self.base_weights = {"E": 0.6, "S": 0.2, "G": 0.2}
        elif ind == "IT/Services":
            self.base_weights = {"E": 0.2, "S": 0.5, "G": 0.3}

    def _get_ai_benchmark(self, revenue, employees, industry_str):
        if not self.model_loaded: return max(1, revenue * 0.005)
        
        industry_code = self.industry_map.get(industry_str, 1)
        input_df = pd.DataFrame([[revenue, employees, industry_code]], 
                                columns=['revenue', 'employees', 'industry_type'])
        return max(1.0, self.model.predict(input_df)[0])

    def _calculate_environmental(self):
        env = self.data['environmental']
        prof = self.data['company_profile']
        score = 0
        
        # 1. AI Benchmark Efficiency
        predicted = self._get_ai_benchmark(prof['annual_revenue_inr'], prof['total_employees'], prof['industry'])
        actual = max(1, env['total_energy_consumption_kwh'])
        
        if actual <= predicted:
            score += 50
        else:
            excess = (actual - predicted) / predicted
            score += max(0, 50 * (1 - excess))
            if excess > 0.2:
                self.recommendations.append(f"High Energy Usage: {int(excess*100)}% above industry standard.")

        # 2. Renewables
        ren_pct = (env['renewable_energy_kwh'] / actual) * 100
        score += min(30, (ren_pct / 30) * 30)

        # 3. Waste
        gen = max(1, env['waste_generated_kg'])
        score += (env['waste_recycled_kg'] / gen) * 20
            
        self.scores['environmental'] = round(score, 2)

    def _calculate_social(self):
        soc = self.data['social']
        total_emp = max(1, self.data['company_profile']['total_employees'])
        score = 0
        
        # Diversity
        div_pct = (soc['female_employees'] / total_emp) * 100
        score += min(40, (div_pct / 40) * 40)
        
        # Safety (Critical)
        if soc['safety_accidents_count'] == 0: score += 30
        else: self.recommendations.append("CRITICAL: Safety accidents reported. Immediate audit required.")

        # Training
        train_pct = (soc['employees_trained_count'] / total_emp) * 100
        score += min(30, (train_pct / 50) * 30)

        self.scores['social'] = round(score, 2)

    def _calculate_governance(self):
        gov = self.data['governance']
        score = 0
        
        # Policies
        score += min(50, len(gov['policies_implemented']) * 15)
        
        # Fines
        if gov['regulatory_fines_paid_inr'] == 0: score += 30
        else: self.recommendations.append("Compliance Alert: Regulatory fines detected.")
        
        # Committee
        if gov['has_sustainability_committee']: score += 20
        
        self.scores['governance'] = round(score, 2)

    def compute(self):
        self._calculate_environmental()
        self._calculate_social()
        self._calculate_governance()
        
        w = self.base_weights
        final = (self.scores['environmental'] * w['E']) + \
                (self.scores['social'] * w['S']) + \
                (self.scores['governance'] * w['G'])
        
        # Re-normalize to 100 base
        total_weight = w['E'] + w['S'] + w['G']
        self.scores['total'] = round(final / total_weight, 2)
        
        return {"scores": self.scores, "recommendations": self.recommendations}