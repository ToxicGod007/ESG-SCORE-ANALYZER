const { spawn } = require('child_process');
const path = require('path');
const Report = require('../models/Report'); // Changed from EsgReport

exports.analyzeESG = async (req, res) => {
    try {
        const userData = req.body;
        const pythonScriptPath = path.join(__dirname, '../scripts/esg_analyzer.py');
        const pythonProcess = spawn('python3', [pythonScriptPath]);

        pythonProcess.stdin.write(JSON.stringify(userData));
        pythonProcess.stdin.end();

        let scriptData = "";
        pythonProcess.stdout.on('data', (data) => { scriptData += data.toString(); });

        pythonProcess.on('close', async (code) => {
            if (code !== 0) return res.status(500).json({ success: false, error: 'Python Failed' });

            const aiResult = JSON.parse(scriptData);

            // Save using the updated Report model
            const savedReport = await Report.create({
                company_name: userData.companyName,
                industry: userData.industry,
                total_esg_score: aiResult.totalEsgScore,
                input_metrics: userData, // Stores all 16 data points
                ai_recommendations: aiResult.aiAnalysis
            });

            res.json({ success: true, report: savedReport });
        });
    } catch (err) {
        res.status(500).json({ success: false, error: err.message });
    }
};
