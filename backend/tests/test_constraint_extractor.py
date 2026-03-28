"""Tests for the rule-based constraint extractor."""

from pantry.constraint_extractor import ConstraintExtractor


class TestConstraintExtractor:
    def setup_method(self):
        self.extractor = ConstraintExtractor()

    def test_time_short_from_keyword_and_minutes(self):
        result = self.extractor.extract("something quick, 20 minutes")
        assert result["time"] == "short"

    def test_time_short_from_explicit_30_minutes(self):
        result = self.extractor.extract("30 minutes max")
        assert result["time"] == "short"

    def test_effort_low_from_easy(self):
        result = self.extractor.extract("easy weeknight dinner")
        assert result["effort"] == "low"

    def test_no_constraints(self):
        result = self.extractor.extract("chicken and rice")
        assert result["time"] is None
        assert result["effort"] is None

    def test_both_time_and_effort(self):
        result = self.extractor.extract("quick and easy pasta")
        assert result["time"] == "short"
        assert result["effort"] == "low"

    def test_under_an_hour(self):
        result = self.extractor.extract("under an hour")
        assert result["time"] == "medium"

    def test_large_time_long(self):
        result = self.extractor.extract("2 hours")
        assert result["time"] == "long"
