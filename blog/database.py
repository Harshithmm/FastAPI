from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:8197696508@localhost:5432/blog_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()








# The future=True parameter is used to enable SQLAlchemy 1.4's "2.0 style" usage which is a new way to use SQLAlchemy that's intended to be more straightforward and consistent. This is a transitional style that's intended to help prepare for SQLAlchemy 2.0, where it will be the default.

# In "2.0 style" usage, some methods work a bit differently. For example, the Session.execute() method is used for all SQL statement executions, and it returns a Result object that provides more capabilities and behaves more consistently across different types of statements.

# Here's an example of how you might use it:

# from sqlalchemy import text

# with Session(engine, future=True) as session:
#     result = session.execute(text("SELECT * FROM users WHERE username = :username"), {"username": "alice"})
#     user = result.scalars().first()

# In this example, session.execute() is used to execute a raw SQL query, and result.scalars().first() is used to get the first row of the result set.

# If you're starting a new project or if you're willing to update your existing code, it's recommended to use future=True to take advantage of these improvements and prepare for SQLAlchemy 2.0. If you're maintaining an existing project and you don't want to change your existing code, you can omit future=True to use the traditional "1.x style" usage.