# MindGrowth -- IQ Tests & Courses Platform

A Django site with two products behind a single freemium paywall:

- **IQ Tests** (`iqtest` app) -- category-based multiple-choice tests. Every
  user gets a limited number of full-detail free attempts (score breakdown,
  explanations, estimated IQ score); after that -- or for Premium-only
  categories -- they need to upgrade.
- **Courses** (`courses` app) -- courses made of modules and lessons. Each
  course's first module is a free preview; the rest requires Premium.
- **Billing** (`billing` app) -- Stripe Checkout integration that unlocks
  Premium access for a configurable number of days per purchase.
- **Accounts** (`accounts` app) -- signup/login and a `Profile` model that
  tracks each user's premium status and free-attempt usage.

The freemium rule is centered on one property: `request.user.profile.has_premium_access`.
Both apps check it (plus their own free-preview flags) before showing paid content.

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

# Optional: adds a couple of sample IQ categories/questions and a sample course
python manage.py seed_iqtest
python manage.py seed_courses

python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Admin is at `/admin/`.

### Adding real content

Use `/admin/` to add:
- **IQ tests app > Categories / Questions / Choices** -- write your own test
  bank. Mark a Category `is_premium` to make the whole category paid-only.
- **Courses app > Courses / Modules / Lessons** -- build out your course
  content. Tick a Module's `is_free_preview` to make it free; leave it
  unticked to require Premium.
- **Billing app > Plans** -- create at least one Plan (name, price for
  display, duration in days). You'll attach it to a real Stripe Price next.

---

## 2. Stripe setup (payments)

1. Create a [Stripe account](https://dashboard.stripe.com/register) (test
   mode is fine to start).
2. In the Stripe dashboard, create a **Product** (e.g. "Premium Access") with
   a one-time **Price** (e.g. $9.99). Copy its Price ID (`price_...`).
3. In Django admin, edit your Plan and paste that Price ID into
   `stripe_price_id`.
4. In `.env` (locally) or Render's environment variables (in production), set:
   - `STRIPE_PUBLIC_KEY` -- from Stripe dashboard > Developers > API keys
   - `STRIPE_SECRET_KEY` -- same page
   - `STRIPE_WEBHOOK_SECRET` -- see next step
5. Add a webhook endpoint in Stripe pointing at
   `https://<your-domain>/billing/webhook/`, subscribed to the
   `checkout.session.completed` event. Stripe will show you a signing secret
   (`whsec_...`) -- that's `STRIPE_WEBHOOK_SECRET`.

Until these are set, the "Upgrade" button shows a friendly "payments aren't
configured yet" message instead of erroring.

To test locally, use the [Stripe CLI](https://stripe.com/docs/stripe-cli):
`stripe listen --forward-to localhost:8000/billing/webhook/`.

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
5. Once live, create an admin user for the production site:
   Render dashboard > your service > **Shell** tab, then:
   ```bash
   python manage.py createsuperuser
   ```
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

## 5. Project layout

```
config/         Project settings, root URLs, WSGI/ASGI
accounts/       Signup/login, Profile (premium status, free-usage counters)
core/           Home page
iqtest/         Categories, Questions, Choices, TestAttempt, Answer, views, templates
courses/        Course, Module, Lesson, Enrollment, LessonProgress, views, templates
billing/        Plan, Purchase, Stripe Checkout + webhook
templates/      Shared base.html + each app's templates
static/         CSS (Bootstrap 5 via CDN + a small custom stylesheet)
```

## 6. Where the freemium rule lives

- `accounts.models.Profile.has_premium_access` -- the single source of truth
  for "is this user currently paying".
- `iqtest.views.take_test` -- computes `detail_unlocked` per attempt from
  `FREE_TEST_ATTEMPTS_LIMIT` (in `.env`) and the user's premium status;
  `Category.is_premium` gates premium-only categories entirely.
- `courses.views.lesson_detail` / `course_detail.html` -- a lesson is
  visible if `lesson.is_free` (its module is a free preview) or the user has
  premium access.

Adjust `FREE_TEST_ATTEMPTS_LIMIT`, which categories/modules are marked
premium, and Plan pricing/duration to match whatever access model you want.
