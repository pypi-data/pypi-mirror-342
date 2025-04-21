from pydicom import Dataset
from pynetdicom import (
    AE,
    evt,
    debug_logger,
    build_role,
    AllStoragePresentationContexts,
)
from pynetdicom.sop_class import (
    Verification,
    DigitalXRayImageStorageForPresentation,

    PatientRootQueryRetrieveInformationModelGet,
    StudyRootQueryRetrieveInformationModelGet,
    PatientStudyOnlyQueryRetrieveInformationModelGet,

    PatientRootQueryRetrieveInformationModelMove,
    StudyRootQueryRetrieveInformationModelMove,
    PatientStudyOnlyQueryRetrieveInformationModelMove,
)

# debug_logger()

class BaseDicomHandler:

    def __init__(self, ae_title='ZY-AE', host='127.0.0.1', port=11112, **kwargs):
        self.ae_title = ae_title
        self.host = host
        self.port = port
        self.ae = AE(ae_title=ae_title)

        for k, v in kwargs.items():
            setattr(self, k, v)

    def test(self):
        print("test dicom server", self.ae)

    def _log(self, event):
        requestor = event.assoc.requestor
        timestamp = event.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        msg = "\n\n{} from ({}, {}) at {}\n\n".format(
            event._event.description, requestor.address, requestor.port, timestamp
        )
        print(msg)

    def handle_echo(self, event):
        """Handle a C-ECHO service request.

        Parameters
        ----------
        event : evt.Event
            The C-ECHO service request event, this parameter is always
            present.
        logger : logging.Logger
            The logger to use, this parameter is only present because we
            bound ``evt.EVT_C_ECHO`` using a 3-tuple.

        Returns
        -------
        int or pydicom.dataset.Dataset
            The status returned to the peer AE in the C-ECHO response.
            Must be a valid C-ECHO status value as either an ``int`` or a
            ``Dataset`` object containing an (0000,0900) *Status* element.
        """
        # Every *Event* includes `assoc` and `timestamp` attributes
        #   which are the *Association* instance the event occurred in
        #   and the *datetime.datetime* the event occurred at
        self._log(event)

        # Return a *Success* status
        return 0x0000

    def _get_remote_ae_info(self, event):
        # {'ae_title': 'WDM', 'address': '192.168.140.56', 'port': 50535, 'mode': 'requestor', 'pdv_size': 16384}
        remote_info = event.assoc.remote
        ae_title = remote_info.get("ae_title")
        address = remote_info.get("address")
        # port = remote_info.get("port")
        return f'{ae_title}@{address}'

    def after_store(self, event, ds):
        # from app.dr_detect.utils import DicomParser
        # from app.dr_detect.const import DataSource
        # from app.dr_detect.service import async_AI_DR_diagnose_entrance


        # # Save the dataset using the SOP Instance UID as the filename
        # now = datetime.datetime.now()
        # save_dir = os.path.join(DR_CLOUD_PATH, f'{now.year}/{now.month}/{now.day}')
        # if not os.path.exists(save_dir):
        #     os.makedirs(save_dir)

        # save_file = os.path.join(save_dir, f'{ds.SOPInstanceUID}.dcm')
        # ds.save_as(save_file, write_like_original=False)

        # if not os.path.exists(save_file):
        #     print(f"Could not found save sop {save_file}")
        #     return

        # sop_file = save_file

        # dcm = DicomParser(sop_file)
        # if hasattr(dcm.ds, 'BodyPartExamined'):
        #     bodypart_examined = dcm.charset_decode(dcm.ds.BodyPartExamined)
        # else:  # 没有的当胸片处理
        #     bodypart_examined = 'CHEST'
        # print("recevied dcm BodyPartExamined is %s", bodypart_examined)
        # print("recevied dcm is %s", sop_file)

        # # 过滤掉非胸片
        # if int(ENVIRON.get("ZY_DATA_DST", 0)) == 0:
        #     ai_diagnose_flag = True
        # elif '胸' in bodypart_examined or bodypart_examined.upper() in ['CHEST', 'THORAX']:
        #     ai_diagnose_flag = True
        # else:
        #     ai_diagnose_flag = False

        # if ai_diagnose_flag:
        #     # 优先白名单ae:ip的模式去强制走node的解决方案
        #     ae_node_ip_scope = ENVIRON.get("AE_NODE_IP_SCOPE", '')
        #     if ae_node_ip_scope:
        #         request_ae_addr = self._get_remote_ae_info(event)
        #         if ae_node_ip_scope.find(request_ae_addr) > -1:
        #             print(f"in special case {request_ae_addr}")
        #             self.handle_type = DataSource.node.value

        #     async_AI_DR_diagnose_entrance(self.handle_type, sop_file)
        #     print(f'dr sop <{sop_file}> send work task')
        raise NotImplementedError("after_store is not implemented")

    def handle_store(self, event):
        """Handle a C-STORE request event."""
        # Decode the C-STORE request's *Data Set* parameter to a pydicom Dataset
        self._log(event)

        ds = event.dataset

        # Add the File Meta Information
        ds.file_meta = event.file_meta

        self.after_store(event, ds)

        return 0x0000


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


