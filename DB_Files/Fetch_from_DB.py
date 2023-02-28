from Cassandra_Database import CassandraDBManagement

obj = CassandraDBManagement()
print(obj.fetch_data_from_table_in_DB('demo','TATAMOTORS'))