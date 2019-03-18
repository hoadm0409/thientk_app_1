from utilities import Setting


def get_db_connect_string():
    """
    Base information on setting.py, generate database connection string.
    :return: database connection string
    """
    return "mysql+mysqldb://{}:{}@{}:{}/{}".format(
        Setting.DB_USER,
        Setting.DB_PASSWORD,
        Setting.DB_HOST,
        Setting.DB_PORT,
        Setting.DB_NAME
    )
