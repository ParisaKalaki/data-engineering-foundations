from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import EnvironmentSettings, StreamTableEnvironment


def create_events_source_kafka(t_env):
    table_name = "green_trips_events"
    source_ddl = f"""
        CREATE TABLE {table_name} (
            lpep_pickup_datetime BIGINT,
            lpep_dropoff_datetime BIGINT,
            PULocationID INTEGER,
            DOLocationID INTEGER,
            passenger_count INTEGER,
            trip_distance DOUBLE,
            total_amount DOUBLE,
            dropoff_ts AS TO_TIMESTAMP_LTZ(lpep_dropoff_datetime, 3),
            WATERMARK FOR dropoff_ts AS dropoff_ts - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'properties.bootstrap.servers' = 'redpanda:29092',
            'topic' = 'green-trips',
            'scan.startup.mode' = 'earliest-offset',
            'properties.auto.offset.reset' = 'earliest',
            'format' = 'json'
        );
    """
    t_env.execute_sql(source_ddl)
    return table_name


def create_session_sink_postgres(t_env):
    table_name = "green_trip_session_streaks"
    sink_ddl = f"""
        CREATE TABLE {table_name} (
            PULocationID INTEGER,
            DOLocationID INTEGER,
            session_start TIMESTAMP(3),
            session_end TIMESTAMP(3),
            trip_streak BIGINT,
            session_seconds BIGINT,
            PRIMARY KEY (PULocationID, DOLocationID, session_start, session_end) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/postgres',
            'table-name' = '{table_name}',
            'username' = 'postgres',
            'password' = 'postgres',
            'driver' = 'org.postgresql.Driver'
        );
    """
    t_env.execute_sql(sink_ddl)
    return table_name


def run_session_job():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.enable_checkpointing(10 * 1000)
    env.set_parallelism(1)

    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    t_env.get_config().set("parallelism.default", "1")

    source_table = create_events_source_kafka(t_env)
    sink_table = create_session_sink_postgres(t_env)

    # Each row represents one uninterrupted streak per pickup/dropoff pair,
    # where the session ends if no trip arrives for 5 minutes.
    t_env.execute_sql(
        f"""
        INSERT INTO {sink_table}
        SELECT
            PULocationID,
            DOLocationID,
            window_start AS session_start,
            window_end AS session_end,
            COUNT(*) AS trip_streak,
            TIMESTAMPDIFF(SECOND, window_start, window_end) AS session_seconds
        FROM TABLE(
            SESSION(TABLE {source_table}, DESCRIPTOR(dropoff_ts), INTERVAL '5' MINUTES)
        )
        GROUP BY
            PULocationID,
            DOLocationID,
            window_start,
            window_end
        """
    ).wait()


if __name__ == "__main__":
    run_session_job()
