from abc import ABC, abstractmethod


class DetachedRunner(ABC):
    @abstractmethod
    def run(self, fname: str, *args, **kwargs):
        """
        Run the given function detached from the current process.

        :param fname: The full path to the function to run.
        :param args: The arguments to pass to the function.
        :param kwargs: The keyword arguments to pass to the function.
        :return: The result of the function.
        """
        raise NotImplementedError
