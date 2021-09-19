from lib.controllers import Controller
from lib.arguments import parse_args
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    controller = Controller(
        arguments=parse_args()
    )
    try:
        controller.join_workers()
    except KeyboardInterrupt:
        pass