import json
from loguru import logger
from mdc_api import fetch_all_records
from metadata_api import MetadataClient
from .defines import MAX_RETRIES, TIMEOUT, SSL_VERIFY
from .Trace import Trace, enable_trace

__all__ = ['flatten_list', 'setup_logger']


def flatten_list(nested_list):
    """
    Recursively flatten a nested list.

    Parameters:
    - nested_list: The input nested list to be flattened.

    Returns:
    - A flattened list containing all elements of the input nested list.
    """
    flattened_list = []
    for item in nested_list:
        if isinstance(item, list):
            # If the element is a list, recursively flatten it
            flattened_list.extend(flatten_list(item))
        else:
            # If the element is not a list, append it to the flattened list
            flattened_list.append(item)
    return flattened_list


def setup_logger(log_file_path='./etl.log', level="INFO",
                 format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"):
    if not hasattr(setup_logger, "logger"):
        logger.add(log_file_path, rotation="500MB", level=level, format=format)
        setup_logger.logger = True


# @enable_trace
def connect_to_database(databasename):
    import sqlite3
    con = sqlite3.connect(database=databasename)
    return con


# @enable_trace
def load_data_from_file(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
            return data
    except Exception as error:
        logger.error(error)
        return None


def store_data_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def dump_data_from_mdc(service_interface):

    tables_full_list = [
        'facilities',
        'units',
        'topics',
        'data_group_types',
        'data_types',
        'experiment_types',
        'parameter_types',
        'repositories',
        'instrument_types',
        'sample_types',
        'samples',
        'instrument_cycles',
        'experiments',
        'beamtimes',
        'proposals_users',
        'instruments',
        'data_groups',
        'data_files',
        'parameters',
        'runs',
        'proposals',
        'techniques',
        'proposals_techniques',
        'users'
    ]
    tables_names = [
    ]

    for table_name in tables_names:
        logger.info(f'Fetch all data from {table_name}.')
        try:
            data = fetch_all_records(service_interface, table_name)
            store_data_to_file(data, f'./resources/{table_name}.json')
        except Exception as e:
            logger.error(e)
    return


def resolve_unit_info(units, attrs):
    try:
        unit_name = attrs.get('unitName', 'Unknown')
        unit_symbol = attrs.get('unitSymbol', 'N_A')
        unit_prefix_name = attrs.get('metricPrefixName', '')
        unit_prefix_symbol = attrs.get('metricPrefixSymbol', '')
        unit_id = next(unit["id"] for unit in units if unit["symbol"] == unit_symbol)  # [key for key, value in my_dictionary.items() if value == 93]
    except Exception as e:
        unit_id = -1
        logger.warning(e)

    return {"unit_name": unit_name, "unit_symbol": unit_symbol, "unit_id": unit_id, "unit_prefix_name": unit_prefix_symbol, "unit_prefix_symbol": unit_prefix_symbol}


def create_metadata_client(app_info, user_info):
    BASE_URL = app_info.get("url")
    # Generate the connection (example with minimum parameter options)
    return MetadataClient(client_id=app_info.get("id"),
                          client_secret=app_info.get("secret"),
                          user_email=user_info.get("email"),
                          token_url=BASE_URL + '/oauth/token',
                          refresh_url=BASE_URL + '/oauth/token',
                          auth_url=BASE_URL + '/oauth/authorize',
                          scope=app_info.get("scope"),
                          base_api_url=BASE_URL + '/api/',
                          max_retries=MAX_RETRIES,
                          timeout=TIMEOUT,
                          session_token=None,
                          ssl_verify=False)


@enable_trace
def create_parameter_data(key, data, attrs):
    #  Example: {'count': 6000.0, 'mean': 111.57698059082031, 'std': 2.211357831954956, 'min': 106.80351257324219, 'max': 116.29515075683594, 'med': 111.6604995727539}
    try:
        param = {
            'data_source': attrs['device'],
            'name': attrs['name'],
            'value': data['med'],
            'minimum': data['min'],
            'maximum': data['max'],
            'mean': data['mean'],
            'standard_deviation': data['std'],
            'data_type_id': 20,
            'parameter_type_id': 1,
            'unit_id': attrs['unit_id'],
            'unit_prefix': attrs['unit_prefix_name'],
            'flg_available': True,
            'description': attrs.get('alias', ''),
        }

        if not (float(data['min']) <= float(data['mean']) <= float(data['max'])):
            logger.warning(f"Invalid parameter: {key}\n{data}")
            param['mean'] = data['med']

        return param
    except Exception as e:
        logger.error(e)
        return None


@enable_trace
def load_configuration():
    app_info = load_data_from_file('./resources/local_app.json')
    user_info = load_data_from_file('./resources/user.json')

    return app_info, user_info


@logger.catch
def load_config_and_connect_to_metadata_catalog():
    app_info, user_info = load_configuration()
    if not (user_info and app_info):
        raise ValueError('Invalid application or user information')

    logger.debug(f'Application info: {app_info}')
    logger.debug(f'User info: {user_info}')

    logger.info(f'Connecting to Metadata service {app_info["url"]} ...')
    client_conn = create_metadata_client(app_info, user_info)

    return client_conn


def fetch_proposal_details(client_conn, proposal_number):
    try:
        proposal_info = client_conn.get_proposal_by_number_api(proposal_number).json()

        if 'id' not in proposal_info:
            raise ValueError(proposal_info["info"])  # ValueError(f"Unable to retrieve proposal info: {proposal_info}")

        return proposal_info
    except Exception as e:
        logger.error(e)
        return None


def fetch_run_details(client_conn, proposal_number, run_number):
    try:
        run_info = client_conn.get_runs_by_proposal_number_api(proposal_number, run_number).json()

        if 'runs' not in run_info:
            raise ValueError(run_info)  # ValueError(f"Unable to retrieve proposal info: {proposal_info}")

        run_id = run_info['runs'][0]['id']
        logger.debug(f'Run details by number ({run_number}):\n{json.dumps(run_info, indent=4)}')

        run_info = client_conn.get_run_by_id_api(run_id).json()
        return run_info
    except Exception as e:
        logger.error(e)
        return None


def fetch_data_group_details(client_conn, data_group_id):  # data_groups_repositories
    try:
        # if isinstance(data_groups_repositories, list) and len(data_groups_repositories):
        #     data_group_id = data_groups_repositories[0]['id']

        logger.debug(f'Retrieve data group info {data_group_id}')
        return client_conn.get_data_group_by_id_api(data_group_id).json()
    except Exception as e:
        logger.error(e)
        return None


def fetch_parameters_details(client_conn, parameters_ids):
    try:
        return [client_conn.get_parameter_by_id_api(id).json() for id in parameters_ids]
    except Exception as e:
        logger.error(e)
        None


def fetch_all_data_group_files(client_conn, data_group_id, prefix_path):
    try:
        data_files = client_conn.get_all_data_files_by_data_group_id_api(data_group_id).json()
        logger.debug(f"Data files:\n{json.dumps(data_files, indent=4)}")

        list_of_files = []
        for f in data_files:
            list_of_files.extend(eval(f['files']) if isinstance(f['files'], str) else f['files'])

        logger.debug(f'Data files per group ({data_group_id}):\n{json.dumps(list_of_files, indent=4)}')

        return [prefix_path + f["relative_path"] + f["filename"] for f in list_of_files]
    except Exception as e:
        logger.error(e)
        return None


def execute_load_data_to_metadata_catalog(client_conn, data_group_id, list_of_parameters, data_group_parameters, parameters):
    units = client_conn.get_all_units_api(0).json()
    mdc_ops_summary = []
    for param in data_group_parameters:
        try:
            logger.debug(f'Process parameter:\n{json.dumps(param, indent=4)}')

            full_name = param["data_source"] + '/' + param["name"]
            if full_name in list_of_parameters:
                value = list_of_parameters[full_name]
                parameter_id = param["id"]
                param = parameters[value]
                data = param['data']
                attrs = param['attributes']

                unit_info = resolve_unit_info(units, attrs)
                attrs |= unit_info
                param = create_parameter_data(value, data, attrs)

                res = client_conn.update_parameter_api(parameter_id, param).json()
                if 'id' in res:
                    # logger.info(f'Updated parameter (id:{parameter_id}) successful:\n{json.dumps(res, indent=4)}')
                    mdc_ops_summary.append({"action": "update", "id": res["id"], "device": res["data_source"], "property": res["name"]})
                    list_of_parameters.pop(full_name)
                else:
                    raise RuntimeError(f'Update parameter (id:{parameter_id}) failed:\n{res}')
            else:
                parameter_id = param["id"]
                res = client_conn.delete_parameter_api(parameter_id)
                logger.debug(f'Delete parameter ({param}):\n{res.status_code}')
                if res.status_code in [200, 204]:
                    mdc_ops_summary.append({"action": "delete", "id": param["id"], "device": param["data_source"], "property": param["name"]})
                else:
                    raise RuntimeError(f'Delete parameter (id:{parameter_id}) failed: {res.json()['info']}')
        except Exception as e:
            logger.warning(e)

    for key, value in list_of_parameters.items():
        param = parameters[value]

        data = param['data']
        attrs = param['attributes']
        unit_info = resolve_unit_info(units, attrs)
        attrs |= unit_info
        param = create_parameter_data(value, data, attrs)

        param['data_groups_parameters_attributes'] = [{'data_group_id': data_group_id}]
        # param['runs_parameters_attributes'] = [{'run_id': 2004}]

        res = client_conn.create_parameter_api(param).json()
        # logger.info(f'Insert parameter successful:\n{res}')
        mdc_ops_summary.append({"action": "create", "id": res["id"], "device": res["data_source"], "property": res["name"]})

    return mdc_ops_summary
