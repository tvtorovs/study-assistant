from sqlmodel import *
from fastapi import *
from fastapi.middleware.cors import CORSMiddleware
import datetime as dt
from contextlib import asynccontextmanager

# This is the ONLY backend file. It has all the backend logic. 

# ----------------------------------------------------------------------------------------------
# This section is all the Database models.


# Collection of all study session attributes
class StudyBase(SQLModel):
    module: str = Field(min_length=1, max_length=20)
    topic: str = Field(min_length=1, max_length=50)
    minutes: int = Field(gt=0, le=1440)
    date: dt.date = Field(default_factory=dt.date.today)
    notes: str = Field(default="", max_length=500)

# DB table of study session and id, such that the id cannot be changed by the client.
class StudySession(StudyBase, table = True):
    id: int | None = Field(default=None, primary_key=True)

#Collection of modules with the total time studied across all sessions.
class ModuleStats(SQLModel):
    module: str 
    hours: float

# ----------------------------------------------------------------------------------------------

# Initialises DB environment
engine = create_engine("sqlite:///study.db", echo=True)

# Creates all DB tables specified above
def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# ----------------------------------------------------------------------------------------------

# no clue what this does i lowkey forgot
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield 

app = FastAPI(lifespan=lifespan) 

# CORS - ensures requests to and from frontend are not blocked by browser. 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------------------------------
# All endpoints are below

# POST endpoint
@app.post("/sessions", response_model=StudySession, status_code=201)
def create_session(data: StudyBase, db: Session = Depends(get_session)):
    sess = StudySession.model_validate(data)
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess

# GET endpoint for sessions
@app.get("/sessions", response_model=list[StudySession])
def get_sessions(module: str | None = None, db: Session = Depends(get_session)):
    query = select(StudySession)
    if module:
        query = query.where(StudySession.module == module)
    return db.exec(query).all()

# GET endpoint for modules
@app.get("/modules", response_model=list[str])
def get_modules(db: Session = Depends(get_session)):
    return db.exec(select(StudySession.module).distinct().order_by(StudySession.module)).all()

# GET endpoint for module stats 
@app.get("/stats", response_model=list[ModuleStats])
def get_stats(db: Session = Depends(get_session)):
    query = (select(StudySession.module, func.sum(StudySession.minutes)).group_by(StudySession.module).order_by(StudySession.module))
    rows = db.exec(query).all()
    return [ModuleStats(module=m, hours=round(total / 60, 2)) for m, total in rows]

# UPDATE endpoint
@app.put("/sessions/{session_id}", response_model=StudySession)
def update_session(session_id: int, data: StudyBase, db:Session = Depends(get_session)):
    sess = db.get(StudySession, session_id)
    if sess is None:
        raise HTTPException(status_code=404, detail="Session not found")
    sess.sqlmodel_update(data.model_dump())
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess

# DEL endpoint
@app.delete("/sessions/{session_id}", status_code=204)
def delete_session(session_id: int, db: Session = Depends(get_session)):
    sess = db.get(StudySession, session_id)
    if sess is None:
        raise HTTPException(status_code=404, detail="Session not found")
    db.delete(sess)
    db.commit()