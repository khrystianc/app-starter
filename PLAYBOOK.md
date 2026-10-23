# App Factory Playbook

Every app follows the same loop: create a repo from the `app-starter` template, open it in a Codespace, have Claude Code build it on a branch, let GitHub Actions test the pull request, merge, and Render deploys it. Set up the factory once, then run the loop for each app.

Think of `app-starter` as the standard load plan. Every vehicle leaves the motor pool packed the same way, so you only solve each problem once.

---

## Part 1: One-time setup (about 30 minutes)

### 1. Create the template repo

1. On GitHub, create a new **public** repo named `app-starter`. Public is fine because it holds no secrets, and it lets Claude Code copy the kit into your existing repos.
2. Upload everything in this kit (including the hidden `.devcontainer` and `.github` folders). The easiest way is to open the empty repo in a Codespace and drag the folders into the VS Code file explorer.
3. In the repo, go to **Settings** and check **Template repository**.

### 2. Keep Claude Code signed in across Codespaces

1. Open a Codespace on `app-starter` (**Code → Codespaces → Create codespace on main**).
2. When it finishes building, run `claude setup-token` in the terminal and follow the sign-in. It prints a long-lived token.
3. On GitHub, go to your profile **Settings → Codespaces → Secrets → New secret**.
   - Name: `CLAUDE_CODE_OAUTH_TOKEN`
   - Value: the token
   - Repository access: `app-starter` for now. You'll add each new app repo here as you create it.

### 3. Connect Render

Create a Render account and connect your GitHub account when it asks. That's all for now; each app gets connected in the loop below.

### 4. Optional: use desktop VS Code instead of the browser

Install the **GitHub Codespaces** extension in desktop VS Code. Then from any Codespace, open the menu (top-left) and choose **Open in VS Code Desktop**. Same container, your normal editor window.

---

## Part 2: The loop for every app

1. **Create the repo.** On `app-starter`, click **Use this template → Create a new repository**. Name it after the app (for example, `race-planner`).
2. **Give the Claude Code secret access.** Profile **Settings → Codespaces → Secrets → CLAUDE_CODE_OAUTH_TOKEN → Update**, and add the new repo.
3. **Open a Codespace.** **Code → Codespaces → Create codespace on main**. The first build takes a few minutes.
4. **Confirm the baseline is green.** In the terminal, run `pytest -q`. You should see 2 passed.
5. **Add app keys to `.env`.** The container creates `.env` from `.env.example` for you. Put the app's Anthropic, Stripe, and other keys there. It's gitignored.
   - **Important:** don't store `ANTHROPIC_API_KEY` as a Codespaces secret. Codespaces secrets become environment variables for the whole container, and Claude Code would pick that key up and bill your API account instead of using your Claude plan. Keeping it in `.env` means only the app reads it.
6. **Start Claude Code.** Run `claude`, then paste the prompt for that app from Part 4. Each prompt asks Claude for a plan first, so review it and say go.
7. **Review and merge.** Claude works on a branch and opens a pull request. GitHub Actions runs lint and tests on it. Review the changes in the PR, and merge when the `tests` check is green.
8. **First deploy (once per app).** In Render, choose **New → Blueprint**, pick the repo, fill in any secret values it asks for, and click **Apply**. From then on, every merge to `main` deploys automatically, but only after tests pass, because `render.yaml` sets `autoDeployTrigger: checksPass`.
9. **Optional but recommended:** in the repo's **Settings → Branches**, add a rule for `main` that requires the `tests` check to pass before merging.
10. **Stop the Codespace when you're done.** Codespaces stop on their own after sitting idle, but stopping manually saves your free hours. Delete old Codespaces you no longer need, since they count against storage.

Before step 6, replace `APP_NAME` in `render.yaml` and `.devcontainer/devcontainer.json` with the repo name. (Or just tell Claude Code to do it as the first step.)

---

## Part 3: Render free-tier gotchas

- **Free web services sleep** after 15 minutes without traffic. The next visitor waits while it wakes up. Fine for portfolio demos, not for anything people pay for.
- **Free Postgres databases expire after 30 days**, data included. For any app with real users or data you care about, upgrade that database to a paid plan before day 30. Apps that don't need a database (the race planner and materials estimator) avoid this entirely.
- Render sets the port through `$PORT`, and the template already binds to it. If you ever see a "no open ports detected" error, something overrode the start command.

---

## Part 4: Claude Code prompts

Each prompt assumes `CLAUDE.md` is in the repo, so it doesn't repeat the stack or coding rules.

### Existing repos (retrofit)

For civic-app and DevDojo, open a Codespace on the existing repo and paste the matching prompt. Claude Code copies in the kit and reconciles it with what's already there.

#### 1. Who Represents Me (civic-app)

