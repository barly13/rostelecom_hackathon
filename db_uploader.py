from pandas import DataFrame
from sqlalchemy import create_engine, MetaData, text

from clear_data_frames import ClearDataFrames


class DbUploader:
    DB_NAME = 'hackaton'
    DB_USER = 'postgres'
    DB_PASSWORD = '1234'
    DB_HOST = 'localhost'
    DB_PORT = '5432'

    def __init__(self):
        self.db_url = f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        self.engine = create_engine(self.db_url)

    def upload_df_to_sql(self, df: DataFrame, table_name: str):
        try:
            df.to_sql(
                table_name,
                self.engine,
                if_exists='append',
                index=False,
                method='multi'
            )
            print(f"Таблица {table_name} успешно заполнена")
        except Exception as e:
            print(f"Ошибка при обработке {table_name}: {str(e)}")

    def clear_data_in_tables(self):
        metadata = MetaData()
        metadata.reflect(bind=self.engine)

        with self.engine.connect() as connection:
            # Отключаем проверку внешних ключей
            connection.execute(text('SET session_replication_role = replica;'))
            # TRUNCATE для каждой таблицы
            for table in reversed(metadata.sorted_tables):
                connection.execute(text(f'TRUNCATE TABLE {table.name} CASCADE;'))
            connection.commit()

            # Включаем проверку внешних ключей обратно
            connection.execute(text('SET session_replication_role = default;'))


sql_uploader = DbUploader()
sql_uploader.clear_data_in_tables()

dfs = ClearDataFrames()
dfs.clear_data()

sql_uploader.upload_df_to_sql(dfs.product_category_name_translation, 'product_category_name_translation')
sql_uploader.upload_df_to_sql(dfs.products, 'products')
sql_uploader.upload_df_to_sql(dfs.customers, 'customers')
sql_uploader.upload_df_to_sql(dfs.orders, 'orders')
sql_uploader.upload_df_to_sql(dfs.order_reviews, 'order_reviews')
sql_uploader.upload_df_to_sql(dfs.order_payments, 'order_payments')
sql_uploader.upload_df_to_sql(dfs.sellers, 'sellers')
sql_uploader.upload_df_to_sql(dfs.geolocation, 'geolocation')
sql_uploader.upload_df_to_sql(dfs.orders_items, 'orders_items')




