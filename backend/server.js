const express = require('express');
const path = require('path');
const engine = require('ejs-mate');
require('dotenv').config();
const ejsMate=require("ejs-mate");




// Import Database and Models
const sequelize = require('./config/database.js');
const EsgReport = require('./models/Report.js');

// Import Controller (Phase 3)
const esgController = require('./controllers/esgController.js');

const app = express();

// 1. EJS MATE SETUP
app.engine('ejs', engine); // Sets ejs-mate as the engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// 2. MIDDLEWARE
app.use(express.json()); // To parse JSON bodies
app.use(express.urlencoded({ extended: true })); // To parse form data
app.use(express.static(path.join(__dirname, 'public'))); // For CSS/JS files

// 3. ROUTES
// Homepage
app.get("/",(req,res)=>{
    res.send("root working");
});
app.get('/esg', (req, res) => {
    res.render('index.ejs'); // Renders views/index.ejs
});

// ESG Analysis API (Connects to Python Bridge)
app.post('/esg/analyze', esgController.analyzeESG);

// 4. DATABASE SYNC & SERVER START
// Using { alter: true } to update tables without deleting data
sequelize.sync({ alter: true })
    .then(() => {
        console.log('✅ PostgreSQL Connected via Sequelize');
        console.log('✅ Database & Tables Synced');
        
        const PORT = process.env.PORT || 3000;
        app.listen(PORT, () => {
            console.log(`🚀 Server running on http://localhost:${PORT}`);
        });
    })
    .catch(err => {
        console.error('❌ Database Sync Failed:', err.message);
    });
