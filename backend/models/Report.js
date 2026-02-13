const { DataTypes } = require('sequelize');
const sequelize = require('../config/database');

const Report = sequelize.define('Report', {
    company_name: { type: DataTypes.STRING, allowNull: false },
    industry: { type: DataTypes.STRING, allowNull: false },
    // Storing all 16 metrics in one JSONB column for easier handling
    input_metrics: { type: DataTypes.JSONB, allowNull: false }, 
    total_esg_score: { type: DataTypes.FLOAT },
    ai_recommendations: { type: DataTypes.JSONB }
});

module.exports = Report;
