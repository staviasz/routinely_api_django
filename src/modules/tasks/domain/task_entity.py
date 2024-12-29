from datetime import datetime
from typing import Optional, cast, get_args
from main.adapters.uuidAdapter import UuidAdapter
from main.domain.entity import Entity
from main.errors.domain.invalid_id_error import InvalidIdError
from modules.tasks.domain import (
    TaskModel,
    TaskType,
    TaskCategories,
    Weekday,
    InvalidTaskTypeError,
    InvalidNameTaskError,
    InvalidDateTimeError,
    InvalidTaskCategoryError,
    InvalidDescriptionTaskError,
    InvalidWeekdayError,
)


class TaskEntity(Entity[TaskModel]):
    def __init__(self, props: TaskModel) -> None:
        self._validate(props)
        super().__init__(props)
        self.type = props["type"]
        self.name = props["name"]
        self.date_time: datetime = cast(datetime, props["date_time"])
        self.category = props["category"]
        self.description = props["description"]
        self.weekdays: Optional[list[Weekday]] = props.get("weekdays")
        self.finally_datetime: datetime = cast(datetime, props["finally_datetime"])
        self.user_id = props["user_id"]

    def _validate(self, props: TaskModel) -> None:
        self._clear_errors()
        self._create_id(props.get("id"))
        self.__validate_user_id(props.get("user_id", ""))

        self.__validate_types(cast(TaskType, props.get("type")))
        self.__validate_categories(cast(TaskCategories, props.get("category")))
        props["name"] = self.__validate_name(props.get("name", ""))
        props["date_time"] = cast(
            str, self.__validate_date_time(props.get("date_time", ""))
        )
        props["description"] = self.__validate_description(props.get("description", ""))
        self.__validate_list_weekdays(props.get("weekdays"))
        props["finally_datetime"] = cast(
            str, self.__validate_finally_date_time(props.get("finally_datetime"))
        )

        self._raize_errors()

    def __validate_user_id(self, value: str) -> None:
        if not value or not UuidAdapter.validate_uuid4(value):
            self._add_error(InvalidIdError("user_id", "TaskEntity"))

    def __validate_types(self, value: TaskType) -> None:
        list_types = list(get_args(TaskType))

        if value not in list_types:
            self._add_error(InvalidTaskTypeError())

    def __validate_name(self, value: str) -> str:
        strip_value = value.strip() if value else value

        if not strip_value or len(strip_value) > 50:
            self._add_error(InvalidNameTaskError())

        return strip_value

    def __validate_date_time(self, value: str) -> datetime:
        try:
            return self.__parse_str_to_datetime(value)
        except Exception:
            self._add_error(InvalidDateTimeError())
            return cast(datetime, None)

    def __validate_categories(self, value: TaskCategories) -> None:
        list_categories = list(get_args(TaskCategories))

        if value not in list_categories:
            self._add_error(InvalidTaskCategoryError())

    def __validate_description(self, value: str) -> str:
        strip_value = value.strip() if value else value

        if not strip_value or len(strip_value) > 1000:
            self._add_error(InvalidDescriptionTaskError())

        return strip_value

    def __validate_list_weekdays(self, value: Optional[list[Weekday]]) -> None:
        if not value or len(value) == 0:
            return

        list_categories = list(get_args(Weekday))

        for item in value:
            if item not in list_categories:
                self._add_error(InvalidWeekdayError())
                return

    def __validate_finally_date_time(self, value: Optional[str]) -> datetime | None:
        try:
            if not value:
                return None

            return self.__parse_str_to_datetime(value)
        except Exception:
            self._add_error(InvalidDateTimeError("finally_datetime"))
            return cast(datetime, None)

    def __parse_str_to_datetime(self, value: str) -> datetime:
        date_formats = [
            "%Y/%m/%d",
            "%Y/%m/%d %H:%M",
            "%Y/%m/%d %H:%M:%S",
            "%Y/%m/%dT%H:%M:%S",
        ]

        for date_format in date_formats:
            try:
                return datetime.strptime(value, date_format)
            except (ValueError, TypeError):
                continue

        raise ValueError("Invalid date format")
