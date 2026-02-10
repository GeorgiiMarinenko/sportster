// Инициализация Telegram WebApp
let tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;

if (tg) {
  tg.expand();
}

let rating = 1000;
let wins = 0;
let losses = 0;
let games = [];
let opponentUsername = null;

const ratingSpan = document.getElementById("rating");
const winsSpan = document.getElementById("wins");
const lossesSpan = document.getElementById("losses");

const startMatchBtn = document.getElementById("start-match-btn");
const matchSection = document.getElementById("match-section");
const opponentInput = document.getElementById("opponent-username");
const findOpponentBtn = document.getElementById("find-opponent-btn");

const gameScoreSection = document.getElementById("game-score-section");
const currentGameNumberSpan = document.getElementById("current-game-number");
const playerScoreInput = document.getElementById("player-score");
const opponentScoreInput = document.getElementById("opponent-score");
const addGameBtn = document.getElementById("add-game-btn");
const gamesList = document.getElementById("games-list");
const finishMatchBtn = document.getElementById("finish-match-btn");

const resultSection = document.getElementById("result-section");
const resultSummaryP = document.getElementById("result-summary");
const ratingChangeP = document.getElementById("rating-change");

// Обновление UI статистики
function updateStats() {
  ratingSpan.textContent = Math.round(rating);
  winsSpan.textContent = wins;
  lossesSpan.textContent = losses;
}

// Старт матча
startMatchBtn.addEventListener("click", () => {
  matchSection.style.display = "block";
  resultSection.style.display = "none";
});

// Поиск соперника (пока просто проверяем, что ник введён)
findOpponentBtn.addEventListener("click", () => {
  const value = opponentInput.value.trim();
  if (!value || !value.startsWith("@")) {
    alert("Укажи ник соперника в формате @username");
    return;
  }
  opponentUsername = value;
  alert(`Соперник ${opponentUsername} найден (пока только локально).`);
  gameScoreSection.style.display = "block";
});

// Добавление гейма
addGameBtn.addEventListener("click", () => {
  const playerScore = parseInt(playerScoreInput.value, 10);
  const opponentScore = parseInt(opponentScoreInput.value, 10);

  if (Number.isNaN(playerScore) || Number.isNaN(opponentScore)) {
    alert("Заполни очки обоих игроков.");
    return;
  }

  games.push({ playerScore, opponentScore });

  const li = document.createElement("li");
  li.textContent = `Гейм ${games.length}: ${playerScore} : ${opponentScore}`;
  gamesList.appendChild(li);

  playerScoreInput.value = "";
  opponentScoreInput.value = "";
  currentGameNumberSpan.textContent = games.length + 1;
});

// Завершение матча
finishMatchBtn.addEventListener("click", async () => {
  if (games.length === 0) {
    alert("Добавь хотя бы один гейм.");
    return;
  }

  let playerGamesWon = 0;
  let opponentGamesWon = 0;

  games.forEach((g) => {
    if (g.playerScore > g.opponentScore) {
      playerGamesWon += 1;
    } else if (g.playerScore < g.opponentScore) {
      opponentGamesWon += 1;
    }
  });

  let resultText;

  if (playerGamesWon > opponentGamesWon) {
    resultText = `Ты победил(а) ${opponentUsername} по геймам ${playerGamesWon}:${opponentGamesWon}`;
    wins += 1;
  } else if (playerGamesWon < opponentGamesWon) {
    resultText = `Ты проиграл(а) ${opponentUsername} по геймам ${playerGamesWon}:${opponentGamesWon}`;
    losses += 1;
  } else {
    resultText = `Ничья по геймам ${playerGamesWon}:${opponentGamesWon}`;
  }

  resultSummaryP.textContent = resultText;

  // --- Подготовка данных для API ---
  let playerTgId = null;
  let playerUsername = null;

  if (tg && tg.initDataUnsafe && tg.initDataUnsafe.user) {
    playerTgId = tg.initDataUnsafe.user.id;
    playerUsername = tg.initDataUnsafe.user.username || "";
  }

  const payload = {
    player_tg_id: playerTgId || 0,
    player_username: playerUsername || "unknown",
    opponent_username: opponentUsername || "unknown",
    games: games.map((g) => ({
      player_score: g.playerScore,
      opponent_score: g.opponentScore,
    })),
    player_rating_before: Math.round(rating),
    player_rating_after: Math.round(rating), // сервер посчитает по-своему
    rating_delta: 0,
  };

  try {
    const response = await fetch("/api/matches", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      console.error("Ошибка сохранения матча:", await response.text());
      alert("Не удалось сохранить матч на сервере. Смотри логи backend.");
    } else {
      const data = await response.json();
      const delta = data.player.delta;
      rating = data.player.new_rating;

      ratingChangeP.textContent = `Изменение рейтинга: ${delta >= 0 ? "+" : ""}${delta.toFixed(
        1
      )}`;
      updateStats();
    }
  } catch (e) {
    console.error("Ошибка сети при сохранении матча:", e);
    alert("Ошибка сети при сохранении матча.");
  }

  resultSection.style.display = "block";

  // Обнуляем данные матча
  games = [];
  gamesList.innerHTML = "";
  currentGameNumberSpan.textContent = "1";
  matchSection.style.display = "none";
});

// Инициализация статистики
updateStats();
