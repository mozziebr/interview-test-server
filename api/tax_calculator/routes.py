from flask import jsonify, redirect, request
from app import app
from . import controllers, error_handlers


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
    """Calculate total tax based on salary and tax year."""
    try:
        # Extracting query parameters from the request
        salary = float(request.args.get('salary'))
        tax_year = int(request.args.get('tax_year'))

        # Validating tax year
        if tax_year not in [2019, 2020, 2021, 2022]:
            return jsonify({
                'errors': error_handlers.format_error(
                    'Invalid tax year. Only years 2019, 2020, 2021, and 2022 are supported.',
                    field='tax_year'
                )
            }), 400

        # Validating salary
        if salary <= 0:
            return jsonify({
                'errors': error_handlers.format_error(
                    'Salary must be a positive value.',
                    field='salary'
                )
            }), 400

        # Calculating tax
        total_tax, tax_bands, effective_rate = controllers.calculate_tax(salary, tax_year)

        # Returning JSON response with total_tax, tax_bands, and effective_rate
        return jsonify({
            'total_tax': total_tax,
            'tax_bands': tax_bands,
            'effective_rate': effective_rate
        }), 200

    except ValueError:
        # Handling invalid input types
        return jsonify({
            'errors': error_handlers.format_error(
                'Invalid input types. Salary and tax_year must be numeric values.',
            )
        }), 400
    except Exception as e:
        # Handling other exceptions
        return jsonify({
            'errors': error_handlers.format_error(
                str(e),
            )
        }), 500