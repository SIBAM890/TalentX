"""
TalentX – Timeline Engine
Generates year-by-year career roadmaps based on career path data.
"""
import logging
from app.config import CAREER_PATHS_PATH
from app.utils import load_json
from app.models import TimelineMilestone, TimelineResponse

logger = logging.getLogger("talentx.timeline")

_career_paths: dict = {}


def _get_career_paths() -> dict:
    global _career_paths
    if not _career_paths:
        _career_paths = load_json(CAREER_PATHS_PATH)
        logger.info(f"Loaded {len(_career_paths)} career paths")
    return _career_paths


class TimelineEngine:
    """Generates year-by-year career path timelines."""

    def get_timeline(self, career_path_key: str, current_skills: list[str] = None) -> TimelineResponse:
        """Return a timeline for a given career path."""
        paths = _get_career_paths()
        current_skills_lower = {s.lower() for s in (current_skills or [])}

        if career_path_key not in paths:
            # Fuzzy match
            for key in paths:
                if career_path_key.lower() in key or key in career_path_key.lower():
                    career_path_key = key
                    break
            else:
                return self._generic_timeline(career_path_key)

        path = paths[career_path_key]
        raw_milestones = path.get("yearly_milestones", [])

        milestones = []
        for m in raw_milestones:
            year = m.get("year", 1)
            # If user already has skills relevant to this milestone, mark earlier ones as done
            status = "pending"
            if year == 1 and current_skills_lower:
                required = {s.lower() for s in path.get("skills_required", [])}
                if len(current_skills_lower & required) >= len(required) * 0.5:
                    status = "in-progress"
            milestones.append(TimelineMilestone(
                year=year,
                milestone=m.get("milestone", ""),
                action=m.get("action", ""),
                status=status,
            ))

        return TimelineResponse(
            career_path=career_path_key,
            title=path.get("title", career_path_key.replace("_", " ").title()),
            milestones=milestones,
            total_duration=path.get("timeline", "1–3 years"),
            expected_salary=path.get("avg_salary", "₹6–15 LPA"),
        )

    def _generic_timeline(self, path_name: str) -> TimelineResponse:
        """Generate a generic 5-year timeline when specific path not found."""
        milestones = [
            TimelineMilestone(year=1, milestone="Build foundational skills", action="Take online courses, build 2 projects", status="pending"),
            TimelineMilestone(year=2, milestone="Internship or first project", action="Apply to internships, freelance projects", status="pending"),
            TimelineMilestone(year=3, milestone="Entry-level role", action="Apply to companies, leverage network", status="pending"),
            TimelineMilestone(year=4, milestone="Develop specialization", action="Get certifications, deepen expertise", status="pending"),
            TimelineMilestone(year=5, milestone="Mid-level role or leadership", action="Mentor others, take ownership of projects", status="pending"),
        ]
        return TimelineResponse(
            career_path=path_name,
            title=path_name.replace("_", " ").title(),
            milestones=milestones,
            total_duration="3–5 years",
            expected_salary="₹6–20 LPA",
        )

    def list_available_paths(self) -> list[dict]:
        """Return all available career paths."""
        paths = _get_career_paths()
        return [
            {
                "key": key,
                "title": data.get("title", key),
                "avg_salary": data.get("avg_salary", "N/A"),
                "demand": data.get("demand", "N/A"),
            }
            for key, data in paths.items()
        ]


_timeline_instance = None


def get_timeline_engine() -> TimelineEngine:
    global _timeline_instance
    if _timeline_instance is None:
        _timeline_instance = TimelineEngine()
    return _timeline_instance
