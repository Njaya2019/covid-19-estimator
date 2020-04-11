from flask import Blueprint, jsonify, request, Response
from form_validator import FormValidator
from src.estimator import estimator
from dicttoxml import dicttoxml
from json import dumps

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
        "periodType", "timeToElapse", "region",
        "reportedCases", "population", "totalHospitalBeds"
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

                json_estimates = dumps(estimatedData)

                # If the output format variable is xml

                if outputformat == "xml":

                    # coverts dictionary to xml format

                    estimatedData_xml = dicttoxml(estimatedData)

                    # decodes the xml

                    xml = estimatedData_xml.decode()

                    xml_response = Response(
                        xml,
                        content_type='application/xml; charset=utf-8'
                    )
                    xml_response.headers.add(
                        'content-length', len(xml)
                    )
                    xml_response.status_code = 201

                    return xml_response

                # else return json format

                elif outputformat == 'json':

                    json_response = Response(
                        json_estimates,
                        content_type='application/json; charset=utf-8'
                    )
                    json_response.headers.add(
                        'content-length', len(json_estimates)
                    )
                    json_response.status_code = 201

                    return json_response

                else:

                    json_response = Response(
                        json_estimates,
                        content_type='application/json; charset=utf-8'
                    )
                    json_response.headers.add(
                        'content-length', len(json_estimates)
                    )
                    json_response.status_code = 201

                    return json_response

    return jsonify({
        "status": 200,
        "message": "Post covid-19 data and get the estimates"
    }), 200
