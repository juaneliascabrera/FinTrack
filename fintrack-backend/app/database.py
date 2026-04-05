from sqlmodel import create_engine, SQLModel, Session

# En un paso siguiente usaremos .env, pero por ahora usemos la URL directa
# postgresql://usuario:contraseña@localhost:puerto/nombre_db
DATABASE_URL = "postgresql://heroe_user:heroe_password@localhost:5432/heroes_database"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    # Esta función le dice a Postgres: "Mirá mis modelos y creá las tablas"
    SQLModel.metadata.create_all(engine)

def get_session():
    # Este es el "generador" de grifos (sesiones)
    with Session(engine) as session:
        yield session