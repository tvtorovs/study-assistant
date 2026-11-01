from sqlmodel import *
from fastapi import *
import datetime as dt
from contextlib import asynccontextmanager

# ----------------------------------------------------------------------------------------------
# Collection of all study session attributes
class StudyBase(SQLModel):
    module: str
    topic: str
    minutes: int
    date: dt.date = Field(default_factory=dt.date.today)
    notes: str = ""

# DB table of study session and id, such that the id cannot be changed by the client.
class StudySession(StudyBase, table = True):
    id: int | None = Field(default=None, primary_key=True)

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield 

app = FastAPI(lifespan=lifespan) 

# ----------------------------------------------------------------------------------------------

@app.post("/sessions", response_model=StudySession, status_code=201)
def create_session(data: StudyBase, db: Session = Depends(get_session)):
    sess = StudySession.model_validate(data)
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return sess

@app.get("/sessions", response_model=list[StudySession])
def get_sessions(db: Session = Depends(get_session)):
    return db.exec(select(StudySession)).all()
