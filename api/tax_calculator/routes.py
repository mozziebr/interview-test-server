import logging

from flask import jsonify, redirect, request
from app import app
from . import controllers, error_handlers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/tax-calculator/')
def tax_calculator_instructions():
    """Provide instructions for tax calculator API."""
    return jsonify({
        'tax_brackets': controllers.get_reliable_brackets()
    })


@app.route('/tax-calculator/tax-year')
def default_brackets():
    """Redirect to default brackets."""
    return redirect('/')


@app.route('/tax-calculator', methods=['GET'])
def tax_calculator():
    """
    Calculate total tax based on salary and tax year.

    Returns:
        jsonify: JSON response containing total_tax, tax_bands, and effective_rate.
    """
    try:
        salary = float(request.args.get('salary'))
        tax_year = int(request.args.get('tax_year'))

        if tax_year not in [2019, 2020, 2021, 2022]:
            error_message = 'Invalid tax year. Only years 2019, 2020, 2021, and 2022 are supported.'
            logger.error(error_message)
            return jsonify({
                'errors': error_handlers.format_error(
                    error_message,
                    field='tax_year'
                )
            }), 400

        if salary <= 0:
            error_message = 'Salary must be a positive value.'
            logger.error(error_message)
            return jsonify({
                'errors': error_handlers.format_error(
                    error_message,
                    field='salary'
                )
            }), 400

        total_tax, tax_bands, effective_rate = controllers.calculate_tax(salary, tax_year)

        return jsonify({
            'total_tax': total_tax,
            'tax_bands': tax_bands,
            'effective_rate': effective_rate
        }), 200

    except ValueError:
        error_message = 'Invalid input types. Salary and tax_year must be numeric values.'
        logger.error(error_message)
        return jsonify({
            'errors': error_handlers.format_error(
                error_message,
            )
        }), 400
    except Exception as e:
        error_message = str(e)
        logger.error(error_message)
        return jsonify({
            'errors': error_handlers.format_error(
                error_message,
            )
        }), 500
