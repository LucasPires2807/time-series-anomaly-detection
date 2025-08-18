import io

from fastapi import Depends
import matplotlib.pyplot as plt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db.database import get_db
from app.repository.plot_traning_repository import PlotTrainingRepository


class PlotTrainingService:
    def __init__(self, session: AsyncSession):
        self._repository = PlotTrainingRepository(session)

    async def plot(self, series_id: str, version: str):
        training_series = await self._repository.get_training_serie(
            series_id=series_id, version=version
        )
        params = await self._repository.get_params(
            series_id=series_id, version=version
        )
        mean, std = params["mean"], params["std"]
        anomaly_threshold = mean + 3 * std

        timestamps = []
        values = []
        anomalies = []
        for datapoint in training_series:
            timestamp = datapoint["timestamp"]
            value = datapoint["value"]
            timestamps.append(timestamp)
            values.append(value)
            if value > anomaly_threshold:
                anomalies.append((timestamp, value))


        fig, ax = plt.subplots(figsize=(12, 6))

        ax.axhline(
            y=anomaly_threshold, 
            color='red', 
            linestyle='--', 
            linewidth=2, 
            label=f'Anomaly Threshold ({anomaly_threshold:.2f})'
        )
        
        if anomalies:
            anom_t, anom_v = zip(*anomalies)
            ax.scatter(anom_t, anom_v, color='darkorange', s=100, zorder=3, label='Anomalous Points')
    
        ax.plot(timestamps, values, label=f'Time Series Data for {series_id}', color='royalblue', zorder=2)

        ax.set_title(f"Training Data for {series_id} (Version: {version})", fontsize=16)
        ax.set_xlabel("Timestamp", fontsize=12)
        ax.set_ylabel("Value", fontsize=12)
        ax.legend()
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)
        
        return buf

def get_plot_service(session=Depends(get_db)) -> PlotTrainingService:
    return PlotTrainingService(session=session)
