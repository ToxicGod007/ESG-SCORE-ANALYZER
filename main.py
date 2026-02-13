from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import esg_engine  # This imports your existing logic

app = FastAPI()

# Allow your React app to talk to this Python server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/esg-score")
async def get_score():
    # Call your actual AI function from esg_engine.py
    # Example: result = esg_engine.analyze_data()
    return {
        "overall": 74,
        "breakdown": {"E": 65, "S": 82, "G": 74},
        "actions": [
            "Implement LED lighting",
            "Draft community policy",
            "Establish audit committee"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
