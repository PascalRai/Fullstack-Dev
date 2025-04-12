from app.database.database import engine, Base

def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")