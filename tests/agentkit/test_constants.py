from agora_agent.agentkit import (
    DataChannel,
    FillerWordsSelectionRule,
    GeofenceArea,
    GeofenceExcludeArea,
    SalModeValues,
    SilenceActionValues,
    TurnDetectionTypeValues,
)


def test_constants_match_expected_values():
    assert DataChannel.RTM == "rtm"
    assert DataChannel.DATASTREAM == "datastream"
    assert SilenceActionValues.SPEAK == "speak"
    assert SilenceActionValues.THINK == "think"
    assert SalModeValues.LOCKING == "locking"
    assert SalModeValues.RECOGNITION == "recognition"
    assert GeofenceArea.GLOBAL == "GLOBAL"
    assert GeofenceArea.NORTH_AMERICA == "NORTH_AMERICA"
    assert GeofenceExcludeArea.JAPAN == "JAPAN"
    assert FillerWordsSelectionRule.SHUFFLE == "shuffle"
    assert FillerWordsSelectionRule.ROUND_ROBIN == "round_robin"
    assert TurnDetectionTypeValues.AGORA_VAD == "agora_vad"
    assert TurnDetectionTypeValues.SERVER_VAD == "server_vad"
    assert TurnDetectionTypeValues.SEMANTIC_VAD == "semantic_vad"
