desi-food-puch/
│
├── backend/
│   ├── app.js                 # Express/Flask entry point
│   ├── routes/
│   │   ├── recipes.js         # Handles recipe fetch requests
│   │   ├── locality.js        # Handles locality queries
│   ├── controllers/
│   │   ├── recipeController.js
│   │   ├── localityController.js
│   ├── services/
│   │   ├── recipeService.js   # API calls / DB fetch for recipes
│   │   ├── localityService.js # Google Places API calls
│   ├── utils/
│   │   ├── formatter.js       # For clean WhatsApp messages
│   │   ├── recommender.js     # Recommendation logic
│   ├── data/
│   │   ├── recipes.db         # SQLite / CSV dataset
│   │   ├── mappings.json      # Dish → famous region mapping
│   ├── tests/
│   │   ├── recipe.test.js
│   ├── package.json
│
├── docs/
│   ├── README.md              # Main hackathon documentation
│   ├── API_REFERENCE.md       # Endpoint details
│   ├── ROADMAP.md             # Development plan
│
├── scripts/
│   ├── seedData.js            # For populating DB
│   ├── testBot.js             # For local WhatsApp simulation
│
├── .env.example               # Example env vars (API keys, DB path)
├── Dockerfile
├── docker-compose.yml
├── LICENSE
└── README.md


---

Why This Works
Separation of concerns — Each logic part is in its own layer (controllers, services, utils)

Scalable — Easy to add new modules (nutrition info, festival dishes, etc.)

Hackathon-friendly — You can skip writing heavy tests now but keep folders ready for later

Documentation ready — Judges love a clean repo