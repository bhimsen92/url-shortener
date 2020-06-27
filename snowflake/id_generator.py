from datetime import datetime
import time
from sync import synchronized


_64bit = 0xFFFFFFFFFFFFFFFF


class IdGenerator:
    UNUSED_BITS = 1
    EPOCH_BITS = 41
    SERVICE_ID_BITS = 10
    SEQUENCE_BITS = 12
    CUSTOM_EPOCH = 1593201852000  # June 26 2020 10PM.

    max_service_id = int(2 ** SERVICE_ID_BITS - 1)
    max_sequence = int(2 ** SEQUENCE_BITS - 1)

    def __init__(self, service_id: int):
        if service_id < 0 or service_id > self.max_service_id:
            raise Exception(
                "Service ID must be between %d and %d.", (1, self.max_service_id)
            )
        self.service_id: int = service_id
        self.last_timestamp = -1
        self.sequence = 0

    @synchronized
    def next_id(self):
        """
        Returns next 64 bit unique id.
        """
        current_timestamp = self._timestamp()
        if current_timestamp < self.last_timestamp:
            raise Exception(
                "Clock is running backwards. Can't generate ids until its fixed."
            )

        if current_timestamp == self.last_timestamp:
            # within a millisecond, you received a lot of requests, hence the equality check.
            self.sequence = (self.sequence + 1) % self.max_sequence
            if self.sequence == 0:
                # sequence exhausted, wait for next millisecond.
                current_timestamp = self._wait_next_milliseconds(current_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = current_timestamp
        unique_id = (
            current_timestamp << (self.SEQUENCE_BITS + self.SERVICE_ID_BITS)
            | self.service_id << self.SEQUENCE_BITS
            | self.sequence
        ) & _64bit
        return unique_id

    def _timestamp(self):
        return self._get_current_time_in_milliseconds() - self.CUSTOM_EPOCH

    @staticmethod
    def _get_current_time_in_milliseconds():
        epoch = datetime.utcfromtimestamp(0)
        return int((datetime.utcnow() - epoch).total_seconds() * 1000)

    def _wait_next_milliseconds(self, current_timestamp):
        while self.last_timestamp == current_timestamp:
            time.sleep(1 / 1000.0)
            current_timestamp = self._timestamp()
        return current_timestamp
