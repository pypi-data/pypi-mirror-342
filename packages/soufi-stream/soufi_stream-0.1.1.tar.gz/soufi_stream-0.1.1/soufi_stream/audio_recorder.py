import os
import streamlit.components.v1 as components
import base64

# Get the directory of the current file
_RELEASE = True

# Determine paths for production vs development
if _RELEASE:
    # When the component is installed as a package
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "templates")
    _audio_recorder = components.declare_component(
        "audio_recorder",
        path=build_dir
    )
else:
    # When running in development mode (component is not installed as package)
    _audio_recorder = components.declare_component(
        "audio_recorder",
        url="http://localhost:3001",  # Local dev server
    )


def audio_recorder(
    interval=50,
    threshold=-60,
    play=False,
    silenceTimeout=1500,
    key=None
):
    """
    Create an audio recorder component that segments recordings based on silence detection.
    
    Parameters:
    -----------
    interval : int
        Time in milliseconds between checks for silence (default: 50)
    threshold : int
        Volume threshold in dB to detect silence (default: -60)
    play : bool
        Whether to play back the audio during recording (default: False)
    silenceTimeout : int
        Time in milliseconds of silence before stopping a segment (default: 1500)
    key : str or None
        An optional key that uniquely identifies this component (default: None)
        
    Returns:
    --------
    dict or None
        None if no recording has been made yet
        A dict with keys:
        - 'audioData': base64 encoded audio data (when status is 'stopped')
        - 'status': 'stopped' when a recording segment is ready
        - 'error': error message string if an error occurred
    """
    component_value = _audio_recorder(
        interval=interval,
        threshold=threshold,
        play=play,
        silenceTimeout=silenceTimeout,
        key=key,
        default=None
    )
    
    return component_value


# For development and testing
if _RELEASE:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "templates")
    _audio_recorder = components.declare_component(
        "audio_recorder",
        path=build_dir
    )