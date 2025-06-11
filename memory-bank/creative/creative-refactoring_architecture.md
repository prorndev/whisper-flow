# Creative Phase: Refactoring Architecture

This document outlines the design decisions for the WhisperFlow refactoring task.

---

## 📌 CREATIVE PHASE START: Configuration System
**Date**: $(date)

### 1️⃣ PROBLEM
**Description**: The current configuration is hardcoded throughout the `whisper_flow.py` script. This makes it difficult to manage, update, and customize the application without modifying the source code. A centralized, user-friendly configuration system is needed.
**Requirements**:
- Externalize all configurable parameters (e.g., paths, hotkeys, performance settings).
- Use a human-readable format (e.g., YAML or TOML).
- Provide sensible default values.
- Implement validation to ensure configuration integrity.
- Easy to access configuration values throughout the application.
**Constraints**:
- Must be able to handle different data types (strings, integers, booleans, lists).
- Minimal performance overhead during application startup.

### 2️⃣ OPTIONS
**Option A**: YAML with Pydantic - Use a YAML file for configuration and Pydantic for data validation and settings management.
**Option B**: INI file with `configparser` - Use the standard library `configparser` for a simple, flat configuration structure.
**Option C**: JSON file with custom validation - Use a JSON file and write a custom validation schema and loader.

### 3️⃣ ANALYSIS
| Criterion       | A: YAML + Pydantic | B: INI + configparser | C: JSON + Custom |
|-----------------|--------------------|-----------------------|------------------|
| Readability     | ⭐⭐⭐⭐⭐         | ⭐⭐⭐⭐             | ⭐⭐⭐⭐          |
| Validation      | ⭐⭐⭐⭐⭐         | ⭐⭐                  | ⭐⭐               |
| Complexity      | ⭐⭐                 | ⭐⭐⭐                | ⭐⭐⭐⭐          |
_Requires dependency_ | _Low complexity_    | _High complexity_|
| Maintainability | ⭐⭐⭐⭐            | ⭐⭐⭐                | ⭐⭐               |
| Features        | ⭐⭐⭐⭐⭐         | ⭐⭐                  | ⭐⭐⭐             |
_(Typed, nested)_  | _(Flat, strings only)_| _(Nested)_          |

**Key Insights**:
- **YAML + Pydantic** offers the best combination of readability, powerful validation, and modern Python features (data classes). It handles nested structures and data types automatically. The only downside is a new dependency (`PyYAML` and `pydantic`).
- **INI + `configparser`** is simple and standard but is limited to flat structures and string values, requiring manual type conversion and more complex validation logic.
- **JSON + Custom** is flexible but requires significant effort to build and maintain a robust validation system, reinventing the wheel that Pydantic already provides.

### 4️⃣ DECISION
**Selected**: Option A: YAML with Pydantic.
**Rationale**: This approach provides the most robust, maintainable, and developer-friendly solution. Pydantic's data validation is a significant advantage that will prevent runtime errors and make the configuration system resilient. The added dependencies are justified by the substantial benefits.

### 5️⃣ IMPLEMENTATION NOTES
- Create a `config.yaml` file in the project root.
- Create a `config` module with a `settings.py` file.
- Inside `settings.py`, define Pydantic models that map to the structure of `config.yaml`.
- The main `Settings` model will load the YAML file and perform validation at startup.
- A singleton instance of the `Settings` object will be created and made available to the rest of the application to ensure consistent access to configuration.
- Add `PyYAML` and `pydantic` to `requirements.txt`.
---

## 📌 CREATIVE PHASE START: Component Communication
**Date**: $(date)

### 1️⃣ PROBLEM
**Description**: The current script uses global variables and direct function calls between different parts of the system (e.g., `on_press` directly calls `start_recording_logic`, which modifies global state). This creates tight coupling, making the code hard to test, maintain, and reason about. A more structured communication mechanism is needed.
**Requirements**:
- Decouple components from each other.
- Allow components to react to events without direct knowledge of the event source.
- Improve testability by allowing components to be tested in isolation.
- Provide a clear and centralized way to understand system-wide events.
**Constraints**:
- The mechanism should be thread-safe.
- Must not introduce significant performance bottlenecks, especially for real-time tasks like audio recording.

### 2️⃣ OPTIONS
**Option A**: Event Bus (Pub/Sub) - Implement a central event bus where components can publish events (e.g., `hotkey_pressed`, `recording_finished`) and other components can subscribe to these events.
**Option B**: Direct Dependency Injection - Components are explicitly given references to the other components they need to interact with. Communication happens via direct method calls.
**Option C**: Callbacks and Listeners - Use a more formal observer pattern where components explicitly register callback functions with other components.

### 3️⃣ ANALYSIS
| Criterion       | A: Event Bus (Pub/Sub) | B: Dependency Injection | C: Callbacks/Listeners |
|-----------------|------------------------|-------------------------|------------------------|
| Decoupling      | ⭐⭐⭐⭐⭐             | ⭐⭐⭐                  | ⭐⭐⭐⭐              |
| Simplicity      | ⭐⭐⭐⭐                | ⭐⭐⭐⭐                | ⭐⭐⭐                 |
| Testability     | ⭐⭐⭐⭐⭐             | ⭐⭐⭐⭐                | ⭐⭐⭐⭐              |
| Thread Safety   | ⭐⭐⭐⭐ _(Manageable)_ | ⭐⭐⭐⭐ _(Clear)_      | ⭐⭐⭐ _(Complex)_    |
| Discoverability | ⭐⭐⭐ _(Centralized)_   | ⭐⭐⭐⭐⭐ _(Explicit)_ | ⭐⭐ _(Decentralized)_ |

