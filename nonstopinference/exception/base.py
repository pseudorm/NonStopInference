import json
import os
import time
import pickle


class ExceptionRecord:
    def __init__(
        self, data_id: str, block_id: str, status: str, error_msg: str
    ):
        self.data_id = data_id
        self.block_id = block_id
        self.status = status
        self.error_message = error_msg


class ExceptionChain:
    def __init__(self):
        None


class ExceptionLogger:
    def __init__(self, name, log_dir=None, log_callback=None):
        self.name = name
        self.log_dir = log_dir
        self.log_callback = log_callback
        self._log_json, self._log_json_path = self._init_log_json()
        # self._log_pickle, self._log_pickle_path = self._init_log_pickle()

    def _init_log_json(self):
        json_name = self.name + "_" + int(time.now()) + ".json"
        json_path = os.path.join(self.log_dir, json_name)

        return open(json_path, "a"), json_path

    # def _init_log_pickle(self):
    #     pickle_name = self.name + "_" + int(time.now()) + ".pkl"
    #     pickle_path = os.path.join(self.log_dir, pickle_name)

    #     return open(pickle_path, "a+"), pickle_path

    def _log_to_json(self, exception_record):
        error_body = {
            "data_id": exception_record.data_id,
            "block_id": exception_record.block_id,
            "status": exception_record.status,
            "error_message": exception_record.error_msg,
        }

        self._log_json.write(json.dumps(error_body), +"\n")

    # def _log_to_pickle(self, exception_record):
    #     data_body = {
    #         "data_id": exception_record.data_id,
    #         "data": exception_record.data,
    #     }
    #     pickle.dump(data_body, self._log_pickle)

    def log(
        self, data_id: str, block_id: str, status: str, error_msg: str
    ) -> None:
        exception_record = ExceptionRecord(
            data_id, block_id, status, error_msg
        )

        if self.log_callback:
            self.log_callback(exception_record)

        self._log_to_json(exception_record)
        # self._log_to_pickle(exception_record)


class ExceptionReader:
    def __init__(self, name, log_dir=None) -> None:
        self.name = name
        self.log_dir = log_dir

