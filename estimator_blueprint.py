from flask import Blueprint, jsonify, request, Response
from form_validator import FormValidator
from src.estimator import estimator
from dicttoxml import dicttoxml

# creates a blueprint object called estimate_blueprint

estimate_blueprint = Blueprint('estimate', __name__)

# An endpoint for handling estimator POST request


@estimate_blueprint.route(
    '/api/v1/on-covid-19/', methods=["GET", "POST"]
)
@estimate_blueprint.route(
    '/api/v1/on-covid-19/<path:outputformat>', methods=["GET", "POST"]
)
def estimator_endpoint(outputformat=None):

    """An endpoint to handle estimator data posted"""

    # required form keys

    form_keys = (
        "name", "avgAge", "avgDailyIncomeInUSD",
        "avgDailyIncomePopulation", "periodType",
        "timeToElapse", "reportedCases", "population",
        "totalHospitalBeds"
    )

    # If the request is a post request

    if request.method == "POST":

        # Gets form data and converts it to a dict

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

            strings_FormData = (data["name"], data["periodType"])

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

                dataToEstimate = {
                    "region": {
                        "name": data["name"],
                        "avgAge": data["avgAge"],
                        "avgDailyIncomeInUSD": data[
                            "avgDailyIncomeInUSD"
                        ],
                        "avgDailyIncomePopulation": data[
                            "avgDailyIncomePopulation"
                        ]
                    },
                    "periodType": data["periodType"],
                    "timeToElapse": data["timeToElapse"],
                    "reportedCases": data["reportedCases"],
                    "population": data["population"],
                    "totalHospitalBeds": data["totalHospitalBeds"]
                }

                estimatedData = estimator(dataToEstimate)

                # If the output format variable is xml

                if outputformat == "xml":

                    # coverts dictionary to xml format

                    estimatedData_xml = dicttoxml(estimatedData)

                    # decodes the xml

                    xml = estimatedData_xml.decode()

                    return Response(xml, mimetype='text/xml')

                # else return json format

                elif outputformat == 'json':

                    return jsonify(estimatedData), 201

                else:

                    return jsonify(estimatedData), 201

    return jsonify({
        "status": 200,
        "message": "Post covid-19 data and get the estimates"
    }), 200
