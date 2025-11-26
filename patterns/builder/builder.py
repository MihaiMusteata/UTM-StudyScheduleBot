from abc import abstractmethod, ABC

from patterns.builder.product import Notification


class NotificationBuilder(ABC):

    @property
    @abstractmethod
    def notification(self) -> Notification:
        pass

    @abstractmethod
    def set_type(self, value: str) -> None:
        pass

    @abstractmethod
    def set_target(self, value: str) -> None:
        pass

    @abstractmethod
    def set_subject_name(self, value: str) -> None:
        pass

    @abstractmethod
    def set_date(self, value: str) -> None:
        pass

    @abstractmethod
    def set_time(self, value: str) -> None:
        pass

    @abstractmethod
    def set_room(self, value: str) -> None:
        pass

    @abstractmethod
    def set_target_label(self, value: str) -> None:
        pass
