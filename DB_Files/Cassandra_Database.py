import  pandas as pd
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from Logger.logging import App_Logger

log = App_Logger()

class CassandraDBManagement:
    def __init__(self):
        try:
            cloud_config= {
                     'secure_connect_bundle': "E:\Academics\Data Science\Project\Income Prediction\My Project\secure-connect-test1.zip"
            }
            auth_provider = PlainTextAuthProvider('ifQGDYedNKbXYaMfcnXzMZtR', 'lpeFqpZ-DGMnSno51aZ,D-To7C6OA.nOwlwBWeW8OmBJdQN8eerfQxE_,Ns1s2imlRG7qpuTt3tBAs7x1+UfB20PoB2L5U4OkuH0Qe+zh.Go62FOt68KW,ZeHDhq+mPa')
            self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = self.cluster.connect()
            #print(self.session.execute("select release_version from system.local").one())
            log.log("inside init of CassandraDBManagement Class object created successufully")
        except Exception as e:
            log.log("Exception occured while creating object of CassandraDBManagement class")
            pass

    def shutdown_session(self):
        try:
            log.log("Entered try block of shutdown_session function ")
            self.session.shutdown()
        except Exception as e:
            log.log("Entered Except block of shutdown_session function ")
            pass
    def get_Session(self):
        log.log("inside get_Session function")
        return self.session

    def create_Keyspace(self,name):
        try:
            log.log("inside try bock of create_Keyspace function")
            string = f"CREATE KEYSPACE {name} WITH replication = {{\'class\':\'SympleStrategy\',\'replication_factor\':3}}"
            print(string)
            self.session.execute(string)
        except Exception as e:
            log.log("Exception bock of create_Keyspace function")
            return e

    def get_keyspaces(self):
        try:
            log.log("inside try bock of get_Keyspace function")
            lst = list()
            for i in self.session.execute("SELECT * FROM system_schema.keyspaces;"):
                if (i.keyspace_name not in ["datastax_sla","system_auth","system_schema","data_endpoint_auth","system","system_traces"]):
                    lst.append(i.keyspace_name)
            return lst
        except Exception as e:
            log.log("inside exception block of get_Keyspace function")
            return e

    def is_keyspace_present(self,name):
        try:
            log.log("inside try block of is_Keyspace_presetn function")
            if (name in self.get_keyspaces()):
                return True
            return False
        except Exception as e:
            log.log("inside try block of is_Keyspace_presetn function")
            return e

    def create_table(self,keyspace,structure):

        """Creates the table in keyspace using strucutre which specify column names and datatupes and keys"""
        try:
            log.log("inside try block of create_table function")
            self.session.execute(f"USE {keyspace} ;")
            self.session.execute(structure)
            return("table created !")
        except Exception as e:
            log.log("Exception block of create_table function")
            return e

    def get_column_names(self,keyspace,table_name):
        """Returns the column names of specific table in particular keyspace"""
        try:
            log.log("inside try block of get_column_names function")
            self.session.execute(f"USE {keyspace} ;")
            return self.session.execute(f"SELECT * FROM {table_name} ;").column_names
        except Exception as e:
            log.log("inside Exception block of get_column_names function")
            return e

    def drop_table(self,keyspcace,table_name):
        try:
            log.log("inside try block of drop_table function")
            self.session.execute(f'USE {keyspcace}')
            self.session.execute(f"DROP {table_name}")
        except Exception as e:
            log.log("inside Except block of drop_table function")
            print(e)

    def upload_data_to_DB(self,keyspace):
        try:
            log.log("inside try block of upload_data_to_DB function")
            (os.chdir(os.getcwd()[:63]))
            path = (os.getcwd()[:63] + "\\" + f"Data\Scraped Data\{os.listdir('Data/Scraped Data')[0]}")
            data = pd.read_csv(path)
            table_name = path[81:-4]


            if self.is_keyspace_present(keyspace):
                self.session.execute(f"USE {keyspace};")

            else:
                return "Keyspace not present"
            if (self.create_table(keyspace,
                                 f"CREATE TABLE {table_name} (Date TEXT PRIMARY KEY,Price FLOAT,Volume Float) ;")) == "table created !":
                self.log_keyspaces_table_names(keyspace, table_name)
                for i in (data.values):
                    string = f"INSERT INTO {keyspace}.{table_name}(Date,Price,Volume) VALUES{i[0], i[1], i[2]}"
                    self.session.execute(string)
                log.log(f"New table named {keyspace}.{table_name} created and values inserted in cloud DB")
            else:
                for i in (data.values):
                    string = f"INSERT INTO {keyspace}.{table_name} (Date,Price,Volume) VALUES{i[0], i[1], i[2]}"
                    self.session.execute(string)
                log.log(f"table named {keyspace}.{table_name} aldready exist and values inserted in cloud DB")
            log.log("upload_data_to_DB function executed successfully and data fetch from DB returned")
            return (self.session.execute(f"select * from {keyspace}.{table_name};").current_rows)

        except Exception as e :

            return e
    def fetch_data_from_table_in_DB(self,keyspace):
        try:
            log.log("Entered Try block of fetch_data_from_table_in_DB")
            self.session.execute(f"USE {keyspace} ;")

            (os.chdir(os.getcwd()[:63]))
            path = (os.getcwd()[:63] + "\\" + f"Data\Scraped Data\{os.listdir('Data/Scraped Data')[0]}")
            table_name = path[81:-4]
            log.log(f"data from remote table named {keyspace}.{table_name} retrieved successfully")
            return self.session.execute(f"select * from {keyspace}.{table_name};").current_rows
        except Exception as e:
            log.log("Entered Exception block of fetch_data_from_table_in_DB")
            return e

    # @staticmethod
    def log_keyspaces_table_names(self,keyspace, table):
        try:
            log.log("Entered Try block of log_keyspaces_table_names function")
            os.chdir(os.getcwd()[:63])
            with open(os.getcwd()[:63] + "\DB_Files\keyspaces_tables_names.txt", 'a') as f:
                f.write(f"{keyspace}.{table}\n")
                f.close()
        except Exception as e:
            log.log("Entered Exception block of log_keyspaces_table_names function")
            pass




if __name__ == "__main__":

    obj = CassandraDBManagement()
    obj.upload_data_to_DB('demo')
    print(obj.fetch_data_from_table_in_DB('demo'))



