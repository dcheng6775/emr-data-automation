"""
Run with:
    pip install pytest flask flask-cors
    pytest test_suite.py -v
"""

import io
import json
import pytest
from unittest.mock import MagicMock

import sys
sys.modules.setdefault("pytesseract", MagicMock())
sys.modules.setdefault("pdf2image", MagicMock())
sys.modules.setdefault("PIL", MagicMock())
sys.modules.setdefault("PIL.Image", MagicMock())

from utils import extract_data
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


SAMPLE_REPORT = """
Name: Smith, John
DOB: 1950-03-14
Age: 74
Sex: M
Wt: 85.0
Ht: 175.0
The patient has paroxysmal atrial fibrillation and underwent pulmonary vein isolation ablation.
LVEF: 55-60%
"""

SAMPLE_REPORT_FEMALE = """
Name: Doe, Jane
Age: 76
Sex: F
Wt: 65.0
Ht: 163.0
The patient has persistent AF.
LVEF 40%
"""


class TestExtractData:

    def test_name_extracted(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["Name"] == "Smith, John"

    def test_age_extracted(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["Age"] == "74"

    def test_sex_extracted(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["Sex"] == "M"

    def test_weight_extracted(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["Wt"] == "85.0"

    def test_height_extracted(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["Ht"] == "175.0"

    def test_afib_type_detected(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["AFib_Type"].lower() == "paroxysmal"

    def test_ablation_type_detected(self):
        result = extract_data(SAMPLE_REPORT)
        assert "pulmonary" in result["Ablation_Type"].lower()

    def test_lvef_extracted(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["LVEF (Lower Range)"] == "55"

    def test_not_found_for_missing_field(self):
        result = extract_data("No useful content here.")
        assert result["Name"] == "NOT FOUND"
        assert result["Age"] == "NOT FOUND"


class TestDerivedFields:

    def test_age_65_74_band_true(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["Age_65_74"] == "Y"
        assert result["Age_75_plus"] == "N"

    def test_age_75_plus_band(self):
        result = extract_data(SAMPLE_REPORT_FEMALE)
        assert result["Age_65_74"] == "N"
        assert result["Age_75_plus"] == "Y"

    def test_female_flag_male(self):
        result = extract_data(SAMPLE_REPORT)
        assert result["Female"] == "N"

    def test_female_flag_female(self):
        result = extract_data(SAMPLE_REPORT_FEMALE)
        assert result["Female"] == "Y"

    def test_bmi_calculated_metric(self):
        result = extract_data(SAMPLE_REPORT)
        assert isinstance(result["BMI"], float)
        assert 25.0 < result["BMI"] < 30.0

    def test_bmi_not_found_when_height_missing(self):
        report = "Age: 50\nSex: M\nWt: 80.0\n"
        result = extract_data(report)
        assert result["BMI"] == "NOT FOUND"

    def test_age_bands_not_found(self):
        result = extract_data("No age here.")
        assert result["Age_65_74"] == "N"
        assert result["Age_75_plus"] == "N"


class TestAnalyzeEndpoint:

    def _make_file(self, content: str, filename: str = "report.txt"):
        return (io.BytesIO(content.encode()), filename)

    def test_analyze_returns_200_with_valid_file(self, client):
        data = {"file1": self._make_file(SAMPLE_REPORT)}
        resp = client.post("/analyze", data=data, content_type="multipart/form-data")
        assert resp.status_code == 200

    def test_analyze_returns_json(self, client):
        data = {"file1": self._make_file(SAMPLE_REPORT)}
        resp = client.post("/analyze", data=data, content_type="multipart/form-data")
        body = json.loads(resp.data)
        assert "Name" in body
        assert "Age" in body

    def test_analyze_returns_400_with_no_files(self, client):
        resp = client.post("/analyze", data={}, content_type="multipart/form-data")
        assert resp.status_code == 400

    def test_analyze_accepts_up_to_three_files(self, client):
        data = {
            "file1": self._make_file(SAMPLE_REPORT, "r1.txt"),
            "file2": self._make_file(SAMPLE_REPORT_FEMALE, "r2.txt"),
        }
        resp = client.post("/analyze", data=data, content_type="multipart/form-data")
        assert resp.status_code == 200


class TestExportEndpoint:

    def _make_file(self, content: str, filename: str = "report.txt"):
        return (io.BytesIO(content.encode()), filename)

    def test_export_returns_csv_mimetype(self, client):
        data = {"file1": self._make_file(SAMPLE_REPORT)}
        resp = client.post("/export", data=data, content_type="multipart/form-data")
        assert resp.status_code == 200
        assert "text/csv" in resp.content_type

    def test_export_has_content_disposition(self, client):
        data = {"file1": self._make_file(SAMPLE_REPORT)}
        resp = client.post("/export", data=data, content_type="multipart/form-data")
        assert "attachment" in resp.headers.get("Content-Disposition", "")

    def test_export_csv_has_header_and_data_row(self, client):
        data = {"file1": self._make_file(SAMPLE_REPORT)}
        resp = client.post("/export", data=data, content_type="multipart/form-data")
        lines = resp.data.decode().strip().splitlines()
        assert len(lines) == 2

    def test_export_returns_400_with_no_files(self, client):
        resp = client.post("/export", data={}, content_type="multipart/form-data")
        assert resp.status_code == 400