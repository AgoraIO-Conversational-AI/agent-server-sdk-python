import typing


def is_heygen_avatar(config: typing.Dict[str, typing.Any]) -> bool:
    return config.get("vendor") == "heygen"


def is_live_avatar_avatar(config: typing.Dict[str, typing.Any]) -> bool:
    return config.get("vendor") == "liveavatar"


def is_akool_avatar(config: typing.Dict[str, typing.Any]) -> bool:
    return config.get("vendor") == "akool"


def is_anam_avatar(config: typing.Dict[str, typing.Any]) -> bool:
    return config.get("vendor") == "anam"


def validate_avatar_config(config: typing.Dict[str, typing.Any]) -> None:
    """Validates avatar configuration at runtime.

    Parameters
    ----------
    config : dict
        The avatar configuration dictionary.

    Raises
    ------
    ValueError
        If the configuration is invalid.
    """
    if is_heygen_avatar(config) or is_live_avatar_avatar(config):
        label = "HeyGen" if is_heygen_avatar(config) else "LiveAvatar"
        params = config.get("params", {})
        if not params.get("api_key"):
            raise ValueError(f"{label} avatar requires api_key")
        if not params.get("quality"):
            raise ValueError(f"{label} avatar requires quality (low, medium, or high)")
        if not params.get("agora_uid"):
            raise ValueError(f"{label} avatar requires agora_uid")
        valid_qualities = ("low", "medium", "high")
        if params.get("quality") not in valid_qualities:
            raise ValueError(
                f"Invalid quality for {label}: {params.get('quality')}. "
                f"Must be one of: {', '.join(valid_qualities)}"
            )
    elif is_akool_avatar(config):
        params = config.get("params", {})
        if not params.get("api_key"):
            raise ValueError("Akool avatar requires api_key")
    elif is_anam_avatar(config):
        params = config.get("params", {})
        if not params.get("api_key"):
            raise ValueError("Anam avatar requires api_key")


def validate_tts_sample_rate(
    avatar_config: typing.Dict[str, typing.Any],
    tts_sample_rate: int,
) -> None:
    """Validates that TTS sample rate is compatible with the avatar vendor.

    Different avatar vendors have specific sample rate requirements:
    - HeyGen: ONLY supports 24,000 Hz
    - Akool: ONLY supports 16,000 Hz

    Parameters
    ----------
    avatar_config : dict
        The avatar configuration dictionary.
    tts_sample_rate : int
        The sample rate from your TTS configuration (in Hz).

    Raises
    ------
    ValueError
        If TTS sample rate is incompatible with the avatar vendor.
    """
    if is_heygen_avatar(avatar_config) or is_live_avatar_avatar(avatar_config):
        if tts_sample_rate != 24000:
            label = "HeyGen" if is_heygen_avatar(avatar_config) else "LiveAvatar"
            raise ValueError(
                f"{label} avatars ONLY support 24,000 Hz sample rate. "
                f"Your TTS is configured with {tts_sample_rate} Hz. "
                f"Please update your TTS configuration to use 24kHz sample rate. "
                f"See: https://docs.agora.io/en/conversational-ai/models/avatar/overview"
            )
    elif is_akool_avatar(avatar_config):
        if tts_sample_rate != 16000:
            raise ValueError(
                f"Akool avatars ONLY support 16,000 Hz sample rate. "
                f"Your TTS is configured with {tts_sample_rate} Hz. "
                f"Please update your TTS configuration to use 16kHz sample rate. "
                f"See: https://docs.agora.io/en/conversational-ai/models/avatar/akool"
            )
