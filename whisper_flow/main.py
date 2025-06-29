import sys
import os
import atexit
from whisper_flow.core.application import Application
from whisper_flow.config.settings import settings

# Force unbuffered output for better logging
import functools
print = functools.partial(print, flush=True)

def main():
    """Main entry point for the application."""
    print("🚀 WhisperFlow starting up...")
    print(f"📋 Configuration: beam_size={settings.performance.beam_size}, model={settings.performance.model_size}")
    
    # --- Single Instance Lock ---
    lock_file_handle = None
    try:
        # Create a lock file in exclusive mode. Fails if file exists.
        lock_file_handle = open(settings.app.lock_file, 'x')
        lock_file_handle.write(str(os.getpid()))
        lock_file_handle.close()

        # Ensure the lock file is removed on any exit
        def remove_lock_file():
            if os.path.exists(settings.app.lock_file):
                print("\nExiting and cleaning up lock file.")
                os.remove(settings.app.lock_file)
        
        atexit.register(remove_lock_file)

    except FileExistsError:
        print("Another instance of WhisperFlow is already running. Exiting.")
        print(f"If this is an error, manually delete the lock file: {settings.app.lock_file}")
        sys.exit(1)
    finally:
        if lock_file_handle:
            lock_file_handle.close()
    # --- End of Single Instance Lock ---

    app = Application()
    try:
        app.run()
    except KeyboardInterrupt:
        print("\nCaught interrupt, shutting down...")
    finally:
        app.shutdown()


if __name__ == "__main__":
    main() 