class DicomClient(BaseDicomHandler):
    store_contexts = [
        DigitalXRayImageStorageForPresentation
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for cx in self.store_contexts:
            self.ae.add_requested_context(cx)

    def QR_Get(self, q_level, **q_kwargs):
        if q_level == 'STUDY':
            query = StudyRootQueryRetrieveInformationModelGet
        elif q_level == 'SERIES':
            query = PatientRootQueryRetrieveInformationModelGet
        else:
            query = PatientStudyOnlyQueryRetrieveInformationModelGet

        self.ae.add_requested_context(query)

        ds = Dataset()
        ds.QueryRetrieveLevel = q_level
        for k, v in q_kwargs.items():
            if hasattr(ds, k):
                setattr(ds, k, v)

        ext_neg = [build_role(cx, scp_role=True) for cx in self.store_contexts]
        handlers = [(evt.EVT_C_STORE, self.handle_store)]
        assoc = self.ae.associate(
            self.host, self.port, ae_title=self.remote_ae_title,
            ext_neg=ext_neg, evt_handlers=handlers
        )
        if assoc.is_established:
            # Use the C-GET service to send the identifier
            responses = assoc.send_c_get(ds, query)
            for (status, _) in responses:
                if status:
                    print('C-GET query status: 0x{0:04x}'.format(status.Status))
                else:
                    raise Exception('DICOM C-GET request timed out')

            # Release the association
            assoc.release()
        else:
            raise Exception('DICOM Server is unavailable')

    def QR_Move(self, q_level, **q_kwargs):
        if q_level == 'STUDY':
            query = StudyRootQueryRetrieveInformationModelMove
        elif q_level == 'SERIES':
            query = PatientRootQueryRetrieveInformationModelMove
        else:
            query = PatientStudyOnlyQueryRetrieveInformationModelMove

        self.ae.add_requested_context(query)

        ds = Dataset()
        ds.QueryRetrieveLevel = q_level
        for k, v in q_kwargs.items():
            setattr(ds, k, v)

        assoc = self.ae.associate(
            self.host, self.port, ae_title=self.remote_ae_title,
        )
        if assoc.is_established:
            responses = assoc.send_c_move(ds, self.ae_title, query)
            for (status, _) in responses:
                if status:
                    print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
                else:
                    print(f'C-MOVE query timeout: {q_kwargs}')
                    raise Exception('DICOM C-MOVE request timed out')

            # Release the association
            assoc.release()
        else:
            raise Exception('DICOM Server [%s@%s:%s] is unavailable.'.format(
                self.remote_ae_title, self.host, self.port))


if __name__ == '__main__':
    DicomClient(
        host='88.20.10.141', port=4002, remote_ae_title='jhbfz_storeQR'
    ).QR_Move(
        'STUDY',
        StudyInstanceUID='1.2.840.113619.2.261.4.2147483647.20241127.385431'
    )
