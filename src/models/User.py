from typing import Optional
from sqlmodel import SQLModel, Field

from datetime import datetime, timezone


class User(SQLModel, table=True):

    id: Optional[int] = Field(primary_key=True, index=True)
    email: str = Field(str, unique=True, nullable=False, index=True)
    password: str = Field(str, nullable=False)
    first_name: Optional[str] = Field(str, nullable=False)
    last_name: Optional[str] = Field(str, nullable=False)
    account_created: Optional[datetime] = Field(default=datetime.now(timezone.utc))
    account_updated: Optional[datetime] = Field(default=datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return f"id={self.id!r}, email={self.email!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, account_created={self.account_created.__str__()!r}, account_updated={self.account_updated.__str__()!r}"
