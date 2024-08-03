from fastapi import FastAPI

from typing import List

from models.models import Trade, User

app = FastAPI(
    title='Trading app'
)


USERS = [
    {'id': 1, 'role': 'admin', 'nickname': 'Vados'},
    {'id': 2, 'role': 'investor', 'nickname': 'Yasos'},
    {'id': 3, 'role': 'trader', 'nickname': 'Biba'},
]

TRADES = [
    {'id': 1, 'user_id': 2, 'currency': 'BTC', 'side': 'buy', 'price': 100, 'amount': 2.12},
    {'id': 2, 'user_id': 3, 'currency': 'BTC', 'side': 'sell', 'price': 200, 'amount': 2.12},
]


@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in USERS if user.get('id') == user_id]

@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return TRADES[offset:][:limit]

@app.post('/users/{user_id}')
def change_user_name(user_id: int, new_name: str):
    curr_user = list(filter(lambda user: user.get('id') == user_id, USERS))[0]
    curr_user['nickname'] = new_name
    return {'status': 200, 'data': curr_user}

@app.post('/trades')
def add_trades(trades: List[Trade]):
    TRADES.extend(trades)
    return {'status': 200, 'data': TRADES}
