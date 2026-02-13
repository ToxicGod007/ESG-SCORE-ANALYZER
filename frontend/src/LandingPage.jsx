import React from 'react';
import { 
  BarChart3, 
  ShieldCheck, 
  Leaf, 
  ArrowRight, 
  CheckCircle2, 
  Menu,
  Globe,
  Zap
} from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-white font-sans text-slate-900">
      
      {/* Navigation */}
      <nav className="sticky top-0 z-50 w-full border-b border-slate-100 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div className="flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-600 text-white shadow-lg shadow-emerald-200">
              <Leaf size={22} fill="currentColor" />
            </div>
            <span className="text-xl font-bold tracking-tight text-slate-900">EcoMetric<span className="text-emerald-600">AI</span></span>
          </div>
          
          <div className="hidden md:flex items-center gap-8">
            <a href="#features" className="text-sm font-semibold text-slate-600 hover:text-emerald-600 transition-colors">Features</a>
            <a href="#compliance" className="text-sm font-semibold text-slate-600 hover:text-emerald-600 transition-colors">Frameworks</a>
            <button className="rounded-full bg-slate-900 px-6 py-2.5 text-sm font-bold text-white transition-all hover:bg-emerald-600 hover:scale-105">
              Launch App
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-20 pb-32 overflow-hidden">
        <div className="mx-auto max-w-7xl px-6 relative z-10">
          <div className="text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center rounded-full border border-emerald-100 bg-emerald-50 px-4 py-1.5 text-sm font-bold text-emerald-700 mb-8 animate-fade-in">
              <Zap size={14} className="mr-2 fill-emerald-600" />
              v8 Experimental Engine Enabled
            </div>
            <h1 className="text-5xl font-black tracking-tight text-slate-900 sm:text-7xl mb-8 leading-[1.1]">
              ESG Analysis. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-600 to-teal-500">
                Driven by AI.
              </span>
            </h1>
            <p className="text-xl text-slate-600 mb-12 leading-relaxed max-w-2xl mx-auto">
              Transform raw operational data into standardized ESG scores. Built for SMEs to meet BRSR and GRI compliance in minutes, not months.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
              <button 
                className="group w-full sm:w-auto px-10 py-5 rounded-2xl bg-emerald-600 text-white font-bold text-lg shadow-2xl shadow-emerald-200 hover:bg-emerald-700 hover:-translate-y-1 transition-all flex items-center justify-center gap-3"
              >
                Analyze My Score 
                <ArrowRight size={20} className="group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="w-full sm:w-auto px-10 py-5 rounded-2xl bg-white border-2 border-slate-100 text-slate-700 font-bold text-lg hover:bg-slate-50 transition-all">
                View Documentation
              </button>
            </div>
          </div>
        </div>

        {/* Background Visuals */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10">
          <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-emerald-50 rounded-full blur-[120px] opacity-60"></div>
          <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-blue-50 rounded-full blur-[120px] opacity-60"></div>
        </div>
      </section>

      {/* Feature Section */}
      <section id="features" className="py-24 bg-slate-50">
        <div className="mx-auto max-w-7xl px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="bg-white p-10 rounded-3xl shadow-sm border border-slate-100 hover:shadow-xl transition-shadow">
              <div className="h-14 w-14 rounded-2xl bg-emerald-100 text-emerald-600 flex items-center justify-center mb-8">
                <BarChart3 size={28} />
              </div>
              <h3 className="text-2xl font-bold mb-4">Real-time Scoring</h3>
              <p className="text-slate-600 leading-relaxed">
                Our backend engine processes your CSV or manual inputs to provide instant Environmental, Social, and Governance ratings.
              </p>
            </div>

            <div className="bg-white p-10 rounded-3xl shadow-sm border border-slate-100 hover:shadow-xl transition-shadow">
              <div className="h-14 w-14 rounded-2xl bg-blue-100 text-blue-600 flex items-center justify-center mb-8">
                <ShieldCheck size={28} />
              </div>
              <h3 className="text-2xl font-bold mb-4">Compliance First</h3>
              <p className="text-slate-600 leading-relaxed">
                Mapped directly to global reporting initiatives, ensuring your SME is always ready for investor audits and government checks.
              </p>
            </div>

            <div className="bg-white p-10 rounded-3xl shadow-sm border border-slate-100 hover:shadow-xl transition-shadow">
              <div className="h-14 w-14 rounded-2xl bg-purple-100 text-purple-600 flex items-center justify-center mb-8">
                <Globe size={28} />
              </div>
              <h3 className="text-2xl font-bold mb-4">Actionable Insights</h3>
              <p className="text-slate-600 leading-relaxed">
                Don't just see a score—get AI-generated steps to improve your sustainability standing and reduce operational costs.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Banner */}
      <div className="py-12 border-y border-slate-100">
        <div className="mx-auto max-w-7xl px-6 flex flex-wrap justify-center items-center gap-12 opacity-40 grayscale">
          <span className="text-2xl font-black">GRI STANDARDS</span>
          <span className="text-2xl font-black">BRSR READY</span>
          <span className="text-2xl font-black">ISO 14001</span>
          <span className="text-2xl font-black">SDG ALIGNED</span>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-12 bg-white">
        <div className="mx-auto max-w-7xl px-6 text-center">
          <p className="text-slate-400 text-sm font-medium">
            Developed for Sustainable Enterprise Compliance • Project ID: HSUST004
          </p>
        </div>
      </footer>

    </div>
  );
};

export default LandingPage;