import os
import threading
import time
from datetime import datetime, timezone
from typing import Generator, Union

try:
    from sqlalchemy.engine import Connection as SQLAlchemyConnection
except ImportError:
    SQLAlchemyConnection = None


shared_benchmark = None


class Benchmark:
    def __init__(
        self,
        db_connection: Union[any, "SQLAlchemyConnection"],
        number_of_runs: int = 1,
        visualize: bool = False,
    ):
        """
        :param db_connection: psycopg2 or SQLAlchemy connection object
        :param number_of_runs: How many times to run the SQL
        :param visualize: If True, start a local webserver to show results
        """
        self.sql_query = None
        self.db_connection = db_connection
        self.number_of_runs = number_of_runs
        self.execution_times = []
        self._run_timestamps = []
        self._paused = False
        self._visualize = visualize
        self._webserver_thread = None
        self._is_sqlalchemy = SQLAlchemyConnection is not None and isinstance(db_connection, SQLAlchemyConnection)

        global_bench = self

        if self._visualize:
            self._start_web_server()

    def set_sql(self, query: str):
        if os.path.isfile(query):
            with open(query, "r", encoding="utf-8") as f:
                self.sql_query = f.read().strip()
        else:
            self.sql_query = query

    def get_sql(self) -> str:
        return self.sql_query

    def __iter__(self) -> Generator[dict, None, None]:
        if not self.db_connection:
            raise ValueError("Database connection is not set.")
        if not self.sql_query:
            raise ValueError("SQL query is not set.")

        self.execution_times = []
        self._run_timestamps = []

        for i in range(self.number_of_runs):
            while self._paused:
                time.sleep(0.1)

            start_time = time.time()
            timestamp_sent = datetime.now(timezone.utc)

            try:
                if self._is_sqlalchemy:
                    self.db_connection.execute(self.sql_query)
                    self.db_connection.commit()
                else:
                    cursor = self.db_connection.cursor()
                    cursor.execute(self.sql_query)
                    self.db_connection.commit()
                    cursor.close()
            except Exception as e:
                raise RuntimeError(f"Error executing query: {e}") from e

            end_time = time.time()
            duration = round(end_time - start_time, 6)
            duration_str = format(duration, '.6f').rstrip('0').rstrip('.')

            record = {
                "sent_at": timestamp_sent.isoformat(),
                "duration": duration_str
            }
            self.execution_times.append(duration)
            self._run_timestamps.append(record)

            yield record

    def get_execution_results(self):
        if not self.execution_times:
            raise ValueError("Benchmark has not been run yet.")

        return {
            "runs": self.number_of_runs,
            "min_time": format(min(self.execution_times), '.6f').rstrip('0').rstrip('.'),
            "max_time": format(max(self.execution_times), '.6f').rstrip('0').rstrip('.'),
            "avg_time": format(sum(self.execution_times) / self.number_of_runs, '.6f').rstrip('0').rstrip('.')
        }

    def get_execution_timeseries(self):
        if not self.execution_times:
            raise ValueError("Benchmark has not been run yet.")
        return self._run_timestamps

    def _start_web_server(self):
        try:
            from fastapi import FastAPI
            from fastapi.responses import HTMLResponse, JSONResponse
            import uvicorn
        except ImportError:
            raise ImportError("FastAPI and uvicorn are required for visualization. Install with: pip install fastapi uvicorn")

        app = FastAPI()

        @app.get("/", response_class=HTMLResponse)
        def index():
            return """
            <html>
            <head>
                <title>Benchmark Timeseries</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
                <h2>Query Duration (Seconds)</h2>
                <canvas id="myChart" width="800" height="400"></canvas>
                <script>
                    async function loadData() {
                        const res = await fetch('/data');
                        const json = await res.json();
                        const labels = json.map(d => d.sent_at);
                        const data = json.map(d => parseFloat(d.duration));

                        const ctx = document.getElementById('myChart').getContext('2d');
                        new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: labels,
                                datasets: [{
                                    label: 'Query Duration (s)',
                                    data: data,
                                    fill: false,
                                    borderColor: 'rgb(75, 192, 192)',
                                    tension: 0.1
                                }]
                            },
                            options: {
                                responsive: true,
                                scales: {
                                    x: { display: true, title: { display: true, text: 'Timestamp' }},
                                    y: { display: true, title: { display: true, text: 'Seconds' }}
                                }
                            }
                        });
                    }

                    loadData();
                    setInterval(() => location.reload(), 3000);
                </script>
            </body>
            </html>
            """

        @app.get("/data")
        def get_data():
            return JSONResponse(self._run_timestamps)

        def run_server():
            uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")

        self._webserver_thread = threading.Thread(target=run_server, daemon=True)
        self._webserver_thread.start()
