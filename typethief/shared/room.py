# typethief/shared/room.py

import threading
from collections import defaultdict

import pygame
from .clock import Clock
from .player import Player
from .text import Text


class Room(object):
    """
    Represents the state of a single game
    """
    STATES = set(['waiting', 'playing', 'finished'])
    _next_room = 0

    def __init__(self, encoded=None):
        self._state_mutex = threading.Lock()

        if encoded:
            self.decode(encoded)
            return

        self._text = Text()
        self._players = defaultdict(lambda: None)
        self._room_id = Room._new_room_id()
        self._clock = Clock()
        self._state = 'waiting'

    def encode(self):
        encoded_players = {k: v.encode() for k, v in self._players.items()}
        return {
            'text': self._text.encode(),
            'players': encoded_players,
            'id': self._room_id,
            'time': self._clock.epoch,
            'state': self._state,
        }

    def decode(self, encoded):
        self._text = Text(encoded=encoded['text'])
        self._players = defaultdict(
            lambda: None,
            {k: Player(encoded=v) for k, v in encoded['players'].items()},
        )
        self._room_id = encoded['id']
        self._clock = Clock(epoch=encoded['time'])
        self._state = encoded['state']

    @property
    def text(self):
        return self._text

    @property
    def id(self):
        return self._room_id

    @property
    def time(self):
        return self._clock.time

    @property
    def state(self):
        # if there is no next char, then finished
        return self._state if self._text.next_char else 'finished'

    @property
    def size(self):
        return len(self._players)

    def __iter__(self):
        for p in self._players.values():
            yield p

    @property
    def winner(self):
        players = self._players.values()
        winner = players[0]
        for p in players:
            if p and p.score > winner.score:
                winner = p
        return winner

    @state.setter
    def state(self, new_state):
        if new_state not in Room.STATES:
            raise Exception('{} is not a valid state'.format(new_state))
        self._state = new_state

    @classmethod
    def _new_room_id(cls):
        room_id = 'room' + str(cls._next_room)
        cls._next_room += 1
        return room_id

    def empty(self):
        return len(self._players) == 0

    def get_player(self, player_id):
        return self._players[player_id]

    def add_player(self, player):
        self._players[player.id] = player

    def remove_player(self, player_id):
        del self._players[player_id]
