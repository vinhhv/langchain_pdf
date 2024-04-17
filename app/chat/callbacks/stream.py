from langchain.callbacks.base import BaseCallbackHandler


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
        self.streaming_run_ids = set()

    def on_chat_model_start(self, serialized, messages, run_id, **kwargs):
        if serialized["kwargs"]["streaming"]:
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, run_id, **kwargs):
        # Multiple streaming models have access to this.
        # Prevent non-streaming models to put `None` into the queue.
        if run_id in self.streaming_run_ids:
            self.queue.put(None)
            self.streaming_run_ids.remove(run_id)

    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)
