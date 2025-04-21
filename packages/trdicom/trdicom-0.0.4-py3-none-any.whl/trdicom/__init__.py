from pynetdicom import (
    evt,
    AllStoragePresentationContexts,
)
from pynetdicom.sop_class import (
    Verification,
)

from trdicom.netdicom import BaseDicomHandler


class DicomServer(BaseDicomHandler):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_server(self):
        self.ae.add_supported_context(Verification)
        self.ae.supported_contexts = AllStoragePresentationContexts
        handlers = [
            (evt.EVT_C_ECHO, self.handle_echo),
            (evt.EVT_C_STORE, self.handle_store),
        ]
        # Start the SCP in non-blocking mode
        self.ae.start_server(
            (self.host, self.port),
            block=self.block,
            evt_handlers=handlers
        )