```
This is an existing Flask app (Who Represents Me). First, clone
https://github.com/khrystianc/app-starter into /tmp/starter and copy in
.devcontainer/, .github/workflows/tests.yml, render.yaml, CLAUDE.md,
pyproject.toml, requirements-dev.txt, and tests/conftest.py. Then read CLAUDE.md.

Reconcile the kit with the existing app without changing app behavior:
- Keep the existing app factory, blueprints, and data/ files. Add /health if missing.
- Merge requirements. Don't drop anything the app uses.
- Update render.yaml to match the existing Render service and database names so
  Render updates them instead of creating duplicates. Ask me for the names if
  they aren't in the repo.
- Write tests for /health, /api/lookup (mock Census and OpenStates; no network),
  the office-explainer route, auth (signup/login/logout), and the Stripe donation
  webhook (mock signature verification).
- The basic lookup must stay free and ungated. Add a test that proves it.

Give me a plan first. After I approve, work on a branch, get ruff and pytest
passing, and open a PR with a plain-English summary.
```

#### 2. DevDojo

```
This is an existing Flask app (DevDojo, an AI coding coach with Duolingo-style
gamification). First, clone https://github.com/khrystianc/app-starter into
/tmp/starter and copy in .devcontainer/, .github/workflows/tests.yml,
render.yaml, CLAUDE.md, pyproject.toml, requirements-dev.txt, and
tests/conftest.py. Then read CLAUDE.md.

Reconcile the kit with the existing app without changing behavior:
- Keep the existing structure. Add /health if missing. Merge requirements.
- Make the Anthropic model come from ANTHROPIC_MODEL in config. Remove any
  hardcoded model string.
- Match render.yaml to the existing Render service and database names (ask me
  if they aren't in the repo).
- Write tests for the gamification rules: XP curve (100 XP for Level 1, each
  level needs 20% more), streak increment and reset, streak freeze, hearts
  (lose one per wrong answer, refill daily), and the free-tier daily message
  limit. Use a frozen clock for anything date-based.
- Test that the coach endpoint fails closed with a clear error when
  ANTHROPIC_API_KEY is missing, and that Stripe webhook handling works with
  signature verification mocked. Mock the Anthropic client everywhere.

Give me a plan first. After I approve, work on a branch, get ruff and pytest
passing, and open a PR with a plain-English summary.
```

### New apps (start from the template)

#### 3. Run-Together Race Planner + Galloway pacing API

```
Read CLAUDE.md. Rename APP_NAME to race-planner in render.yaml and
devcontainer.json. This app needs no database: remove the databases block and
DATABASE_URL from render.yaml.

Build a race planner for couples or groups who want to finish together.
- Input: each runner's recent pace (or a recent race time), run:walk ratio
  (e.g. 6:1, 5:1), race distance, optional course GPX upload, race date and
  location.
- Output: one shared run/walk plan paced to the slower runner, adjusted for
  elevation (parse GPX with gpxpy) and forecast heat (Open-Meteo, free, no key).
- Pages: a simple form, a results page, and a printable pace band.
- Public JSON API: POST /api/v1/plan with the same inputs, returns the plan.
  Document it on an /api page.

Tests: interval math against hand-calculated cases, slower runner sets the pace,
a small GPX fixture file, weather mocked, and API input validation (bad paces,
zero distance, unknown ratios).

Give me a plan first, then work on a branch and open a PR.
```

#### 4. Training Readiness Dashboard

```
Read CLAUDE.md. Rename APP_NAME to readiness-dashboard. Keep the database.

Build a private, single-user training readiness dashboard.
- Add Flask-Login with one account. All pages require login; this is health data.
- Pull HRV, resting heart rate, and sleep from the Oura API. Look up Oura's
  current authentication method in their docs rather than assuming.
- Import workouts from an Apple Health export.zip upload (parse export.xml).
- Planned workouts are entered manually (Runna has no public API).
- Store everything in Postgres with a clean schema and migrations
  (Flask-Migrate).
- Dashboard: trends for HRV and resting HR, weekly training load vs. recovery,
  and a flag when recovery lags load.
- Nightly sync: a protected POST /tasks/sync endpoint, called by a scheduled
  GitHub Actions workflow using a SYNC_SECRET. (Render cron jobs aren't free.)

Tests: parsing a small sample export.xml fixture, Oura responses mocked, the
recovery-flag logic, sync endpoint rejects missing or wrong secrets, and every
page redirects to login when logged out.

Give me a plan first, then work on a branch and open a PR.
```

#### 5. Creator Pillar Analytics (@coupleofclarks)

