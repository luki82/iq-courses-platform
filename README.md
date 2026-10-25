# MindGrowth -- IQ Tests & Courses Platform

A Django site where **everything is free**, kept online by optional donations:

- **IQ Tests** (`iqtest` app) -- category-based multiple-choice tests,
  including the timed 30-question Full IQ Assessment. Anyone can take any
  test, with or without an account, and always gets the full breakdown
  (estimated IQ score, correct answers, explanations).
- **Courses** (`courses` app) -- courses made of modules and lessons, all
  free once you enrol.
- **IELTS Preparation** (`ielts` app) -- lesson modules across Reading,
  Listening, Writing, and Speaking in three tiers, all free.
- **Billing** (`billing` app) -- a Donate page using Stripe Checkout for
  one-off donations (A$5 / 10 / 20 / 50 or a custom amount). Donating
  unlocks nothing; it just helps pay for hosting.
- **Accounts** (`accounts` app) -- signup/login, so learners can track their
  courses and see their test results on any device.

The old Premium plans, paid test passes and premium fields are still in the
database (and in Django admin) as a record of past payments, but no code
checks them any more. Old links (`/billing/pricing/`, paid-test private links)
redirect to the right place.

---

## 1. Local setup

Requirements: Python 3.11+ and pip. From the project folder:

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

copy .env.example .env      # Windows
# cp .env.example .env      # macOS/Linux
```

Open `.env` and at minimum set `SECRET_KEY` to something random (the file
tells you how to generate one). Leave `DATABASE_URL` empty to use a local
SQLite database automatically.

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Optional: sample IQ questions, plus the real courses and IELTS lessons
# (build.sh runs all of these except seed_iqtest on every Render deploy)
python manage.py seed_iqtest
python manage.py seed_english_esl
python manage.py seed_workplace_english
python manage.py seed_school_english
python manage.py load_ielts_lesson ielts_content/

python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Admin is at `/admin/`.

### Adding real content

Use `/admin/` to add:
- **IQ tests app > Categories / Questions / Choices** -- write your own test
  bank.
- **Courses app > Courses / Modules / Lessons** -- build out your course
  content.
- **IELTS app > IELTS lessons / questions** -- add lessons directly in admin,
  or load them from JSON (see section 5 below).

---

## 2. Stripe setup (donations)

Donations are charged directly from the amount the visitor picks, so you
don't need to create Products or Prices in Stripe. Each donation appears in
the Stripe dashboard under Payments with the description "iQ donation".

To switch donations on, set these environment variables on Render (or in
`.env` locally):

1. `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` -- Stripe dashboard >
   Developers > API keys (`pk_...` / `sk_...`).
2. Optional: `STRIPE_WEBHOOK_SECRET`. Donations don't need the webhook; it
   only finishes off an IQ test pass bought just before tests went free. If
   you already have a webhook pointed at `/billing/webhook/`, leave it as is.

Until `STRIPE_SECRET_KEY` is set, the Donate page shows a friendly "being set
up" note instead of the donation form.

Use test-mode keys first and donate with card `4242 4242 4242 4242` (any
future expiry, any CVC), then swap in live keys.

---

## 3. Pushing to GitHub (from VS Code)

From the project folder:

```bash
git init
git add .
git commit -m "Initial commit: IQ test + courses platform"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

(Or use VS Code's Source Control panel -- Initialize Repository, stage all,
commit, then "Publish Branch" to push to GitHub.) `.env`, `db.sqlite3`, and
`venv/` are already excluded via `.gitignore`, so secrets and your local
database won't be pushed.

---

## 4. Deploying to Render

