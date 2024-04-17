from dotenv import load_dotenv
from queue import Queue
from threading import Thread
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler

load_dotenv()


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue

    def on_llm_new_token(self, token, **kwargs):
        self.queue.put(token)

    def on_llm_end(self, response, **kwargs):
        self.queue.put(None)

    def on_llm_error(self, error, **kwargs):
        self.queue.put(None)


# kwargs are overridden by call method (i.e. "chat(...) or chat.invoke(...), or chat.stream(...) with streaming")
chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([("human", "{content}")])


class StreamingChain(LLMChain):
    def stream(self, input):
        queue = Queue()
        handler = StreamingHandler(queue)

        def task():
            self(input, callbacks=[handler])

        Thread(target=task).start()

        while True:
            token = queue.get()
            if token is None:
                break
            yield token


chain = StreamingChain(llm=chat, prompt=prompt)

for output in chain.stream(input={"content": "tell me a joke"}):
    print(output)


# chain = LLMChain(llm=chat, prompt=prompt)

# messages = prompt.format_messages(content="tell me a joke")

# # Streaming is different for the chain (it streams separate inputs, but not single outputs)
# for output in chain.stream(input={"content": "tell me a joke"}):
#     print(output)


# for message in chat.stream(messages):
#     print(message.content)
