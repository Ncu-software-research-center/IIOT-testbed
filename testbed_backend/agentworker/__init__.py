class EmulationStatus:
    INIT = "0"
    START = "1"
    END = "2"
    EXCEPTION = "3"
    ABORT = "4"

class WorkerStatus:
    WAIT = "0"
    PREPARE = "1"
    READY = "2"
    DONE = "3"
    EXCEPTION = "4"
