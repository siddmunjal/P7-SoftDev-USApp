def test_points_board_accessible_without_login(client):
    """Any user, even one who isn't logged in, can view the points board."""
    resp = client.get("/clubs")
    assert resp.status_code == 200


def test_points_board_lists_all_clubs_and_points(client):
    resp = client.get("/clubs")
    body = resp.data.decode()
    assert "Simply Lift" in body
    assert "13" in body
    assert "Iron Temple" in body
    assert "4" in body
    assert "She Lifts" in body
    assert "12" in body
