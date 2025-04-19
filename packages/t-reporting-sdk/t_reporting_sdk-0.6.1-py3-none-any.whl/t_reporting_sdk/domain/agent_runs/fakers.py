from random import randint
from typing import Optional

from faker import Faker

from t_reporting_sdk.domain.agent_runs.models import AgentRun


class AgentRunFaker:
    @staticmethod
    def provide(
        run_id: Optional[int] = None,
        run_date: Optional[str] = None,
    ) -> AgentRun:
        faker = Faker()

        fake_run_id = randint(1, 100)
        fake_run_date = faker.date_time_this_month()

        return AgentRun(
            run_id=fake_run_id if run_id is None else run_id,
            run_date=fake_run_date if run_date is None else run_date,
        )