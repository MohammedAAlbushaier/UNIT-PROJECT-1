from datetime import datetime
from typing import Dict, Any


class Course:
    """Represents a course with its details."""

    def __init__(self, subject: str, crn: int, start_date: datetime, end_date: datetime, start_time: str,
                 end_time: str, cost: float) -> None:
        self.__subject = subject
        self.__crn = crn
        self.__start_date = start_date
        self.__end_date = end_date
        self.__start_time = start_time
        self.__end_time = end_time
        self.__cost = cost

    def to_dict(self) -> Dict[str, Any]:
        """Convert the course object to a dictionary."""
        return {
            "Subject": self.__subject,
            "CRN": self.__crn,
            "Start Date": self.__start_date.isoformat(),
            "End Date": self.__end_date.isoformat(),
            "Start Time": self.__start_time,
            "End Time": self.__end_time,
            "Cost": self.__cost
        }

    @property
    def subject(self) -> str:
        return self.__subject

    @property
    def crn(self) -> int:
        return self.__crn

    @property
    def start_date(self) -> datetime:
        return self.__start_date

    @property
    def end_date(self) -> datetime:
        return self.__end_date

    @property
    def start_time(self) -> str:
        return self.__start_time

    @property
    def end_time(self) -> str:
        return self.__end_time

    @property
    def cost(self) -> float:
        return self.__cost

