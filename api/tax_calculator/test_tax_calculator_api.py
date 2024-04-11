import os
import json


brackets_dir = os.path.join(os.path.dirname(__file__), 'fixtures')


def _get_brackets(tax_year):
    """
    Get tax brackets for a specific year.

    Parameters:
        tax_year (str): The tax year for which to retrieve the brackets.

    Returns:
        dict: A dictionary containing the tax brackets for the specified year.
    """
    filename = f'tax-brackets--{tax_year}.json'
    file_with_path = os.path.join(brackets_dir, filename)

    with open(file_with_path) as config_file:
        json_contents = json.load(config_file)
        config_file.close()

    return json_contents


def test_basic_route(client):
    """
    Test the basic route for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/')
    brackets = _get_brackets('2022')
    assert resp.json == {'tax_brackets': brackets}


def test_valid_input(client):
    """
    Test valid input for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/?salary=100000&tax_year=2021')
    assert resp.status_code == 200
    data = resp.json
    assert 'total_tax' in data
    assert 'tax_bands' in data
    assert 'effective_rate' in data


def test_invalid_tax_year(client):
    """
    Test invalid tax year input for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/?salary=100000&tax_year=2018')
    assert resp.status_code == 400
    error = resp.json['errors'][0]
    assert error['code'] == ''
    assert error['field'] == 'tax_year'
    assert 'Invalid tax year' in error['message']


def test_negative_salary(client):
    """
    Test negative salary input for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/?salary=-10000&tax_year=2022')
    assert resp.status_code == 400
    error = resp.json['errors'][0]
    assert error['code'] == ''
    assert error['field'] == 'salary'
    assert 'positive value' in error['message']


def test_invalid_input_types(client):
    """
    Test invalid input types for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/?salary=abc&tax_year=2022')
    assert resp.status_code == 400
    error = resp.json['errors'][0]
    assert error['code'] == ''
    assert 'Invalid input types' in error['message']


def test_no_params(client):
    """
    Test no parameters provided for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/')
    assert resp.status_code == 400
    error = resp.json['errors'][0]
    assert error['code'] == ''
    assert error['message'] == 'Both salary and tax_year parameters are required.'


def test_missing_salary(client):
    """
    Test missing salary parameter for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/?tax_year=2022')
    assert resp.status_code == 400
    error = resp.json['errors'][0]
    assert error['code'] == ''
    assert error['field'] == 'salary'
    assert 'required' in error['message']


def test_missing_tax_year(client):
    """
    Test missing tax year parameter for the tax calculator API.

    Parameters:
        client: The Flask test client.

    Returns:
        None
    """
    resp = client.get('/tax-calculator/?salary=50000')
    assert resp.status_code == 400
    error = resp.json['errors'][0]
    assert error['code'] == ''
    assert error['field'] == 'tax_year'
    assert 'required' in error
