from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "webui" / "Main.py"
SOURCE = MAIN.read_text(encoding="utf-8")


REQUIRED_TRANSLATION_KEYS = [
    "Basic Settings",
    "Hide Basic Settings",
    "Hide Log",
    "LLM Settings",
    "LLM Provider",
    "API Key",
    "Base Url",
    "Model Name",
    "Video Source Settings",
    "Pexels API Key",
    "Pixabay API Key",
    "Video Script Settings",
    "Video Subject",
    "Script Language",
    "Generate Video Script and Keywords",
    "Video Script",
    "Generate Video Keywords",
    "Video Keywords",
    "Advanced Script Settings",
    "Script Paragraph Number",
    "Custom Script Requirements",
    "Use Custom System Prompt",
    "Custom System Prompt",
    "Video Settings",
    "Video Source",
    "Video Concat Mode",
    "Video Transition Mode",
    "Video Ratio",
    "Clip Duration",
    "Number of Videos Generated Simultaneously",
    "Audio Settings",
    "TTS Servers",
    "Speech Synthesis",
    "Play Voice",
    "Speech Region",
    "Speech Key",
    "SiliconFlow API Key",
    "MiMo API Key",
    "Speech Volume",
    "Speech Rate",
    "Custom Audio File",
    "Background Music",
    "Custom Background Music File",
    "Background Music Volume",
    "Subtitle Settings",
    "Enable Subtitles",
    "Font",
    "Position",
    "Custom Position (% from top)",
    "Font Size",
    "Font Color",
    "Stroke Color",
    "Stroke Width",
    "Click to show API Key management",
    "Manage Pexels and Pixabay API Keys",
    "Add Pexels API Key",
    "Delete Selected Pexels API Key",
    "Add Pixabay API Key",
    "Delete Selected Pixabay API Key",
    "Generate Video",
]


REQUIRED_STATE_KEYS = [
    "video_subject",
    "video_script",
    "video_terms",
    "video_script_prompt",
    "custom_system_prompt",
    "use_custom_system_prompt",
    "ui_language",
    "local_video_materials",
]


REQUIRED_CONFIG_KEYS = [
    "hide_config",
    "hide_log",
    "llm_provider",
    "video_source",
    "tts_server",
    "voice_name",
    "font_name",
    "subtitle_position",
    "custom_position",
    "text_fore_color",
    "font_size",
    "pexels_api_keys",
    "pixabay_api_keys",
]


REQUIRED_UI_ANCHORS = [
    "creative-editor-shell",
    "editor-main-card",
    "preview-card",
    "config-stack",
    "generate-action-card",
]


REQUIRED_BEHAVIOR_ANCHORS = [
    "uploaded_audio_file",
    "uploaded_files",
    "params.video_materials",
    "logger.add(log_received)",
    "tm.start(task_id=task_id, params=params)",
    "open_task_folder(task_id)",
    "player_cols",
]


def test_existing_configuration_labels_remain_exposed():
    missing = [key for key in REQUIRED_TRANSLATION_KEYS if f'tr("{key}")' not in SOURCE]

    assert missing == []


def test_existing_state_and_config_keys_remain_wired():
    missing_state = [key for key in REQUIRED_STATE_KEYS if f'"{key}"' not in SOURCE]
    missing_config = [key for key in REQUIRED_CONFIG_KEYS if f'"{key}"' not in SOURCE]

    assert missing_state == []
    assert missing_config == []


def test_creative_editor_layout_anchors_exist():
    missing = [anchor for anchor in REQUIRED_UI_ANCHORS if anchor not in SOURCE]

    assert missing == []


def test_generation_behavior_anchors_remain_present():
    missing = [anchor for anchor in REQUIRED_BEHAVIOR_ANCHORS if anchor not in SOURCE]

    assert missing == []
