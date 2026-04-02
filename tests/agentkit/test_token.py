from unittest import mock

import pytest

from agora_agent.agentkit.token import (
    MAX_EXPIRY_SECONDS,
    expires_in_hours,
    expires_in_minutes,
    generate_convo_ai_token,
    generate_rtc_token,
)


def test_expires_in_helpers_validate_and_cap_values():
    with pytest.raises(ValueError):
        expires_in_hours(0)
    with pytest.raises(ValueError):
        expires_in_minutes(-1)

    with pytest.warns(UserWarning):
        assert expires_in_hours(30) == MAX_EXPIRY_SECONDS
    with pytest.warns(UserWarning):
        assert expires_in_minutes(60 * 30) == MAX_EXPIRY_SECONDS

    assert expires_in_hours(1.5) == 5400
    assert expires_in_minutes(2.5) == 150


def test_token_generators_return_non_empty_strings():
    rtc = generate_rtc_token(
        app_id="a" * 32,
        app_certificate="b" * 32,
        channel="demo",
        uid=1,
    )
    convo = generate_convo_ai_token(
        app_id="a" * 32,
        app_certificate="b" * 32,
        channel_name="demo",
        account="1",
    )
    assert isinstance(rtc, str) and rtc
    assert isinstance(convo, str) and convo


def test_generate_convo_ai_token_uses_builder_when_available_and_defaults_privilege_expire():
    fake_builder = mock.Mock()
    fake_builder.buildTokenWithRtm.return_value = "token-123"

    with mock.patch.dict("sys.modules", {"agora_token_builder": mock.Mock(RtcTokenBuilder=fake_builder)}):
        token = generate_convo_ai_token(
            app_id="app-id",
            app_certificate="app-cert",
            channel_name="demo",
            account="1",
            token_expire=120,
            privilege_expire=0,
        )

    assert token == "token-123"
    fake_builder.buildTokenWithRtm.assert_called_once_with(
        "app-id",
        "app-cert",
        "demo",
        "1",
        1,
        120,
        0,
    )
