from flask import Blueprint, jsonify, request, Response, g
from form_validator import FormValidator
from src.estimator import estimator
from dicttoxml import dicttoxml
from datetime import datetime

# creates a blueprint object called estimate_blueprint

estimate_blueprint = Blueprint('estimate', __name__)

# An endpoint for handling estimator POST request


@estimate_blueprint.route(
    '/api/v1/on-covid-19', methods=["GET", "POST"]
)
@estimate_blueprint.route(
    '/api/v1/on-covid-19/<string:dataformat>', methods=["GET", "POST"]
)
def estimator_endpoint(dataformat=None):

    """An endpoint to handle estimator data posted"""

    # required form keys

    form_keys = (
        "periodType", "timeToElapse", "region",
        "reportedCases", "population", "totalHospitalBeds"
    )

    # If the request is a post request

    if request.method == "POST":

        # Gets form data and converts it to a dict

        data = request.get_json()

        # Validating the form data, for keys and values

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

                # Checks if the path variable matches a json or an xml.

                if dataformat == 'json':

                    return jsonify(estimatedData)

                elif dataformat == 'xml':

                    xml_estimates = dicttoxml(estimatedData)

                    return xml_estimates

                else:

                    return jsonify(estimatedData)

    return jsonify({
        "status": 200,
        "message": "Post covid-19 data and get the estimates"
    }), 200

logs = []

# All requests to the blueprint


@estimate_blueprint.before_request
def before_a_request():

    """This Logs all requests issued in the app"""

    g.request_start_time = datetime.now()

    g.log_string = '{}   {}  '.format(request.method, request.path)


@estimate_blueprint.after_request
def after_a_request(response):

    """This Logs all requests issued in the app"""

    global logs

    g.request_time = datetime.now() - g.request_start_time

    g.log_string = '{}{}  {} ms\n'.format(
        g.log_string, response.status_code,
        g.request_time.microseconds
    )

    logs.append(g.log_string)

    return response


# Before and after requests logs endpoint


@estimate_blueprint.route(
    '/api/v1/on-covid-19/logs', methods=['GET']
)
def requests_logs():

    """This endpoint returns all requests and responses logs"""

    global logs

    string_logs = ''

    for log in logs:
        string_logs += log
    return string_logs
