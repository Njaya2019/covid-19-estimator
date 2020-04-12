from flask import Blueprint, jsonify, request, Response
from form_validator import FormValidator
from src.estimator import estimator
import xmltodict

# creates a blueprint object called estimate_blueprint

estimate_blueprint = Blueprint('estimate', __name__)

# An endpoint for handling estimator POST request


@estimate_blueprint.route(
    '/api/v1/on-covid-19/', methods=["GET", "POST"]
)
@estimate_blueprint.route(
    '/api/v1/on-covid-19/<path:dataformat>', methods=["GET", "POST"]
)
def estimator_endpoint(dataformat=None):

    """An endpoint to handle estimator data posted"""

    # required form keys

    form_keys = (
        "periodType", "timeToElapse", "region",
        "reportedCases", "population", "totalHospitalBeds"
    )

    data = ''
    # If the request is a post request

    if request.method == "POST":

        # Gets form data and converts it to a dict

        if dataformat == 'json':

            data = request.get_json()

        elif dataformat == 'xml':

            data = request.get_data()

            data = xmltodict.parse(data)

        else:

            data = request.get_json()

        # Validating the form data

        formValues = FormValidator.checkEmptyValues(**data)

        formKeys = FormValidator.checkFormKeys(**data)

        formKeysValid = FormValidator.checkFormValidKeys(
            *form_keys, **data
        )

        # Tests if the form data are valid

        if not formValues:

            return jsonify({
                'status': 400,
                'error': 'Please provide all values for the form'
            }), 400

        elif not formKeys:

            return jsonify({
                'status': 400,
                'error': 'Please provide all keys for the form'
            }), 400

        elif not formKeysValid:

            return jsonify({
                'status': 400,
                'error': 'Please provide all valid keys for the form'
            }), 400

        else:

            strings_FormData = (data["region"]["name"], data["periodType"])

            formStringsSpaces =\
                FormValidator.checkAbsoluteSpaceCharacters(
                    *strings_FormData
                )

            if formStringsSpaces:

                return jsonify({
                    'status': 400,
                    'error': 'The form strings values can\'t be spaces'
                }), 400

            else:

                estimatedData = estimator(data)

                # Converts the estimates into a json abject

                return jsonify(estimatedData)

    return jsonify({
        "status": 200,
        "message": "Post covid-19 data and get the estimates"
    }), 200
