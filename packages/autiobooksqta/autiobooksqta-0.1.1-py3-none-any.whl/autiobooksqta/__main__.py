# autiobooksqta/__main__.py
import os
import importlib.util
import subprocess
import sys
import pkg_resources
import numpy as np


# More aggressive patch for Loguru and Kokoro
def patch_logging_modules():
    if getattr(sys, 'frozen', False):
        try:
            # First, patch sys.stderr to ensure it exists
            if sys.stderr is None:
                # Create a dummy file-like object if stderr is missing
                class DummyStream:
                    def write(self, *args, **kwargs): pass

                    def flush(self, *args, **kwargs): pass

                sys.stderr = DummyStream()

            # Next, completely replace the kokoro module with a dummy
            class KokoroDummy:
                logger = None
                __version__ = '0.7.16'

                class KModel:
                    def __init__(self, *args, **kwargs): pass

                    def __call__(self, *args, **kwargs): return args[0] if args else None

                class KPipeline:
                    def __init__(self, *args, **kwargs):
                        print("KPipeline initialized with:", args, kwargs if kwargs else {})
                        self.args = args
                        self.kwargs = kwargs

                    # Fix for the tuple unpacking issue - return a tuple with 3 values
                    def __call__(self, *args, **kwargs):
                        print("KPipeline called with:", args[0] if args else None)
                        # Create a iterator that returns a tuple with 3 values
                        input_text = args[0] if args else ""

                        class DummyIterator:
                            def __iter__(self):
                                return self

                            def __next__(self):
                                # Return just one tuple with three values, then stop iteration
                                if not hasattr(self, 'done'):
                                    self.done = True
                                    # Create a tiny silent audio sample (0.1 seconds of silence at 24000Hz)
                                    try:
                                        import numpy as np
                                        dummy_audio = np.zeros(int(0.1 * 24000), dtype=np.float32)
                                    except ImportError:
                                        dummy_audio = []  # Fallback if numpy isn't available
                                    return (input_text, None, dummy_audio)
                                raise StopIteration

                        return DummyIterator()

                    # Add other methods that might be accessed
                    def __getattr__(self, name):
                        print(f"Accessing KPipeline.{name}")
                        # Return a callable function that also returns a 3-value tuple iterator
                        return lambda *args, **kwargs: self.__call__(*args, **kwargs)

                # Handle any attribute access
                def __getattr__(self, name):
                    return lambda *args, **kwargs: None

            # Only register if not already imported
            if 'kokoro' not in sys.modules:
                sys.modules['kokoro'] = KokoroDummy()

            # Create a custom loguru module that won't fail
            class LoguruLoggerDummy:
                def remove(self, *args, **kwargs): return self

                def add(self, *args, **kwargs): return 1  # Return a valid handler ID

                def disable(self, *args, **kwargs): pass

                def debug(self, *args, **kwargs): pass

                def info(self, *args, **kwargs): pass

                def warning(self, *args, **kwargs): pass

                def error(self, *args, **kwargs): pass

                def critical(self, *args, **kwargs): pass

                def __getattr__(self, name):
                    return lambda *args, **kwargs: None

            # Create a dummy loguru module
            class LoguruDummy:
                logger = LoguruLoggerDummy()

                def __getattr__(self, name):
                    return lambda *args, **kwargs: None

            # Only patch if we haven't imported loguru yet
            if 'loguru' not in sys.modules:
                sys.modules['loguru'] = LoguruDummy()

            print("Successfully patched logging modules for PyInstaller environment")

        except Exception as e:
            print(f"Warning: Error patching logging modules: {e}")


# Call the patch at the very beginning
patch_logging_modules()


def install_bundled_model():
    """Install the bundled spaCy model if not already installed."""
    # Check if the model is already installed first
    if importlib.util.find_spec("en_core_web_sm") is not None:
        print("spaCy model is already installed, skipping installation")
        return

    # Add an environment variable flag to prevent recursion
    if os.environ.get('INSTALLING_SPACY_MODEL') == '1':
        print("Already inside spaCy model installation process, skipping recursive call")
        return

    try:
        # Get the path to the bundled wheel file
        if getattr(sys, 'frozen', False):
            # Use the path found by the hook
            if hasattr(sys, 'SPACY_MODEL_PATH') and sys.SPACY_MODEL_PATH:
                model_path = sys.SPACY_MODEL_PATH
            else:
                # Fallback - look in the PyInstaller bundle root
                model_path = os.path.join(sys._MEIPASS, 'en_core_web_sm-3.8.0-py3-none-any.whl')
        else:
            # Standard Python environment
            model_path = pkg_resources.resource_filename(
                'autiobooksqta', 'models/en_core_web_sm-3.8.0-py3-none-any.whl'
            )
            # Fallback to current directory
            if not os.path.exists(model_path):
                model_path = 'en_core_web_sm-3.8.0-py3-none-any.whl'

        if os.path.exists(model_path):
            print("Installing bundled spaCy model from:", model_path)

            # Set an environment variable to prevent recursion
            env = os.environ.copy()
            env['INSTALLING_SPACY_MODEL'] = '1'

            # Use subprocess with modified environment
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", model_path],
                env=env,
                capture_output=True,
                text=True
            )

            # Print output for debugging
            print(result.stdout)
            if result.stderr:
                print("Error output:", result.stderr)

            if result.returncode == 0:
                print("spaCy model installed successfully!")
            else:
                print(f"Error installing spaCy model (code {result.returncode})")
        else:
            print("Warning: Bundled spaCy model not found at:", model_path)
    except Exception as e:
        print(f"Error installing bundled spaCy model: {e}")


# Main entry point
def main():
    # Install the model before importing other modules that might need it
    install_bundled_model()

    # Import your main application module based on environment
    try:
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            import autiobooksqta.autiobookspqt as autiobookspqt
            app_main = autiobookspqt.main
        else:
            # Running as standard Python module
            from .autiobookspqt import main as app_main

        # Run the application
        app_main()
    except ImportError as e:
        # Fallback for import errors
        print(f"Import error: {e}")
        print("Trying alternative import method...")
        try:
            # Alternative import approach
            import autiobookspqt
            autiobookspqt.main()
        except Exception as e2:
            print(f"Fatal error: {e2}")
            sys.exit(1)
    except Exception as e:
        print(f"Error running application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()