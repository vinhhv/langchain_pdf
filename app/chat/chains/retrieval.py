from app.chat.chains.streamable import StreamableChain
from app.chat.chains.traceable import TraceableChain
from langchain.chains import ConversationalRetrievalChain


class StreamingConversationalRetrievalChain(
    TraceableChain, StreamableChain, ConversationalRetrievalChain
):
    pass
