import math


def expected_score(rating_a: float, rating_b: float) -> float:
    """
    Ожидаемый счёт игрока A против B по формуле ELO.
    """
    return 1 / (1 + math.pow(10, (rating_b - rating_a) / 400))


def update_elo(rating_a: float, rating_b: float, score_a: float, k: float = 32.0):
    """
    Обновление рейтинга двух игроков.
    score_a: фактический результат игрока A (1 = победа, 0.5 = ничья, 0 = поражение).
    Возвращает (new_rating_a, new_rating_b).
    """
    expected_a = expected_score(rating_a, rating_b)
    expected_b = expected_score(rating_b, rating_a)

    new_a = rating_a + k * (score_a - expected_a)
    new_b = rating_b + k * ((1 - score_a) - expected_b)

    return new_a, new_b
