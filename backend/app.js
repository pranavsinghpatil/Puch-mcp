// backend/app.js
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const recipeRoutes = require('./routes/recipe');
const localityRoutes = require('./routes/locality');
const recommendRoutes = require('./routes/recommend');

const app = express();
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/recipe', recipeRoutes);
app.use('/api/locality', localityRoutes);
app.use('/api/recommend', recommendRoutes);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`MCP Server running on port ${PORT}`));
