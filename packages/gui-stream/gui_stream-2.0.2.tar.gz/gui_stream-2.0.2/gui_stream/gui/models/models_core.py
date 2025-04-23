#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod

# Sujeito
class ABCNotifyProvider(ABC):
    def __init__(self):
        self._observer_list: List[ABCObserver] = []
        self.num_observers: int = 0

    def add_observer(self, observer: ABCObserver):
        self._observer_list.append(observer)
        self.num_observers += 1
        print(f'Obsevador adicionado: {self.num_observers}')

    def remove_observer(self, observer: ABCObserver):
        if len(self._observer_list) < 1:
            return
        self._observer_list.remove(observer)
        self.num_observers -= 1
        
    def clear(self):
        self._observer_list.clear()
        self.num_observers = 0

    @abstractmethod
    def notify_all(self):
        for obs in self._observer_list:
            obs.update_notify(self)

# Observador
class ABCObserver(ABC):
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def update_notify(self, notify_provide: ABCNotifyProvider=None):
        """Receber atualizações."""
        pass

 