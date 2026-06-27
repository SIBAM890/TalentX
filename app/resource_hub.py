"""
TalentX – Resource Hub
Recommends courses, certifications, and communities based on career path.
"""
import logging
from app.config import CAREER_PATHS_PATH
from app.utils import load_json

logger = logging.getLogger("talentx.resource_hub")

RESOURCES = {
    "python": [
        {"name": "Python for Everybody (Coursera)", "url": "https://coursera.org/learn/python", "type": "course", "cost": "Free audit", "platform": "Coursera"},
        {"name": "100 Days of Code: Python Bootcamp (Udemy)", "url": "https://udemy.com", "type": "course", "cost": "₹449", "platform": "Udemy"},
        {"name": "CS50P – Python (Harvard)", "url": "https://cs50.harvard.edu/python", "type": "course", "cost": "Free", "platform": "edX"},
    ],
    "machine_learning": [
        {"name": "ML Specialization – Andrew Ng (Coursera)", "url": "https://coursera.org/specializations/machine-learning-introduction", "type": "course", "cost": "Free audit", "platform": "Coursera"},
        {"name": "fast.ai Practical Deep Learning", "url": "https://fast.ai", "type": "course", "cost": "Free", "platform": "fast.ai"},
        {"name": "Kaggle Learn ML Courses", "url": "https://kaggle.com/learn", "type": "course", "cost": "Free", "platform": "Kaggle"},
    ],
    "nlp": [
        {"name": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course", "type": "course", "cost": "Free", "platform": "Hugging Face"},
        {"name": "Natural Language Processing Specialization (Coursera)", "url": "https://coursera.org/specializations/natural-language-processing", "type": "course", "cost": "Free audit", "platform": "Coursera"},
    ],
    "sql": [
        {"name": "SQL for Data Science (Coursera)", "url": "https://coursera.org/learn/sql-for-data-science", "type": "course", "cost": "Free audit", "platform": "Coursera"},
        {"name": "SQLZoo Interactive SQL", "url": "https://sqlzoo.net", "type": "practice", "cost": "Free", "platform": "SQLZoo"},
    ],
    "cloud": [
        {"name": "AWS Cloud Practitioner Essentials", "url": "https://aws.amazon.com/training", "type": "certification", "cost": "Free", "platform": "AWS"},
        {"name": "Google Cloud Digital Leader", "url": "https://cloud.google.com/certification", "type": "certification", "cost": "₹12,000", "platform": "GCP"},
        {"name": "Azure Fundamentals AZ-900", "url": "https://learn.microsoft.com/azure", "type": "certification", "cost": "₹4,500", "platform": "Microsoft"},
    ],
    "gate_prep": [
        {"name": "GATE 2025 Preparation – NPTEL", "url": "https://nptel.ac.in", "type": "course", "cost": "Free", "platform": "NPTEL"},
        {"name": "Made Easy GATE Study Material", "url": "https://madeeasy.in", "type": "course", "cost": "₹3,000–8,000", "platform": "Made Easy"},
        {"name": "GATE Overflow Practice Problems", "url": "https://gateoverflow.in", "type": "practice", "cost": "Free", "platform": "GATE Overflow"},
    ],
    "dsa": [
        {"name": "LeetCode (DSA Practice)", "url": "https://leetcode.com", "type": "practice", "cost": "Free/Premium", "platform": "LeetCode"},
        {"name": "Striver's DSA Sheet", "url": "https://takeuforward.org", "type": "resource", "cost": "Free", "platform": "TakeUForward"},
        {"name": "Data Structures & Algorithms Specialization (Coursera)", "url": "https://coursera.org/specializations/data-structures-algorithms", "type": "course", "cost": "Free audit", "platform": "Coursera"},
    ],
    "communities": [
        {"name": "r/cscareerquestionsINDIA (Reddit)", "url": "https://reddit.com/r/cscareerquestionsINDIA", "type": "community", "cost": "Free", "platform": "Reddit"},
        {"name": "Devfolio (India Hackathons)", "url": "https://devfolio.co", "type": "community", "cost": "Free", "platform": "Devfolio"},
        {"name": "Unstop (Competitions + Jobs)", "url": "https://unstop.com", "type": "platform", "cost": "Free", "platform": "Unstop"},
        {"name": "LinkedIn India Tech Communities", "url": "https://linkedin.com", "type": "community", "cost": "Free", "platform": "LinkedIn"},
    ],
}

CAREER_RESOURCE_MAP = {
    "ai_ml_engineer": ["python", "machine_learning", "nlp", "cloud", "communities"],
    "software_developer": ["python", "dsa", "sql", "cloud", "communities"],
    "data_analyst": ["sql", "python", "machine_learning", "communities"],
    "data_engineer": ["python", "sql", "cloud", "communities"],
    "devops_engineer": ["cloud", "python", "communities"],
    "cybersecurity_analyst": ["cloud", "communities"],
    "gate": ["gate_prep", "dsa", "communities"],
    "default": ["python", "dsa", "communities"],
}


class ResourceHub:
    """Recommends learning resources based on career path or skills needed."""

    def get_resources(self, career_key: str = "default", skills_needed: list[str] = None) -> dict:
        """Return curated resources for a career path or skill list."""
        resource_keys = CAREER_RESOURCE_MAP.get(career_key, CAREER_RESOURCE_MAP["default"])

        # Add skill-specific resources if needed
        if skills_needed:
            for skill in skills_needed:
                skill_lower = skill.lower()
                if "python" in skill_lower:
                    resource_keys.append("python")
                elif "sql" in skill_lower:
                    resource_keys.append("sql")
                elif "ml" in skill_lower or "machine" in skill_lower:
                    resource_keys.append("machine_learning")
                elif "nlp" in skill_lower or "natural language" in skill_lower:
                    resource_keys.append("nlp")
                elif "cloud" in skill_lower or "aws" in skill_lower:
                    resource_keys.append("cloud")

        resource_keys = list(set(resource_keys))  # deduplicate
        result = {}
        for key in resource_keys:
            if key in RESOURCES:
                result[key.replace("_", " ").title()] = RESOURCES[key]

        return {
            "career_path": career_key,
            "resource_categories": result,
            "total_resources": sum(len(v) for v in result.values()),
            "tip": "Start with free resources. Build projects immediately after completing courses — projects get you hired, not certificates alone.",
        }

    def get_all_categories(self) -> list[str]:
        return list(RESOURCES.keys())


_hub_instance = None


def get_resource_hub() -> ResourceHub:
    global _hub_instance
    if _hub_instance is None:
        _hub_instance = ResourceHub()
    return _hub_instance
