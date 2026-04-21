## QAMA Framework - Windows Settings Automation

Python-based test automation framework for the **Windows Settings** application using:

- **Pytest** as test runner  
- **Selenium + Appium Python Client v3 (Windows Driver)**  
- **Page Object Model (POM)**  
- **QAMA-style folder structure with JSON locators**

---

### Project Structure

```text
qama_winapplication/
├── config/
│   └── config.yaml                    # Appium / app / timeout configuration
├── libs/
│   ├── drivers/
│   │   ├── windows_driver.py          # Appium Windows driver factory (singleton)
│   │   └── app_session.py             # Start/stop Settings app session
│   ├── flows/
│   │   └── windows/
│   │       └── settings_page.py       # Main Page Object for Windows Settings
│   └── utils/
│       ├── base_page.py               # Generic POM base using JSON ui_map
│       ├── waits.py                   # Explicit wait helpers
│       ├── assertions.py              # Custom assertion helpers
│       └── logger.py                  # File/console logging
├── resource/
│   └── ui_map/
│       └── windows/
│           └── settings.json          # JSON UI map (locators + test data)
├── tests/
│   ├── conftest.py                    # Pytest fixtures, markers, reports dir
│   └── modules/
│       └── settings/
│           ├── test_settings_system_display.py      # 10 tests: System > Display
│           ├── test_settings_time_language.py       # 10 tests: Time & language
│           └── test_settings_personalization.py     # 10 tests: Personalization
├── logs/                              # Execution logs (created at runtime)
├── reports/                           # HTML reports (created at runtime)
├── PROJECT_OVERVIEW.txt               # Detailed architecture documentation
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

### Key Concepts and Flow

- **Driver & Session**
  - `libs/drivers/windows_driver.py` creates a singleton `Remote` driver using values from `config/config.yaml`.
  - `libs/drivers/app_session.py` provides `AppSession.start()` / `AppSession.stop()` used by pytest fixtures.

- **POM & Locators**
  - `libs/utils/base_page.py` loads `resource/ui_map/windows/settings.json` and interprets the `"locators"` section.
  - Locators follow the format you defined:
    - `{"locator": {"AutomationID": "..."}}` → `By.ACCESSIBILITY_ID`
    - `{"locator": {"name": "..."}}` → `By.NAME`
  - `libs/flows/windows/settings_page.py` exposes high-level actions:
    - Navigation (System > Display, Time & language, Personalization, etc.)
    - Feature operations (brightness, night light, time toggles, themes, taskbar, etc.)

- **Tests & Fixtures**
  - `tests/conftest.py`:
    - Adds project root to `sys.path`.
    - Provides fixtures:
      - `logger` (session)
      - `driver` (session, uses `AppSession`)
      - `settings_page` (function, main POM)
    - Registers markers:
      - `smoke`, `regression`
      - `settings_navigation`, `settings_functional`
      - `system_display`, `time_language`, `personalization`
    - Ensures `reports/` directory exists before the run.
  - Feature test files under `tests/modules/settings/` use `settings_page` and markers to group 30 test cases.

---

### Prerequisites

- **OS**: Windows 10/11 (where Windows Settings is available)  
- **Python**: 3.8+  
- **Appium server with Windows Driver plugin** running on the URL you configure in `config/config.yaml` (default `http://127.0.0.1:4723`).

---

### Installation

1. **Navigate to the project**

```bash
cd qama_winapplication
```

2. **Create and activate virtual environment (recommended)**

```bash
python -m venv venv
# PowerShell
.\venv\Scripts\Activate.ps1
# or CMD
venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure Appium / Settings app if needed**

- Edit `config/config.yaml` to adjust:
  - Top-level `winappdriver.server_url`, `platformName`, `deviceName`
  - `modules.settings.app.app_id` if the AUMID/AppId is different on your machine
  - `modules.settings.timeouts.implicit_wait_sec` and `new_command_timeout_sec`

---

### Running Tests

Before running tests, start **Appium server with Windows driver** on the URL configured in `config.yaml`.

#### Run all Settings tests (30 cases) with HTML report

```bash
pytest tests/modules/settings \
  --html=reports/all_settings.html --self-contained-html
```

#### Run only System > Display tests

```bash
pytest -m system_display \
  tests/modules/settings/test_settings_system_display.py \
  --html=reports/system_display.html --self-contained-html
```

#### Run only Time & language tests

```bash
pytest -m time_language \
  tests/modules/settings/test_settings_time_language.py \
  --html=reports/time_language.html --self-contained-html
```

#### Run only Personalization tests

```bash
pytest -m personalization \
  tests/modules/settings/test_settings_personalization.py \
  --html=reports/personalization.html --self-contained-html
```

#### Run only smoke tests across all features

```bash
pytest -m smoke \
  --html=reports/smoke.html --self-contained-html
```

You can combine markers as needed, for example:

```bash
pytest -m "settings_functional and personalization"
```

---

### Technologies Used

- **Python 3.8+** – language  
- **Selenium 4** + **Appium-Python-Client v3** – Windows app automation via Appium Windows driver  
- **pytest** – test framework, fixtures, markers  
- **pytest-html** – HTML report generation  
- **YAML / JSON** – external configuration and UI map

---

### Extending the Framework

- **Add new Settings feature**
  - Add locators under a new section in `resource/ui_map/windows/settings.json`.
  - Implement navigation/actions in `SettingsPage` using `find`, `click`, `get_text`.
  - Create a new test module under `tests/modules/settings/` and (optionally) a new marker.

- **Adjust locators**
  - Update `"locator": {"AutomationID": "..."} or {"name": "..."}` entries in `settings.json` to match your environment.

For deeper architectural details, see `PROJECT_OVERVIEW.txt`.

