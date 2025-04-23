import llm_logging_debug


def test_hook_sets_debug_logging_when_env_var_is_set(monkeypatch):
    # I couldn't figure out how to have this assert that basicConfig
    # had been correctly called.
    assert llm_logging_debug.is_setup is False
    llm_logging_debug.register_models()
    assert llm_logging_debug.is_setup is False
    monkeypatch.setenv("LLM_LOGGING_DEBUG", "1")
    llm_logging_debug.register_models()
    assert llm_logging_debug.is_setup is True
