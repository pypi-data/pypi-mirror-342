from collections.abc import Generator

import pytest
from standardbots import StandardBotsRobot
from standardbots.auto_generated import models


@pytest.fixture()
def unbrake_robot_fixt(client_live: StandardBotsRobot) -> Generator[None, None, None]:
    """Fixture: Ensure robot is unbraked"""
    with client_live.connection():
        res = client_live.movement.brakes.get_brakes_state()
        if res.data.state == models.BrakesStateEnum.Engaged:
            client_live.movement.brakes.set_brakes_state(
                models.BrakesState(state=models.BrakesStateEnum.Disengaged)
            )

    yield


@pytest.fixture()
def brake_robot_fixt(client_live: StandardBotsRobot) -> Generator[None, None, None]:
    """Fixture: Ensure robot is braked"""
    with client_live.connection():
        res = client_live.movement.brakes.get_brakes_state()
        if res.data.state == models.BrakesStateEnum.Disengaged:
            client_live.movement.brakes.set_brakes_state(
                models.BrakesState(state=models.BrakesStateEnum.Engaged)
            )

    yield
