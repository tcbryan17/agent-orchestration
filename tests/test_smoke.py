from agent_orchestration.config import Settings


def test_settings_defaults_need_no_api_key() -> None:
    # CI has no key; the app must still import, with Haiku as the default model (ADR 0002).
    fields = Settings.model_fields
    assert fields["anthropic_api_key"].default is None
    assert fields["default_model"].default == "claude-haiku-5-5"
