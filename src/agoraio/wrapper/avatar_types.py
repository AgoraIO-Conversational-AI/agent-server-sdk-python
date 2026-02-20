import typing


def is_heygen_avatar(config: typing.Dict[str, typing.Any]) -> bool:
    return config.get("vendor") == "heygen"


def is_akool_avatar(config: typing.Dict[str, typing.Any]) -> bool:
    return config.get("vendor") == "akool"


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
    if is_heygen_avatar(config):
        params = config.get("params", {})
        if not params.get("api_key"):
            raise ValueError("HeyGen avatar requires api_key")
        if not params.get("quality"):
            raise ValueError("HeyGen avatar requires quality (low, medium, or high)")
        if not params.get("agora_uid"):
            raise ValueError("HeyGen avatar requires agora_uid")
        valid_qualities = ("low", "medium", "high")
        if params.get("quality") not in valid_qualities:
            raise ValueError(
                f"Invalid quality for HeyGen: {params.get('quality')}. "
                f"Must be one of: {', '.join(valid_qualities)}"
            )
    elif is_akool_avatar(config):
        params = config.get("params", {})
        if not params.get("api_key"):
            raise ValueError("Akool avatar requires api_key")


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
    if is_heygen_avatar(avatar_config):
        if tts_sample_rate != 24000:
            raise ValueError(
                f"HeyGen avatars ONLY support 24,000 Hz sample rate. "
                f"Your TTS is configured with {tts_sample_rate} Hz. "
                f"Please update your TTS configuration to use 24kHz sample rate. "
                f"See: https://docs.agora.io/en/conversational-ai/models/avatar/heygen"
            )
    elif is_akool_avatar(avatar_config):
        if tts_sample_rate != 16000:
            raise ValueError(
                f"Akool avatars ONLY support 16,000 Hz sample rate. "
                f"Your TTS is configured with {tts_sample_rate} Hz. "
                f"Please update your TTS configuration to use 16kHz sample rate. "
                f"See: https://docs.agora.io/en/conversational-ai/models/avatar/akool"
            )