This repo includes a `render.yaml` (Render's "Blueprint" format), which
provisions a free Postgres database and a web service together.

1. Push this repo to GitHub (step 3).
2. In the Render dashboard: **New > Blueprint**, connect your GitHub repo,
   and Render will read `render.yaml` and propose the `iq-courses-platform`
   web service plus the `iq-courses-db` Postgres database.
3. Before the first deploy, fill in the Stripe env vars it leaves blank
   (`STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`) in the
   service's Environment tab. `SECRET_KEY` and `DATABASE_URL` are generated
   for you automatically.
4. Deploy. Render runs `build.sh` (installs dependencies, collects static
   files, runs migrations) then starts `gunicorn config.wsgi:application`.
5. Once live, create an admin user for the production site. Render's free
   web services don't include Shell/SSH access, so instead of running
   `createsuperuser` in a shell, set these three env vars on the service
   (Environment tab) and redeploy -- `build.sh` runs
   `python manage.py create_admin` automatically, which creates the account
   (or, if it already exists, updates its password when
   `DJANGO_SUPERUSER_RESET_PASSWORD=1` is also set):
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_EMAIL`
   - `DJANGO_SUPERUSER_PASSWORD`

   (If you're on a paid instance type with Shell access, `python manage.py
   createsuperuser` in the Shell tab still works too.)
6. Update your Stripe webhook endpoint to point at your real Render URL
   (`https://<your-service>.onrender.com/billing/webhook/`).

If you'd rather configure the service manually instead of using the
Blueprint: Build Command `./build.sh`, Start Command
`gunicorn config.wsgi:application`, and add a Postgres instance, then copy
its Internal Database URL into `DATABASE_URL`.

**Note on uploaded images:** Render's free web service disk is ephemeral, so
`ImageField` uploads (question images, course covers) won't survive a
redeploy in production. For a real launch, wire up a cloud storage backend
(e.g. `django-storages` with S3, Cloudinary, or Backblaze B2) for
`MEDIA_ROOT`. Not needed if you stick to text content.

---

## 5. Loading IELTS lesson content

IELTS lesson modules (Reading/Listening/Writing/Speaking, split into
TIER_1/2/3) are generated as JSON -- see `ielts_content/*.json` for examples
-- and loaded with:

```bash
python manage.py load_ielts_lesson ielts_content/renewable_energy_task1.json
python manage.py load_ielts_lesson ielts_content/paper_recycling_process.json
python manage.py load_ielts_lesson ielts_content/autonomous_vehicles_reading.json
```

Re-running the same file skips it (a lesson with that title already exists);
pass `--update` to delete and reload it instead. Diagrams render client-side:
`diagram_type: "chartjs"` renders via Chart.js, `"mermaid"` via Mermaid.js,
and `"cloudinary"` displays `diagram_config.image_url` directly (this
project doesn't have Cloudinary wired in -- point that URL at wherever you
actually host the image). Questions use Alpine.js for a click-to-reveal
answer/explanation panel.

---

## 6. Project layout

```
config/         Project settings, root URLs, WSGI/ASGI
accounts/       Signup/login, Profile (premium status, free-usage counters)
core/           Home page
iqtest/         Categories, Questions, Choices, TestAttempt, Answer, views, templates
courses/        Course, Module, Lesson, Enrollment, LessonProgress, views, templates
ielts/          IELTSLesson, IELTSQuestion (Reading/Listening/Writing/Speaking, tiered), views, templates
billing/        Plan, Purchase, Stripe Checkout + webhook
templates/      Shared base.html + each app's templates
static/         CSS (Bootstrap 5 via CDN + a small custom stylesheet)
ielts_content/  Example lesson JSON files for `load_ielts_lesson`
```

## 7. Where the old paywall used to be

Everything is free, so none of these block anyone any more:

- `iqtest.views.take_test` -- one free flow for every test, for guests and
  members. Guests' results are tied to their browser session; members' to
  their account. Results locked under the old rules unlock the next time
  they're opened.
- `courses.views.lesson_detail` -- any enrolled learner can open any lesson.
- `ielts.views.lesson_detail` -- every tier is open to logged-in learners.
- `billing.views` -- the Donate page and Stripe checkout for donations.

If you ever want paid content again, `Profile.has_premium_access`, `Plan`,
`Purchase` and `TestPass` are still in the models to build on.
