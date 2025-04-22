from app.rag.models import State
from app.utils.logging import logger
from langchain_core.runnables import Runnable, RunnableConfig


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: State, config: RunnableConfig):
        logger.info(f"Processing message: {state['messages'][-1].content}")
        while True:
            configuration = config.get("configurable", {})
            user_info = configuration.get("user_info", None)
            state = {**state, "user_info": user_info}
            result = self.runnable.invoke(state)

            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break

        if result.tool_calls:
            logger.info(f"Tool calls: {result.tool_calls}")

        if result.content:
            logger.info(f"Answer: {result.content}")

        return {"messages": result}
