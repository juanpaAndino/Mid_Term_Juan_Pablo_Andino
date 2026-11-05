from typing import Optional, List
import random
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine, select

sqlite_url = "sqlite:///streaming.db"
engine = create_engine(sqlite_url, echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

class Video(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str
    video_url: str
    thumbnail_url: str

    comments: List["Comment"] = Relationship(back_populates="video")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: str
    content: str
    video_id: int = Field(foreign_key="video.id")

    video: Optional[Video] = Relationship(back_populates="comments")

app = FastAPI(
    title="Streaming API",
    description="API de plataforma de videos con FastAPI, S3 y SQLModel",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

S3_VIDEOS = "https://s3.us-east-2.amazonaws.com/media3.3/Videos/"
S3_IMAGENES = "https://s3.us-east-2.amazonaws.com/media3.3/Imagenes/"

def cargar_videos_iniciales():
    with Session(engine) as session:
        existentes = session.exec(select(Video)).all()
        for v in existentes:
            session.delete(v)
        session.commit()

        videos_s3 = [
            Video(
                title="Amanecer en el Horizonte",
                description="Vista cinematografica del amanecer en alta definicion.",
                category="Naturaleza",
                video_url=S3_VIDEOS + "152174-802335605_medium.mp4",
                thumbnail_url=S3_IMAGENES + "datn-dawn-10521445_1920.jpg"
            ),
            Video(
                title="Bosque de Otono",
                description="Recorrido visual por senderos rodeados de hojas de otono.",
                category="Naturaleza",
                video_url=S3_VIDEOS + "270941_medium.mp4",
                thumbnail_url=S3_IMAGENES + "fietzfotos-autumn-10545288_1920.jpg"
            ),
            Video(
                title="Paisaje de Montana",
                description="Panoramica natural de montanas y valles abiertos.",
                category="Paisajes",
                video_url=S3_VIDEOS + "307130_medium.mp4",
                thumbnail_url=S3_IMAGENES + "fietzfotos-landscape-10541588_1920.jpg"
            ),
            Video(
                title="Naturaleza Salvaje",
                description="Exploracion de ecosistemas naturales en estado puro.",
                category="Naturaleza",
                video_url=S3_VIDEOS + "325636_medium.mp4",
                thumbnail_url=S3_IMAGENES + "kodl68-nature-10267644_1920.jpg"
            ),
            Video(
                title="Reflejos en el Lago",
                description="Aguas tranquilas reflejando el paisaje al atardecer.",
                category="Paisajes",
                video_url=S3_VIDEOS + "327388_medium.mp4",
                thumbnail_url=S3_IMAGENES + "leolo212-lake-10416643_1920.jpg"
            ),
            Video(
                title="Cascada Cristalina",
                description="Caida de agua natural en medio de la vegetacion.",
                category="Paisajes",
                video_url=S3_VIDEOS + "353078_medium.mp4",
                thumbnail_url=S3_IMAGENES + "suju-foto-waterfall-10541967_1920.jpg"
            ),
            Video(
                title="Rio entre las Rocas",
                description="Corriente de agua fluyendo por el canon natural.",
                category="Paisajes",
                video_url=S3_VIDEOS + "359930_medium.mp4",
                thumbnail_url=S3_IMAGENES + "suju-foto-waterfall-10541974_1920.jpg"
            ),
            Video(
                title="Cielo Nocturno Estrellado",
                description="Timelapse del firmamento durante una noche despejada.",
                category="Nocturno",
                video_url=S3_VIDEOS + "363550_medium.mp4",
                thumbnail_url=S3_IMAGENES + "tama66-night-sky-10506842_1920.jpg"
            ),
            Video(
                title="Atardecer Dorado",
                description="Colores calidos del sol ocultandose en el horizonte.",
                category="Nocturno",
                video_url=S3_VIDEOS + "365737_medium.mp4",
                thumbnail_url=S3_IMAGENES + "xiserge-sunset-10543299_1920.jpg"
            ),
            Video(
                title="Vuelo de Aves",
                description="Aves silvestres sobrevolando su habitat natural.",
                category="Animales",
                video_url=S3_VIDEOS + "370344_medium.mp4",
                thumbnail_url=S3_IMAGENES + "jsachs99-birds-10482068_1920.jpg"
            ),
            Video(
                title="Mirada Felina",
                description="Primer plano detallado del comportamiento de un gato.",
                category="Animales",
                video_url=S3_VIDEOS + "370702_medium.mp4",
                thumbnail_url=S3_IMAGENES + "schwarzwaldandi-cat-5665915_1920.jpg"
            ),
            Video(
                title="Lobo en el Bosque",
                description="Documental corto sobre el lobo en su territorio.",
                category="Animales",
                video_url=S3_VIDEOS + "370958_medium.mp4",
                thumbnail_url=S3_IMAGENES + "schwarzwaldandi-wolf-10522660_1920.jpg"
            ),
            Video(
                title="Aguila Real en las Alturas",
                description="Majestuoso vuelo del aguila cazando en las montanas.",
                category="Animales",
                video_url=S3_VIDEOS + "371424_medium.mp4",
                thumbnail_url=S3_IMAGENES + "suju-foto-bald-eagle-10502248_1920.jpg"
            ),
            Video(
                title="Trabajo en Equipo",
                description="Escenas cotidianas de trabajo y oficio tradicional.",
                category="Cultura",
                video_url=S3_VIDEOS + "382582_medium.mp4",
                thumbnail_url=S3_IMAGENES + "careofchinmoy-workers-10540191_1920.jpg"
            ),
            Video(
                title="Luces de Invierno",
                description="Ambiente festivo y decoracion luminosa nocturna.",
                category="Cultura",
                video_url=S3_VIDEOS + "383541_medium.mp4",
                thumbnail_url=S3_IMAGENES + "studiofriluma-christmas-10521175_1920.jpg"
            ),
            Video(
                title="Tradicion de Otono",
                description="Colores y cosecha tradicional de temporada.",
                category="Cultura",
                video_url=S3_VIDEOS + "384550_medium.mp4",
                thumbnail_url=S3_IMAGENES + "suju-foto-pumpkin-10520325_1920.jpg"
            )
        ]

        session.add_all(videos_s3)
        session.commit()

@app.on_event("startup")
def startup():
    create_db()
    cargar_videos_iniciales()

@app.get("/api/videos")
def get_videos(category: Optional[str] = None, session: Session = Depends(get_session)):
    statement = select(Video)
    if category:
        statement = statement.where(Video.category == category)
    return session.exec(statement).all()

@app.get("/api/categories")
def get_categories(session: Session = Depends(get_session)):
    videos = session.exec(select(Video)).all()
    categorias = sorted(list(set(v.category for v in videos)))
    return categorias

@app.get("/api/videos/recommendations/{category}")
def get_recommendations(
    category: str,
    exclude_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    todos = session.exec(select(Video)).all()
    disponibles = [v for v in todos if v.id != exclude_id]

    misma_categoria = [v for v in disponibles if v.category == category]
    otras_categorias = [v for v in disponibles if v.category != category]

    random.shuffle(misma_categoria)
    random.shuffle(otras_categorias)

    combinados = misma_categoria + otras_categorias
    return combinados[:10]

@app.get("/api/videos/{video_id}")
def get_video(video_id: int, session: Session = Depends(get_session)):
    video = session.get(Video, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video no encontrado")
    return video

@app.post("/api/videos")
def create_video(video: Video, session: Session = Depends(get_session)):
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

@app.get("/api/videos/{video_id}/comments")
def get_comments(video_id: int, session: Session = Depends(get_session)):
    statement = select(Comment).where(Comment.video_id == video_id)
    return session.exec(statement).all()

@app.post("/api/comments")
def create_comment(comment: Comment, session: Session = Depends(get_session)):
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment