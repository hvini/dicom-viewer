""" patient routers tests module """


def test_get_patients_should_return_success_status_with_an_empty_list_when_table_is_empty(client):
    """ get patients test """

    response = client.get("/patients")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"] == []


def test_get_patient_studies_should_return_error_status_when_invalid_id_is_provided(client):
    """ get patient studies test """

    response = client.get("/patients/1/studies")

    assert response.status_code == 404
    data = response.json()
    assert data["status"] == "error"
