from langgraph.graph import MessagesState


class AICompanionState(MessagesState):
    """State class for the AI Companion workflow.

    Extends MessagesState to track conversation history and maintains the last message received.

    Attributes:
        summary (AnyMessage): Summary of the most recent message in the conversation, can be any valid
            LangChain message type (HumanMessage, AIMessage, etc.)
        current_activity (str): The current activity of Jarvis based on the schedule.
        apply_activity (bool): Flag indicating whether to apply/update the current activity
        workflow (str): The current workflow the AI Companion is in. Can be "conversation", "image", or "audio".
        audio_buffer (bytes): The audio buffer to be used for speech-to-text conversion.
    """

    summary: str
    current_activity: str
    apply_activity: bool
    workflow: str
    audio_buffer: bytes


    