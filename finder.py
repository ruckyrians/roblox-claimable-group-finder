from lib.controllers import Controller
from lib.arguments import parse_args
import multiprocessing

if __name__ == "__main__":
    multiprocessing.freeze_support()
    arguments = parse_args()
    controller = Controller(
        arguments=arguments
    )
    print("All workers are running!")
    try:
        controller.join_workers()
    except KeyboardInterrupt:
        pass