```
Read CLAUDE.md. Rename APP_NAME to creator-analytics. Keep the database.

Build a dashboard for my content channel.
- Flask-Login, single account.
- Pull video stats from the YouTube Data API v3.
- Pull post stats from the Instagram Graph API (requires a creator or business
  account linked to a Facebook Page; walk me through the Meta app setup).
- TikTok: manual entry or CSV upload, since its API is restricted.
- Tag every post with one pillar: pediatric health, couples running/fitness,
  family/role-reversal, or veteran life.
- Views: performance by pillar over time, top posts per pillar, and a media kit
  page with current follower counts and engagement for brand pitches.

Tests: API responses mocked, CSV import with good and malformed rows, pillar
aggregation math, and the media kit numbers.

Give me a plan first, then work on a branch and open a PR.
```

#### 6. Household OPORD

```
Read CLAUDE.md. Rename APP_NAME to household-opord. Keep the database.

Build a family operations board, modeled on a military operations order.
- Two users in one household (me and my wife), Flask-Login.
- Google Calendar API with OAuth for both accounts. Keep the Google app in
  testing mode with us as test users.
- Sections: today's schedule from both calendars, meals, chores with owners,
  and reusable gear checklists (diaper bag, race weekend, travel day).
- A morning brief generated with the Anthropic API from the day's data, written
  in OPORD format: situation, mission, execution, logistics, command/signal.

Tests: calendar API mocked, checklist CRUD, chore assignment, brief generation
with the Anthropic client mocked, and one household can't see another's data.

Give me a plan first, then work on a branch and open a PR.
```

#### 7. DIY Materials Estimator API

```
Read CLAUDE.md. Rename APP_NAME to materials-api. No database: remove the
databases block and DATABASE_URL from render.yaml.

Build a JSON API that estimates materials for DIY projects. This is my QA
showcase, so testing is the main event.
- Endpoints: /api/v1/turf (rolls, seam length, infill pounds), /api/v1/deck-tiles
  (tile count by tile size), /api/v1/gravel (cubic yards and tons by depth).
- Inputs in feet or meters, configurable waste factor with a sensible default.
- OpenAPI docs served at /docs.
- Clear 400 errors for bad input.

Tests: parametrized cases for each calculator (including 1,200 sq ft of turf
and a 10x20 deck of 12x12 tiles as real-world checks), unit conversions,
rounding up to whole units, and invalid input (negative, zero, missing,
non-numeric). Add pytest-cov and fail CI if coverage drops below 95%.

Give me a plan first, then work on a branch and open a PR.
```

#### 8. Military-to-Tech Translator

```
Read CLAUDE.md. Rename APP_NAME to mil2tech. Keep the database.

Build a tool that turns military experience into civilian tech resume bullets.
- Paste duties, evaluation bullets, or a job description. Rewrite them as
  civilian bullets with the Anthropic API, keeping numbers and scope.
- Show a warning before input: never paste SSNs, DoD ID numbers, or classified
  information. Strip anything that looks like an SSN before sending.
- Job matching: the user pastes a job posting, and the app highlights which
  bullets match its requirements and what's missing.
- Optional accounts (Flask-Login) to save bullet libraries.

Tests: Anthropic client mocked, the SSN-stripping filter, the match scoring,
and saved bullets are private to each user.

Give me a plan first, then work on a branch and open a PR.
```

#### 9. Annotation QA Toolkit

```
Read CLAUDE.md. Rename APP_NAME to annotation-qa. Keep the database.

Build a tool that measures annotation quality.
- Upload a CSV: annotator, item, label (or numeric score), timestamp.
- Compute Cohen's kappa (two annotators), Fleiss' kappa and Krippendorff's alpha
  (many), per-annotator agreement with the majority, outlier annotators, and
  drift over time.
- Keep the math in a plain Python module with no Flask imports, so it's
  testable on its own. Flask provides the upload page, results, and a JSON API.
- Include a synthetic sample dataset. Real client annotation data should never
  be uploaded; say so on the upload page.

Tests: each metric against published textbook examples, edge cases (perfect
agreement, all one label, missing ratings), and malformed CSVs.

Give me a plan first, then work on a branch and open a PR.
```

#### 10. Nap-Window Game Picker

```
Read CLAUDE.md. Rename APP_NAME to nap-window. Keep the database.

Build a handheld game picker for short play sessions.
- Flask-Login. Users build a backlog by searching the IGDB API (Twitch client
  credentials: TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET).
- Each game stores a session-length estimate: IGDB time-to-beat data where
  available, otherwise the user's own estimate.
- Enter how much time you have (e.g. 40 minutes) and get games that fit, with
  a note on where you left off.

Tests: IGDB responses mocked, token refresh logic, the picker's filtering, and
backlogs are private to each user.

Give me a plan first, then work on a branch and open a PR.
```

---

## Suggested build order

1. **Retrofit civic-app and DevDojo first.** They already exist, so this proves the whole loop end to end.
2. **Materials Estimator API.** Small, no database, and it gets your testing discipline sharp.
3. **Race Planner,** then **Readiness Dashboard.** They pair well for interviews and for the channel.
4. The rest in whatever order keeps you interested.