**Key Insights**:
- **Event Bus** provides the highest level of decoupling. Components don't need to know about each other at all, only about the events. This is excellent for testability and extensibility. The main challenge is ensuring events and their payloads are well-documented.
- **Dependency Injection** is a very clear and explicit way to manage dependencies. It's easy to see what a component relies on. However, it can lead to more complex constructor signatures and doesn't decouple components as thoroughly as an event bus.
- **Callbacks/Listeners** are a classic observer pattern but can become complex to manage (e.g., "callback hell") and can make the flow of control harder to follow in a system with many events.

### 4️⃣ DECISION
**Selected**: Option A: Event Bus (Pub/Sub).
**Rationale**: An event bus offers the best balance of decoupling, testability, and scalability for this application. It will allow for the clean separation of concerns required by the Single Responsibility Principle. For example, the `HotkeyManager` will simply publish a `HotkeyFired` event, and the `AudioRecorder` will subscribe to it, without either component knowing about the other's implementation details.

### 5️⃣ IMPLEMENTATION NOTES
- Create a central `EventBus` class (as a singleton) in the `core` module.
- The `EventBus` will have `subscribe(event_type, handler)` and `publish(event)` methods.
- Events will be simple data classes defining the event name and its payload.
- All inter-component communication will be migrated to use the event bus. For example:
  - `HotkeyManager` publishes `RecordingStartRequested` and `RecordingStopRequested`.
  - `AudioRecorder` subscribes to these events to control recording.
  - `AudioRecorder` publishes `AudioChunkReady`.
  - `TranscriptionService` subscribes to `AudioChunkReady` and publishes `TranscriptionReady`.
  - `OutputService` subscribes to `TranscriptionReady`.
- The event bus must be made thread-safe using locks to manage subscriber lists and event dispatching.
---

## 📌 CREATIVE PHASE START: Threading Model
**Date**: $(date)

### 1️⃣ PROBLEM
**Description**: The current implementation creates new threads (`threading.Thread`) for each recording and processing task. While functional, this is inefficient as it incurs the overhead of creating and destroying threads frequently. A more robust and efficient model is needed to handle concurrent operations like audio recording, transcription, and UI interaction (hotkeys).
**Requirements**:
- Efficiently manage background tasks (audio processing, transcription).
- Ensure the main thread (hotkey listener) remains responsive.
- Provide a clear way to manage and monitor long-running tasks.
- Allow for graceful shutdown of all background tasks.
**Constraints**:
- Must avoid race conditions and deadlocks.
- Should not add significant complexity to the overall architecture.

### 2️⃣ OPTIONS
**Option A**: `concurrent.futures.ThreadPoolExecutor` - Use a thread pool to manage a fixed number of worker threads. Tasks are submitted to the pool and executed by available threads.
**Option B**: Producer-Consumer with `queue.Queue` - Use thread-safe queues to pass data between dedicated threads (e.g., one thread for recording, one for processing).
**Option C**: Keep `threading.Thread` - Continue creating individual threads for each task but add better management and cleanup logic.

### 3️⃣ ANALYSIS
| Criterion          | A: ThreadPoolExecutor | B: Producer-Consumer Queue | C: Manual `threading.Thread` |
|--------------------|-----------------------|----------------------------|------------------------------|
| Efficiency         | ⭐⭐⭐⭐⭐            | ⭐⭐⭐⭐                    | ⭐⭐                         |
| Simplicity         | ⭐⭐⭐⭐               | ⭐⭐⭐                      | ⭐⭐⭐⭐                       |
| Scalability        | ⭐⭐⭐⭐               | ⭐⭐⭐                      | ⭐⭐                         |
| Control & Shutdown | ⭐⭐⭐⭐               | ⭐⭐⭐⭐                    | ⭐⭐                         |
| Error Handling     | ⭐⭐⭐⭐⭐ _(Futures)_  | ⭐⭐⭐ _(Manual)_           | ⭐⭐ _(Manual)_              |

**Key Insights**:
- **`ThreadPoolExecutor`** is the modern standard for managing threads in Python. It abstracts away the complexity of thread creation and management, provides a simple future-based API for getting results, and handles errors gracefully. It is highly efficient for managing multiple, independent, short-lived tasks.
- **Producer-Consumer Queue** is a powerful pattern for streaming data between long-running threads. It's very robust but can be more complex to set up and manage than a thread pool, especially for shutdown logic.
- **Manual `threading.Thread`** is simple for one-off tasks but inefficient and hard to manage at scale. Graceful shutdown and error handling become complex and error-prone.

### 4️⃣ DECISION
**Selected**: Option A: `concurrent.futures.ThreadPoolExecutor`.
**Rationale**: `ThreadPoolExecutor` provides the best combination of efficiency, simplicity, and robust error handling for this application's needs. It is the perfect tool for offloading the transcription task to a background thread without blocking the main event loop. It simplifies the code by removing the need for manual thread creation and `join()` calls.

### 5️⃣ IMPLEMENTATION NOTES
- Create a `ThreadPoolExecutor` instance (as a singleton or managed by the main `Application` class).
- When an `AudioChunkReady` event is published, the handler will submit the transcription task to the `ThreadPoolExecutor`.
- The `submit()` method will return a `Future` object. A callback can be added to the future (`future.add_done_callback()`) which will publish the `TranscriptionReady` event once the task is complete.
- This ensures the entire processing pipeline is asynchronous and does not block the event bus or the main thread.
- The `ThreadPoolExecutor` should be shut down gracefully (`executor.shutdown(wait=True)`) when the application exits to ensure all pending tasks are completed.
--- 