from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    def __repr__(self) -> str:
        fields = ", ".join(
            f"{key}={value!r}" for key, value in self.__dict__.items() if not key.startswith("_")
        )
        return f"<{self.__class__.__name__}({fields})>"
