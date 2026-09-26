import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from ielts.models import IELTSLesson, IELTSQuestion


class Command(BaseCommand):
    help = (
        "Loads IELTS lesson module(s) from JSON (matching the Claude-generated schema: "
        "module_title, tier, skill, lesson_title, passage_or_prompt, diagram_type, "
        "diagram_config, questions[], band_9_sample) into the database. "
        "Accepts either a single JSON file or a directory of JSON files. "
        "Safe to run repeatedly (e.g. on every deploy) -- a lesson with a title that "
        "already exists is skipped unless --update is passed. "
        "Usage: python manage.py load_ielts_lesson ielts_content/ "
        "or: python manage.py load_ielts_lesson ielts_content/one_lesson.json"
    )

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str, help="Path to a lesson JSON file or a directory of them.")
        parser.add_argument(
            "--update",
            action="store_true",
            help="If a lesson with the same title already exists, replace it instead of skipping.",
        )

    def handle(self, *args, **options):
        path = Path(options["json_path"])
        if not path.exists():
            raise CommandError(f"Path not found: {path}")

        if path.is_dir():
            files = sorted(path.glob("*.json"))
            if not files:
                self.stdout.write(self.style.WARNING(f"No .json files found in {path}"))
                return
            loaded, skipped, failed = 0, 0, 0
            for file in files:
                try:
                    result = self._load_file(file, options["update"])
                    if result:
                        loaded += 1
                    else:
                        skipped += 1
                except CommandError as exc:
                    failed += 1
                    self.stderr.write(self.style.ERROR(f"{file.name}: {exc}"))
            self.stdout.write(
                self.style.SUCCESS(f"Done: {loaded} loaded, {skipped} skipped, {failed} failed.")
            )
        else:
            self._load_file(path, options["update"])

    def _load_file(self, path: Path, update: bool) -> bool:
        """Loads a single JSON file. Returns True if a lesson was created, False if skipped."""
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise CommandError(f"Invalid JSON in {path}: {exc}")

        required = ["module_title", "tier", "skill", "lesson_title", "passage_or_prompt", "questions"]
        missing = [key for key in required if key not in data]
        if missing:
            raise CommandError(f"JSON is missing required key(s): {', '.join(missing)}")

        valid_tiers = dict(IELTSLesson.TIER_CHOICES)
        valid_skills = dict(IELTSLesson.SKILL_CHOICES)
        if data["tier"] not in valid_tiers:
            raise CommandError(f"Unknown tier '{data['tier']}'. Expected one of: {', '.join(valid_tiers)}")
        if data["skill"] not in valid_skills:
            raise CommandError(f"Unknown skill '{data['skill']}'. Expected one of: {', '.join(valid_skills)}")

        existing = IELTSLesson.objects.filter(title=data["lesson_title"]).first()
        if existing:
            if not update:
                self.stdout.write(
                    self.style.WARNING(
                        f"Lesson '{data['lesson_title']}' already exists (id={existing.pk}) -- "
                        "skipping. Pass --update to replace it."
                    )
                )
                return False
            existing.delete()

        lesson = IELTSLesson.objects.create(
            module_title=data["module_title"],
            tier=data["tier"],
            skill=data["skill"],
            title=data["lesson_title"],
            passage_or_prompt=data["passage_or_prompt"],
            diagram_type=data.get("diagram_type", "none"),
            diagram_config=data.get("diagram_config") or {},
            band_9_sample=data.get("band_9_sample", ""),
        )

        questions = []
        for i, q in enumerate(data["questions"], start=1):
            for key in ("prompt", "question_type", "correct_answer", "explanation"):
                if key not in q:
                    lesson.delete()
                    raise CommandError(f"Question {i} in {path.name} is missing required key '{key}'")
            questions.append(
                IELTSQuestion(
                    lesson=lesson,
                    order=q.get("id", i),
                    prompt=q["prompt"],
                    question_type=q["question_type"],
                    options=q.get("options") or [],
                    correct_answer=q["correct_answer"],
                    explanation=q["explanation"],
                )
            )
        IELTSQuestion.objects.bulk_create(questions)

        self.stdout.write(
            self.style.SUCCESS(
                f"Loaded lesson '{lesson.title}' ({lesson.tier}/{lesson.skill}) with "
                f"{len(questions)} question(s)."
            )
        )
        return True