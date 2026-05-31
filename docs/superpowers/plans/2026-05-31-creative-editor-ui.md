# Creative Editor UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rework the Streamlit WebUI into the approved creative editor layout while preserving every existing configuration option and generation behavior.

**Architecture:** Keep the app in `webui/Main.py` and reorganize the existing controls into a main editor column, a right-side preview/configuration column, and a bottom generation/output area. Add source-level coverage tests that guard against dropping existing controls, config keys, session-state keys, and validation branches during the UI reflow.

**Tech Stack:** Python, Streamlit, pytest-style source inspection tests, existing MoneyPrinterTurbo services and models.

---

## File Structure

- Modify: `webui/Main.py`
  - Adds CSS helper markup for the creative editor shell.
  - Reorders the existing Streamlit controls into the approved editor workflow.
  - Preserves existing `VideoParams`, `config`, `st.session_state`, upload handling, validation, task execution, and result playback semantics.
- Create: `test/webui/test_main_ui_coverage.py`
  - Performs focused source checks for required controls and behavioral anchors.
  - Protects against accidental deletion of fields while the page is reorganized.
- Create: `docs/superpowers/plans/2026-05-31-creative-editor-ui.md`
  - This implementation plan.

## Task 1: Add Configuration Coverage Tests

**Files:**
- Create: `test/webui/test_main_ui_coverage.py`
- Read: `docs/superpowers/specs/2026-05-31-creative-editor-ui-design.md`
- Read: `webui/Main.py`

- [ ] **Step 1: Write the failing coverage test**

Create `test/webui/test_main_ui_coverage.py` with this content:

```python
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
```

- [ ] **Step 2: Run the coverage test and verify it fails**

Run:

```powershell
python -m pytest test/webui/test_main_ui_coverage.py -q
```

Expected: `test_creative_editor_layout_anchors_exist` fails because the new layout anchors are not present yet.

- [ ] **Step 3: Commit only the failing test if execution pauses**

If pausing after this task:

```powershell
git add -- test/webui/test_main_ui_coverage.py
git commit -m "Add WebUI configuration coverage tests"
```

## Task 2: Add Creative Editor Styling And Helpers

**Files:**
- Modify: `webui/Main.py`
- Test: `test/webui/test_main_ui_coverage.py`

- [ ] **Step 1: Add helper CSS and lightweight section helpers**

Replace the current `streamlit_style` block with a richer CSS block that keeps Streamlit controls native and adds only visual hierarchy. Include these anchors:

```python
streamlit_style = """
<style>
h1 {
    padding-top: 0 !important;
}
.creative-editor-shell {
    padding: 0.25rem 0 1rem;
}
.editor-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem 1.1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(49, 51, 63, 0.12);
    border-radius: 8px;
    background: linear-gradient(135deg, #101827 0%, #172033 100%);
    color: #ffffff;
}
.editor-brand-title {
    font-size: 1.45rem;
    line-height: 1.2;
    font-weight: 750;
}
.editor-brand-subtitle {
    margin-top: 0.25rem;
    color: rgba(255, 255, 255, 0.72);
    font-size: 0.88rem;
}
.editor-main-card,
.preview-card,
.config-stack,
.generate-action-card {
    border: 1px solid rgba(49, 51, 63, 0.12);
    border-radius: 8px;
    background: #ffffff;
    padding: 1rem;
}
.editor-section-title {
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.35rem;
}
.editor-section-caption {
    color: #64748b;
    font-size: 0.88rem;
    margin-bottom: 0.9rem;
}
.preview-phone {
    width: min(100%, 210px);
    aspect-ratio: 9 / 16;
    margin: 0 auto 1rem;
    border-radius: 24px;
    padding: 0.75rem;
    background: #111827;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.20);
}
.preview-landscape {
    width: 100%;
    aspect-ratio: 16 / 9;
    margin: 0 auto 1rem;
    border-radius: 14px;
    padding: 0.55rem;
    background: #111827;
    box-shadow: 0 16px 34px rgba(15, 23, 42, 0.16);
}
.preview-screen {
    height: 100%;
    border-radius: inherit;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 25% 20%, rgba(255,255,255,0.32), transparent 24%),
        linear-gradient(150deg, #14b8a6 0%, #3b82f6 48%, #111827 100%);
}
.preview-caption {
    position: absolute;
    left: 12%;
    right: 12%;
    bottom: 13%;
    height: 12%;
    border-radius: 7px;
    background: rgba(15, 23, 42, 0.72);
}
.summary-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.6rem;
}
.summary-item {
    border-radius: 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 0.65rem;
}
.summary-label {
    color: #64748b;
    font-size: 0.75rem;
}
.summary-value {
    color: #0f172a;
    font-weight: 700;
    font-size: 0.92rem;
    margin-top: 0.15rem;
}
.generate-action-card {
    margin-top: 1rem;
}
</style>
"""
```

Add two small helpers after `tr`:

