from conftest import Manager, Participant
from httpx import AsyncClient


async def test_register_manager(client: AsyncClient, manager: Manager):
    response = await client.post(
        "/api/v1/register/managers",
        json=manager,
    )
    assert response.status_code == 201


async def test_login(client: AsyncClient, manager: Manager):
    response = await client.post(
        "/api/v1/login",
        json={
            "email": manager["email"],
            "password": manager["password"],
        },
    )

    assert response.status_code == 200


async def test_invalid_login(client: AsyncClient):
    response = await client.post(
        "/api/v1/login",
        json={
            "email": "aaaa",
            "password": "bbbbbbbbbb",
        },
    )

    assert response.status_code == 401


async def test_register_participant(client: AsyncClient, participant: Participant):
    response = await client.post(
        "/api/v1/register/participants",
        json=participant,
    )
    assert response.status_code == 201


async def test_register_same_participant(client: AsyncClient, participant: Participant):
    response = await client.post(
        "/api/v1/register/participants",
        json=participant,
    )
    assert response.status_code == 409


async def test_categories(client: AsyncClient):
    response = await client.get(
        "/api/v1/categories",
    )
    assert response.status_code == 200


async def test_states(client: AsyncClient):
    response = await client.get(
        "/api/v1/states",
    )
    assert response.status_code == 200


async def test_unauthenticated(client: AsyncClient):
    response = await client.get(
        "/api/v1/participants",
    )
    assert response.status_code == 401

    response = await client.get("/api/v1/participants", headers={"Authorization": "<3"})
    assert response.status_code == 401

    response = await client.get(
        "/api/v1/participants",
        headers={"Authorization": "Really long string. Definitely longer than an uuid"},
    )
    assert response.status_code == 401


async def test_participant_id(
        client: AsyncClient,
        manager: Manager,
        participant: Participant,
        manager_token: str,
):
    response = await client.get(
        "/api/v1/participants/me",
        headers={"Authorization": manager_token},
    )
    assert response.status_code == 200
    me = response.json()["result"]
    assert me["first_name"] == manager["first_name"]
    assert me["email"] == manager["email"]

    response = await client.get(
        "/api/v1/participants/2",
        headers={"Authorization": manager_token},
    )
    assert response.status_code == 200
    participant_2 = response.json()["result"]
    assert participant["first_name"] == participant_2["first_name"]
    assert participant["email"] == participant_2["email"]


async def test_participants(
    client: AsyncClient,
    manager_token: str,
):
    response = await client.get(
        "/api/v1/participants",
        headers={"Authorization": manager_token},
    )
    assert response.status_code == 200
    participants = response.json()["result"]
    assert len(participants) == 2, "Unexpected number of participants. Did it count manager itself?"


async def test_participants_no_access(
    client: AsyncClient,
    manager_token: str,
):
    response = await client.get(
        "/api/v1/participants/3",
        headers={"Authorization": manager_token},
    )
    assert response.status_code == 404


async def test_instruction(client: AsyncClient, participant: Participant, participant_token: str,):
    response = await client.get(
        f"/api/v1/instructions",
    )
    assert response.status_code == 401

    response = await client.get(
        f"/api/v1/instructions",
        headers={"Authorization": participant_token},
    )
    assert response.status_code == 200
    instruction = response.json()['result']
    assert participant['first_name'] in instruction


async def test_feedback_same_state(client: AsyncClient, participant_token: str):
    feedback_date = "2022-05-01"
    response = await client.get(
        f"/api/v1/feedbacks/{feedback_date}",
        headers={"Authorization": participant_token},
    )
    assert response.status_code == 200
    feedback = response.json()

    assert feedback["morning"] is None
    assert feedback["evening"] is None

    response = await client.post(
        f"/api/v1/feedbacks/{feedback_date}/morning",
        headers={"Authorization": participant_token},
        json={"state_id": 1},
    )
    assert response.status_code == 204

    response = await client.post(
        f"/api/v1/feedbacks/{feedback_date}/evening",
        headers={"Authorization": participant_token},
        json={"state_id": 1},
    )
    assert response.status_code == 204

    response = await client.get(
        f"/api/v1/feedbacks/{feedback_date}",
        headers={"Authorization": participant_token},
    )
    assert response.status_code == 200
    states = response.json()
    assert states["morning"] == {"id": 1, "name": "Плохо", "value": 100}
    assert states["evening"] == {"id": 1, "name": "Плохо", "value": 100}


async def test_feedback_worse_state(client: AsyncClient, participant_token: str):
    feedback_date = "2022-05-02"
    response = await client.get(
        f"/api/v1/feedbacks/{feedback_date}",
        headers={"Authorization": participant_token},
    )
    assert response.status_code == 200
    feedback = response.json()

    assert feedback["morning"] is None
    assert feedback["evening"] is None

    response = await client.post(
        f"/api/v1/feedbacks/{feedback_date}/morning",
        headers={"Authorization": participant_token},
        json={"state_id": 2},
    )
    assert response.status_code == 204

    response = await client.post(
        f"/api/v1/feedbacks/{feedback_date}/evening",
        headers={"Authorization": participant_token},
        json={"state_id": 1, "factor_id": 3},
    )
    assert response.status_code == 204

    response = await client.get(
        f"/api/v1/feedbacks/{feedback_date}",
        headers={"Authorization": participant_token},
    )
    assert response.status_code == 200
    states = response.json()
    assert states["morning"] == {"id": 2, "name": "Средне", "value": 200}
    assert states["evening"] == {"id": 1, "name": "Плохо", "value": 100}


async def test_recommendation(client: AsyncClient, participant: Participant, participant_token: str,):
    response = await client.get(
        f"/api/v1/recommendations",
    )
    assert response.status_code == 401

    response = await client.get(
        f"/api/v1/recommendations",
        headers={"Authorization": participant_token},
    )
    assert response.status_code == 200
    recommendations = response.json()['result']
    assert participant['first_name'] in recommendations
