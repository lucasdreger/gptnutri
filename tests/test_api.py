from fastapi.testclient import TestClient

from app.main import analyze_meals, app


client = TestClient(app)


def test_analyze_meals_detects_foods_and_totals() -> None:
    result = analyze_meals(["chicken rice broccoli", "banana yogurt"])
    assert result.calories == 730
    assert result.protein_g == 64.3
    assert "chicken" in result.detected_foods
    assert "broccoli" in result.detected_foods


def test_analyze_endpoint() -> None:
    response = client.post("/api/analyze", json={"meals": ["salmon avocado", "oats"]})
    assert response.status_code == 200
    body = response.json()
    assert body["calories"] == 518
    assert sorted(body["detected_foods"]) == ["avocado", "oats", "salmon"]