```python
def section_heading(title, caption=""):
    st.markdown(
        f'<div class="editor-section-title">{title}</div>'
        + (f'<div class="editor-section-caption">{caption}</div>' if caption else ""),
        unsafe_allow_html=True,
    )


def render_preview_card(params):
    ratio_label = tr("Portrait") if params.video_aspect == VideoAspect.portrait else tr("Landscape")
    preview_class = "preview-phone" if params.video_aspect == VideoAspect.portrait else "preview-landscape"
    st.markdown(
        f"""
        <div class="preview-card">
          <div class="editor-section-title">{tr("Video Preview")}</div>
          <div class="{preview_class}">
            <div class="preview-screen"><div class="preview-caption"></div></div>
          </div>
          <div class="summary-grid">
            <div class="summary-item"><div class="summary-label">{tr("Video Ratio")}</div><div class="summary-value">{ratio_label}</div></div>
            <div class="summary-item"><div class="summary-label">{tr("Video Source")}</div><div class="summary-value">{params.video_source or "-"}</div></div>
            <div class="summary-item"><div class="summary-label">{tr("Speech Synthesis")}</div><div class="summary-value">{params.voice_name or "-"}</div></div>
            <div class="summary-item"><div class="summary-label">{tr("Number of Videos Generated Simultaneously")}</div><div class="summary-value">{params.video_count}</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
```

- [ ] **Step 2: Run the coverage test**

Run:

```powershell
python -m pytest test/webui/test_main_ui_coverage.py -q
```

Expected: layout anchor test still fails until the layout uses the anchors in the body.

## Task 3: Reflow Existing Controls Into Creative Editor Layout

**Files:**
- Modify: `webui/Main.py`
- Test: `test/webui/test_main_ui_coverage.py`

- [ ] **Step 1: Replace the three equal columns with editor columns**

Change:

```python
panel = st.columns(3)
left_panel = panel[0]
middle_panel = panel[1]
right_panel = panel[2]
```

to:

```python
editor_columns = st.columns([1.35, 0.85], gap="large")
left_panel = editor_columns[0]
right_panel = editor_columns[1]
```

Move the existing `Video Script Settings` block into `left_panel` inside a container with the `editor-main-card` anchor. Move video, audio, subtitle, and API key management into `right_panel` inside grouped expanders under the `config-stack` anchor. Keep all existing assignments and config writes.

- [ ] **Step 2: Keep video settings in the required settings group**

In `right_panel`, place the current video source, local upload, concat mode, transition mode, ratio, clip duration, and video count controls inside:

```python
with st.container():
    st.markdown('<div class="config-stack">', unsafe_allow_html=True)
    with st.expander(tr("Video Settings"), expanded=True):
        ...
    with st.expander(tr("Audio Settings"), expanded=False):
        ...
    with st.expander(tr("Subtitle Settings"), expanded=False):
        ...
    with st.expander(tr("Click to show API Key management"), expanded=False):
        ...
    st.markdown("</div>", unsafe_allow_html=True)
```

- [ ] **Step 3: Render the preview summary after values are collected**

Call `render_preview_card(params)` in the right column after the video, audio, and subtitle controls have populated `params.video_aspect`, `params.video_source`, `params.voice_name`, and `params.video_count`.

- [ ] **Step 4: Move generation into a bottom action card**

Wrap the existing generate button and output code with:

```python
st.markdown('<div class="generate-action-card">', unsafe_allow_html=True)
start_button = st.button(tr("Generate Video"), use_container_width=True, type="primary")
st.markdown("</div>", unsafe_allow_html=True)
```

Keep the existing validation and task execution block directly below the button.

- [ ] **Step 5: Run the coverage test**

Run:

```powershell
python -m pytest test/webui/test_main_ui_coverage.py -q
```

Expected: all tests pass.

## Task 4: Verify Runtime And Layout

**Files:**
- Verify: `webui/Main.py`
- Verify: `test/webui/test_main_ui_coverage.py`

- [ ] **Step 1: Run Python syntax check**

Run:

```powershell
python -m py_compile webui/Main.py
```

Expected: no output and exit code 0.

- [ ] **Step 2: Run coverage tests**

Run:

```powershell
python -m pytest test/webui/test_main_ui_coverage.py -q
```

Expected: all tests pass.

- [ ] **Step 3: Start Streamlit and inspect the page**

Run:

```powershell
streamlit run webui/Main.py --server.headless true --server.port 8501
```

Expected: the app starts on `http://localhost:8501`.

Open the app and confirm:

- Top bar renders with product/version and language selector.
- Main editor shows subject, script language, AI buttons, script text, keyword text, and advanced script settings.
- Right side contains preview plus video, audio, subtitle, and API key groups.
- Local upload appears when `Local file` is selected.
- Empty input validation still shows `Video Script and Subject Cannot Both Be Empty`.

## Task 5: Commit Implementation

**Files:**
- Add: `docs/superpowers/plans/2026-05-31-creative-editor-ui.md`
- Add: `test/webui/test_main_ui_coverage.py`
- Modify: `webui/Main.py`

- [ ] **Step 1: Review diff**

Run:

```powershell
git diff -- webui/Main.py test/webui/test_main_ui_coverage.py docs/superpowers/plans/2026-05-31-creative-editor-ui.md
```

Expected: diff only contains the planned UI reflow, coverage test, and plan document.

- [ ] **Step 2: Commit**

Run:

```powershell
git add -- webui/Main.py test/webui/test_main_ui_coverage.py docs/superpowers/plans/2026-05-31-creative-editor-ui.md
git commit -m "Rework Streamlit WebUI as creative editor"
```
