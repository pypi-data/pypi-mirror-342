"""The default introspection agent.

This agent looks at the state of a plan run between steps
and makes decisions about whether execution should continue.
"""

from datetime import UTC, datetime

from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage

from portia.config import Config
from portia.introspection_agents.introspection_agent import (
    BaseIntrospectionAgent,
    PreStepIntrospection,
)
from portia.model import Message
from portia.plan import Plan
from portia.plan_run import PlanRun


class DefaultIntrospectionAgent(BaseIntrospectionAgent):
    """Default Introspection Agent.

    Implements the BaseIntrospectionAgent interface using an LLM to make decisions about what to do.

    Attributes:
        config (Config): Configuration settings for the DefaultIntrospectionAgent.

    """

    def __init__(self, config: Config) -> None:
        """Initialize the DefaultIntrospectionAgent with configuration.

        Args:
            config (Config): The configuration to initialize the DefaultIntrospectionAgent.

        """
        self.config = config

        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=(
                        "You are a highly skilled reviewer who reviews in flight plan execution."
                        "Your job is to examine the state of a plan execution (PlanRun) and "
                        "decide what action should be taken next."
                        "You should use the current_step_index field to identify the current step "
                        "in the plan, and the PlanRun state to know what has happened so far."
                        "The actions that can be taken are:"
                        " - COMPLETE -> complete execution and return the result so far."
                        " - SKIP -> skip the current step execution."
                        " - FAIL -> stop and fail execution entirely."
                        " - CONTINUE -> Continue execution for the current step."
                        "You should choose an outcome based on the following logic in order:\n"
                        " - If the overarching goal of the plan "
                        "has already been met return COMPLETE.\n"
                        " - If the current step has a condition that is false you return SKIP.\n"
                        " - If you cannot evaluate the condition"
                        " because it's impossible to evaluate return FAIL.\n"
                        " - If you cannot evaluate the condition because some data had been skipped"
                        "  in previous steps then return SKIP.\n"
                        " - Otherwise return CONTINUE.\n"
                        "Return the outcome and reason in the given format.\n"
                    ),
                ),
                HumanMessagePromptTemplate.from_template(
                    "Today's date is {current_date} and today is {current_day_of_week}.\n"
                    "Review the following plan + current PlanRun.\n"
                    "Current Plan: {plan}\n"
                    "Current PlanRun: {plan_run}\n",
                ),
            ],
        )

    def pre_step_introspection(
        self,
        plan: Plan,
        plan_run: PlanRun,
    ) -> PreStepIntrospection:
        """Ask the LLM whether to continue, skip or fail the plan_run."""
        return self.config.get_introspection_model().get_structured_response(
            schema=PreStepIntrospection,
            messages=[
                Message.from_langchain(m)
                for m in self.prompt.format_messages(
                    current_date=datetime.now(UTC).strftime("%Y-%m-%d"),
                    current_day_of_week=datetime.now(UTC).strftime("%A"),
                    plan_run=plan_run.model_dump_json(),
                    plan=plan.model_dump_json(),
                )
            ],
        )
