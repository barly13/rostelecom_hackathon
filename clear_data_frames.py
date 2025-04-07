import pandas as pd


class ClearDataFrames:
    def __init__(self):
        self.customers = pd.read_csv('./data/hackathon/customers.csv')
        self.geolocation = pd.read_csv('./data/hackathon/geolocation.csv')
        self.order_payments = pd.read_csv('./data/hackathon/order_payments.csv')
        self.order_reviews = pd.read_csv('./data/hackathon/order_reviews.csv')
        self.orders = pd.read_csv('./data/hackathon//orders.csv')
        self.orders_items = pd.read_csv('./data/hackathon/orders_items.csv')
        self.product_category_name_translation = pd.read_csv('./data/hackathon//product_category_name_translation.csv')
        self.products = pd.read_csv('./data/hackathon/products.csv')
        self.sellers = pd.read_csv('./data/hackathon/sellers.csv')

    def clear_data(self):
        self.__clear_products()
        self.__clear_reviews()
        self.__clear_payments()
        self.__clear_orders()
        self.__clear_orders_items()
        self.__clear_geolocation()
        self.__clear_product_category_name_translation()
        self.__clear_sellers()

    def __clear_products(self):
        indices_to_drop = self.products[
            ~self.products['product_category_name'].isin(self.product_category_name_translation['product_category_name'])].index
        self.products.drop(indices_to_drop, inplace=True)
        self.products.rename(columns={
            'product_name_lenght': 'product_name_length',
            'product_description_lenght': 'product_description_length'
        }, inplace=True)
        self.products.dropna(inplace=True)

    def __clear_reviews(self):
        self.order_reviews.drop(columns=['Unnamed: 0'], inplace=True)

    def __clear_payments(self):
        self.order_payments.drop(columns=['Unnamed: 0'], inplace=True)
        self.order_payments.drop_duplicates(inplace=True)

    def __clear_geolocation(self):
        used_zip_codes = pd.concat([
            self.sellers['seller_zip_code_prefix'],
            self.customers['customer_zip_code_prefix']
        ]).drop_duplicates()

        mask = ~self.geolocation['geolocation_zip_code_prefix'].isin(used_zip_codes)

        self.geolocation = self.geolocation[~mask].copy()
        self.geolocation.drop_duplicates(inplace=True)
        self.geolocation.drop(columns=['Unnamed: 0'], inplace=True)

    def __clear_orders(self):
        delivered = self.orders[self.orders['order_status'] == 'delivered']
        drop_i = delivered[delivered.isna().any(axis=1)].index  # delivered orders with NaN timestamps
        self.orders.drop(index=drop_i, inplace=True)
        self.orders.drop_duplicates(inplace=True)

    def __clear_orders_items(self):
        try:
            self.orders_items.drop(['freight_value.1', 'shipping_limit_date.1', 'price.1'], axis=1, inplace=True)
        except Exception:
            pass

        indices_to_drop = self.orders_items[~self.orders_items['order_id'].isin(self.orders['order_id'])].index
        self.orders_items.drop(indices_to_drop, inplace=True)

        indices_to_drop = self.orders_items[~self.orders_items['product_id'].isin(self.products['product_id'])].index
        self.orders_items.drop(indices_to_drop, inplace=True)

        self.orders_items.drop(columns=['Unnamed: 0'], inplace=True)

    def __clear_product_category_name_translation(self):
        self.product_category_name_translation.drop(columns=['Unnamed: 0'], inplace=True)

    def __clear_sellers(self):
        self.sellers.drop(columns=['Unnamed: 0'], inplace=True)