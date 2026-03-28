"""Rule-based constraint extractor for time and effort from free text."""

import re


class ConstraintExtractor:
    """Extracts time and effort constraints from natural language text."""

    # Regex for explicit minutes, e.g. "20 minutes", "45 mins"
    _MINUTES_RE = re.compile(r"(\d+)\s*(?:min|minute|minutes|mins)\b", re.IGNORECASE)

    # Regex for explicit hours, e.g. "2 hours"
    _HOURS_RE = re.compile(r"(\d+)\s*(?:hour|hours|hr|hrs)\b", re.IGNORECASE)

    # Phrase patterns (checked before keywords)
    _TIME_PHRASES = [
        (re.compile(r"under\s+an\s+hour", re.IGNORECASE), "medium"),
        (re.compile(r"under\s+30", re.IGNORECASE), "short"),
    ]

    # Keyword -> time mapping
    _TIME_KEYWORDS = {
        "quick": "short",
        "fast": "short",
        "speedy": "short",
        "moderate": "medium",
        "slow": "long",
        "all day": "long",
        "hours": "long",
    }

    # Keyword -> effort mapping
    _EFFORT_KEYWORDS = {
        "easy": "low",
        "simple": "low",
        "beginner": "low",
        "effortless": "low",
        "basic": "low",
        "lazy": "low",
        "moderate": "medium",
        "intermediate": "medium",
        "complex": "high",
        "challenging": "high",
        "advanced": "high",
        "elaborate": "high",
        "gourmet": "high",
    }

    def __init__(self) -> None:
        pass

    def extract(self, text: str) -> dict:
        """Extract time and effort constraints from free text.

        Returns:
            dict with keys "time" and "effort", each valued as a category
            string or None if not detected.
        """
        text_lower = text.lower()
        time = self._extract_time(text_lower)
        effort = self._extract_effort(text_lower)
        return {"time": time, "effort": effort}

    def _extract_time(self, text: str) -> str | None:
        # 1. Check explicit minutes
        match = self._MINUTES_RE.search(text)
        if match:
            minutes = int(match.group(1))
            if minutes <= 30:
                return "short"
            elif minutes <= 60:
                return "medium"
            else:
                return "long"

        # 2. Check explicit hours
        match = self._HOURS_RE.search(text)
        if match:
            hours = int(match.group(1))
            total_minutes = hours * 60
            if total_minutes <= 30:
                return "short"
            elif total_minutes <= 60:
                return "medium"
            else:
                return "long"

        # 3. Check phrase patterns
        for pattern, value in self._TIME_PHRASES:
            if pattern.search(text):
                return value

        # 4. Check keywords
        for keyword, value in self._TIME_KEYWORDS.items():
            if keyword in text:
                return value

        return None

    def _extract_effort(self, text: str) -> str | None:
        for keyword, value in self._EFFORT_KEYWORDS.items():
            if keyword in text:
                return value
        return None
