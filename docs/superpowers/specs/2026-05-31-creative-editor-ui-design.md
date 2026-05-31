# MoneyPrinterTurbo Creative Editor UI Redesign

## Context

The current Streamlit WebUI in `webui/Main.py` exposes the full video generation form as three dense columns: script settings, video/audio settings, and subtitle/API settings. This keeps every control visible, but it makes the primary creation path hard to scan and puts advanced configuration on the same visual level as the main task.

The approved direction is **C. Creative Editor**: reorganize the interaction flow so the screen feels like a short-video creation workspace instead of a settings dashboard.

## Goals

- Make the main path obvious: write or generate the script, review keywords, configure the video, then generate.
- Move secondary controls into clear grouped panels so they remain available without dominating the first view.
- Add a right-side preview and summary area that communicates video ratio, subtitle style, source, voice, and batch count at a glance.
- Preserve every configuration option currently exposed by the WebUI, even when an option moves into a new group or collapsed section.
- Keep existing generation behavior, configuration persistence, validation, and API calls intact unless layout changes require minor wiring.
- Keep the implementation inside Streamlit and the existing `webui/Main.py` structure unless small helpers make the layout clearer.

## Non-Goals

- Do not replace Streamlit with another frontend framework.
- Do not redesign backend task generation, LLM calls, TTS calls, video rendering, or upload logic.
- Do not add new providers, new media processing behavior, or new account management features.
- Do not remove existing options; hide advanced options only inside purposeful expanders or grouped sections.
- Do not change config key names, session state keys, validation rules, uploaded file handling, or task parameter semantics as part of the UI redesign.

## Configuration Coverage Requirement

The redesign must include all configuration currently available in the page. Moving a field is allowed; dropping it, renaming its stored key, or changing its behavior is not allowed.

Required coverage:

- Basic settings: hide basic settings, hide log.
- LLM settings: provider, API key, base URL, model name, provider-specific secret key or account ID fields, and existing provider help text.
- Video source settings: Pexels API key and Pixabay API key.
- Script settings: video subject, script language, AI script and keyword generation buttons, script text, keywords text, paragraph count, custom script requirements, custom system prompt toggle, and custom system prompt text.
- Video settings: source, local file upload, concat mode, transition mode, ratio, clip duration, and generated video count.
- Audio settings: TTS server, voice selection, voice preview, provider-specific TTS credentials and informational notes, speech volume, speech rate, custom audio upload, background music mode, custom background music path, and background music volume.
- Subtitle settings: enable subtitles, font, position, custom position, font color, font size, stroke color, and stroke width.
- API key management: list, add, and delete Pexels and Pixabay API keys.
- Generation output: generate button, validation messages, log output controlled by `hide_log`, result video playback, and opening the task folder after completion.

Before implementation is considered complete, each item above must be mapped to a visible or intentionally collapsed location in the new layout.

## Proposed Layout

### Top Bar

The top of the page becomes a compact app bar with:

- Product name and version.
- Language selector.
- Basic settings entry point.

The existing Basic Settings expander remains available, but it should be visually separated from the creation workspace. If `hide_config` is false, it can sit below the app bar in a collapsed section.

### Main Creation Area

The left and widest area becomes the primary editor:

- Video subject input.
- Script language selector.
- AI action row for generating script and keywords.
- Main script text area.
- Keyword text area or compact keyword block.
- Advanced script settings in a collapsed expander directly below the script controls.

This area should read as step 1 of the workflow and should not be interrupted by video, audio, or subtitle controls.

### Right Preview And Configuration Area

The right column becomes a preview and configuration stack:

- A phone-style preview card for portrait output and a landscape-style frame when landscape is selected.
- A compact summary of current ratio, source, voice, subtitle status, and number of videos.
- Grouped expanders for:
  - Material and video settings.
  - Voice and background music.
  - Subtitle styling.
  - API key management.

Each group should keep the current options and persistence behavior. The first group can be expanded by default because video source and ratio are required for a valid task. Audio and subtitle groups can default to collapsed or expanded based on available vertical space after implementation.

The grouped expanders are organizational only. They must not change how values are written into `config`, `st.session_state`, or `VideoParams`.

### Generate And Output Area

The generation button moves to a clear bottom action area:

- Primary `Generate Video` button remains full-width or visually prominent.
- Validation messages should appear near this area when possible.
- Runtime log output remains below or next to the action area and still respects `hide_log`.
- Generated video players remain in the task result area after completion.

## Interaction Flow

1. User enters a video subject or script in the main editor.
2. User optionally asks AI to generate the script and keywords.
3. User reviews material/video summary in the right panel and opens grouped settings as needed.
4. User checks the preview summary for ratio, subtitles, and voice.
5. User clicks `Generate Video`.
6. Existing validation, file persistence, task execution, logging, result playback, and task folder opening run as they do today.

## Implementation Notes

- Keep state keys such as `video_subject`, `video_script`, `video_terms`, `video_script_prompt`, `custom_system_prompt`, `use_custom_system_prompt`, `ui_language`, and `local_video_materials`.
- Reuse existing `VideoParams` construction and config writes.
- Prefer small local helper functions for repeated layout markup or CSS injection if they reduce clutter in `webui/Main.py`.
- Use Streamlit containers, columns, and expanders; avoid introducing new dependencies.
- Add CSS only for visual hierarchy, spacing, preview cards, and button/card polish. CSS must not become a separate behavior layer.
- Preserve all current validation checks for empty subject/script, invalid source, and missing API keys.
- Keep API key management accessible but no longer visually equal to the main creation path.

## Verification

After implementation:

- Run a syntax check for `webui/Main.py`.
- Start the Streamlit WebUI locally.
- Open the app in the browser and verify the editor layout renders without overlapping controls.
- Walk through the configuration coverage list and confirm every existing control is present in the new layout.
- Verify changing language still updates labels.
- Verify the AI script and keyword buttons still write to session state when providers are configured.
- Verify local file upload controls still appear only when local source is selected.
- Verify `Generate Video` validation still catches empty input and missing required API keys.
- Verify the generated result area still displays videos when a task completes.
