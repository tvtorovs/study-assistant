from sqlmodel import SQLModel, Field, create_engine
import datetime as dt

# Database Table for all logged study sessions
class StudySession(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    module: str
    topic: str
    minutes: int
    date: dt.date = Field(default_factory=dt.date.today)
    notes: str = ""

# Initialises DB environment
engine = create_engine("sqlite:///study.db", echo=True)

# Creates all DB tables specified above
def create_db():
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
    # creates test session to check parameters
    s = StudySession(module="CS001", topic="Object Oriented Programming", minutes = 30)
    print(s.id, s.date)


