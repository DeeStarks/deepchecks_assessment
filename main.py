from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from models import Alert, AlertType, InteractionType, session
from tasks import log_interaction_from_file


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/log")
async def log_interaction(file: UploadFile):
    log_interaction_from_file.delay((await file.read()).decode('utf-8'))
    return {"message": "Uploaded interactions are being logged"}


@app.get("/alerts")
async def get_alerts(
    interaction_id: int = None,
    interaction_type: InteractionType = None,
    alert_type: AlertType = None
):
    query = session.query(Alert)
    if interaction_id:
        query = query.filter(Alert.interaction_id == interaction_id)
    if interaction_type:
        query = query.filter(Alert.element == interaction_type)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    alerts = query.all()
    return {"alerts": [alert.__dict__ for alert in alerts]}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
