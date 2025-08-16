import uuid
from sqlalchemy import String, Text, Float, ForeignKey, DateTime, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class TimeSeries(Base):
    __tablename__ = "time_series"
    __table_args__ = (UniqueConstraint("series_id", "version", name="uix_series_id_version"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    series_id: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    data_points: Mapped[list["DataPoint"]] = relationship(
        "DataPoint"
    )
    models: Mapped[list["ModelVersion"]] = relationship(
        "ModelVersion"
    )

class DataPoint(Base):
    __tablename__ = "data_points"
    __table_args__ = (UniqueConstraint("time_series_id", "timestamp", name="uix_time_series_id_timestamp"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    time_series_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("time_series.id", ondelete="CASCADE"), nullable=False)
    timestamp: Mapped[str] = mapped_column(Text, nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    time_series: Mapped["TimeSeries"] = relationship("TimeSeries")

class ModelVersion(Base):
    __tablename__ = "model_version"
    __table_args__ = (UniqueConstraint("time_series_id", "version", name="uix_time_series_id_version"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    time_series_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("time_series.id", ondelete="CASCADE"), nullable=False)
    version: Mapped[str] = mapped_column(String(32), nullable=False)
    mean: Mapped[float] = mapped_column(Float, nullable=False)
    std: Mapped[float] = mapped_column(Float, nullable=False)
    trained_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    time_series: Mapped["TimeSeries"] = relationship("TimeSeries")