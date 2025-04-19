import shutil
from typing import Callable, List, Optional, Any
from functools import wraps
from halo import Halo


class bcolors:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"


class AppChecker:
    def __init__(self, checks: Optional[List[Callable[[], Any]]] = None) -> None:
        self.checks: List[Callable[[], Any]] = []
        self.spinner: Halo = Halo(text="Loading", spinner="dots")
        self.success: int = 0
        self.failure: int = 0

    def register_check(self, func: Callable[[], Any]) -> Callable[[], Any]:
        """Метод для регистрации функции проверки."""
        self.checks.append(func)
        return func

    async def run_checks(self) -> None:
        self.display_message(self.on_center("check starts"))
        print(f"collected {len(self.checks)} items")
        print()
        for check in self.checks:
            result: Optional[bool] = False
            name: str = check.__name__

            print(f"Starting {name}...")
            result = await self.load_with_halo(check)

            if result is True:
                self.spinner.succeed(f"[SUCCESS] {name}")
                self.success += 1
            else:
                self.spinner.fail(f"[FAILURE] {name}")
                self.failure += 1

        self.display_results()

    async def load_with_halo(self, check_func: Callable[[], Any]) -> bool:
        with Halo(text="Loading", spinner="dots"):
            try:
                result: bool = await check_func()
            except Exception as e:
                print()
                print(e)
                return False
        return result

    def display_results(self) -> None:
        message: str = f"{self.success} [success]"
        message = self.set_color(self.on_center(message), bcolors.OKGREEN)
        if self.failure:
            message = f"{self.failure} [failure]"
            message = self.set_color(self.on_center(message), bcolors.FAIL)
            self.display_message(message, bcolors.FAIL)
        else:
            self.display_message(message, bcolors.OKGREEN)

        if not self.failure:
            self.display_startup_message("All checks success.")
        elif self.failure == len(self.checks):
            self.display_startup_message("All checks failed.")
        else:
            self.display_startup_message("Some checks failed.")

    def display_startup_message(self, message: str) -> None:
        print(message)

    def set_color(self, message: str, color: Optional[str] = None) -> str:
        if color:
            return f"{color}{message}{color}"
        return f"{message}"

    def on_center(self, message: str) -> str:
        terminal_width: int = shutil.get_terminal_size().columns
        return message.center(terminal_width)

    def display_message(self, message: str, color: Optional[str] = None) -> None:
        terminal_width: int = shutil.get_terminal_size().columns
        dashes: str = "-" * terminal_width

        print(self.set_color(dashes, color))
        print(f"{message}")
        print(self.set_color(dashes, color))

    def check_health(self, func: Callable[[], Any]) -> Callable[[], Any]:

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> bool:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                print()
                print(e)
                return False

        self.register_check(wrapper)
        return wrapper
