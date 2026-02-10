from typing import List

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

from sqlalchemy.orm import Session

from app.database import init_db, get_db
from app.models import User, Rating, Match, RatingHistory
from app.elo import update_elo

app = FastAPI()

# --- CORS (для Mini App) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для dev; на Amvera заменим на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.on_event("startup")
def on_startup():
    # Инициализация БД при старте приложения
    init_db()


@app.get("/")
async def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(index_path)


# --------- Pydantic-модели для API ---------

class GameResult(BaseModel):
    player_score: int = Field(..., ge=0)
    opponent_score: int = Field(..., ge=0)


class MatchResult(BaseModel):
    player_tg_id: int
    player_username: str
    opponent_username: str
    games: List[GameResult]
    player_rating_before: int
    player_rating_after: int
    rating_delta: int


# --------- Вспомогательные функции ---------

def get_or_create_user(db: Session, tg_id: int, username: str) -> User:
    user = None
    if tg_id:
        user = db.query(User).filter(User.tg_id == tg_id).first()
    if not user and username:
        user = db.query(User).filter(User.username == username).first()

    if not user:
        user = User(tg_id=tg_id or None, username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

    # Убедимся, что у юзера есть Rating
    if not user.rating:
        rating = Rating(user_id=user.id, current_rating=1000.0)
        db.add(rating)
        db.commit()
        db.refresh(rating)

    return user


def get_or_create_user_by_username(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)

        rating = Rating(user_id=user.id, current_rating=1000.0)
        db.add(rating)
        db.commit()
        db.refresh(rating)

    return user


# --------- API: приём матча, расчёт ELO и сохранение ---------

@app.post("/api/matches")
async def create_match(result: MatchResult, db: Session = Depends(get_db)):
    # 1. Игрок и соперник
    player = get_or_create_user(db, tg_id=result.player_tg_id, username=result.player_username)
    opponent = get_or_create_user_by_username(db, username=result.opponent_username)

    # 2. Текущие рейтинги
    player_rating_obj = player.rating
    opponent_rating_obj = opponent.rating

    rating_a = float(player_rating_obj.current_rating)
    rating_b = float(opponent_rating_obj.current_rating)

    # 3. Фактический результат по геймам
    player_games_won = 0
    opponent_games_won = 0

    for g in result.games:
        if g.player_score > g.opponent_score:
            player_games_won += 1
        elif g.player_score < g.opponent_score:
            opponent_games_won += 1

    if player_games_won > opponent_games_won:
        score_a = 1.0
    elif player_games_won < opponent_games_won:
        score_a = 0.0
    else:
        score_a = 0.5  # теоретическая ничья

    # 4. ELO
    new_rating_a, new_rating_b = update_elo(rating_a, rating_b, score_a, k=32.0)

    # 5. Сохраняем матч
    match = Match(
        player1_id=player.id,
        player2_id=opponent.id,
        player1_score=player_games_won,
        player2_score=opponent_games_won,
    )
    db.add(match)
    db.commit()
    db.refresh(match)

    # 6. История рейтинга
    player_history = RatingHistory(
        user_id=player.id,
        match_id=match.id,
        old_rating=rating_a,
        new_rating=new_rating_a,
        delta=new_rating_a - rating_a,
    )
    opponent_history = RatingHistory(
        user_id=opponent.id,
        match_id=match.id,
        old_rating=rating_b,
        new_rating=new_rating_b,
        delta=new_rating_b - rating_b,
    )
    db.add_all([player_history, opponent_history])

    # 7. Обновляем текущие рейтинги
    player_rating_obj.current_rating = new_rating_a
    opponent_rating_obj.current_rating = new_rating_b

    db.commit()

    return {
        "status": "ok",
        "player": {
            "username": player.username,
            "old_rating": rating_a,
            "new_rating": new_rating_a,
            "delta": new_rating_a - rating_a,
        },
        "opponent": {
            "username": opponent.username,
            "old_rating": rating_b,
            "new_rating": new_rating_b,
            "delta": new_rating_b - rating_b,
        },
    }
