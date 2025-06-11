import threading
from collections import defaultdict
from typing import Callable, Any

class Event:
    """Base class for all events."""
    pass

class EventBus:
    """A simple, thread-safe event bus using the Pub/Sub pattern."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(EventBus, cls).__new__(cls)
                    cls._instance._subscribers = defaultdict(list)
        return cls._instance

    def subscribe(self, event_type: type, handler: Callable):
        """Subscribe a handler to an event type."""
        with self._lock:
            self._subscribers[event_type].append(handler)

    def publish(self, event: Event):
        """Publish an event to all subscribed handlers."""
        event_type = type(event)
        handlers = []
        with self._lock:
            # Copy handlers to allow modification during iteration
            handlers = self._subscribers[event_type][:]
        
        for handler in handlers:
            try:
                # Handlers are called in separate threads or via a thread pool
                # to avoid blocking the event bus. For now, calling directly.
                handler(event)
            except Exception as e:
                print(f"Error in event handler for {event_type.__name__}: {e}")

# Singleton instance
event_bus = EventBus() 