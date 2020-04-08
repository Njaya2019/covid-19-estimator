from json import loads, dumps


def estimator(data):

    # change json object to a python dictionary

    data = loads(data)

    # Best case

    bestCase = Covid19Cases.estimateBestCase(
        data['reportedCases'])

    # Worst case

    worstCase = Covid19Cases.estimateWorstCase(
        data['reportedCases'])

    # Estimated best case after a specified time

    bestCase_byTime = Covid19Cases.estimateCasesByTime(
        data['timeToElapse'], bestCase)

    # Estimated worst case after a specified time

    worstCase_byTime = Covid19Cases.estimateCasesByTime(
        data['timeToElapse'], worstCase)

    # Estimated best case for severe cases after a period of time

    bestCase_severeCases = Covid19Cases.estimatesevereCasesByRequestedTime(
        bestCase_byTime)

    # Estimated worst case for severe cases after a period of time

    worstCase_severeCases = Covid19Cases.estimatesevereCasesByRequestedTime(
        worstCase_byTime)

    # Estimated best case available hospital beds for severe cases

    bestCase_avalilableBeds = Covid19Cases.estimateAvailableHospitalBeds(
        data["totalHospitalBeds"], bestCase_severeCases)

    # Estimated worst case available hospital beds for severe cases

    worstCase_avalilableBeds = Covid19Cases.estimateAvailableHospitalBeds(
        data["totalHospitalBeds"], worstCase_severeCases)

    output_data = {
        "data": data,
        "impact": {
            "currentlyInfected": bestCase,
            "infectionsByRequestedTime": bestCase_byTime,
            "severeCasesByRequestedTime": bestCase_severeCases,
            "hospitalBedsByRequestedTime": bestCase_avalilableBeds
        },
        "severeImpact": {
            "currentlyInfected": worstCase,
            "infectionsByRequestedTime": worstCase_byTime,
            "severeCasesByRequestedTime": worstCase_severeCases,
            "hospitalBedsByRequestedTime": worstCase_avalilableBeds
        }
    }

    # Changes the output data dictionary to json

    estimated_output = dumps(output_data)

    return estimated_output

# A class containing all functions to estimate covid 19 cases


class Covid19Cases():

    @staticmethod
    def estimateBestCase(reported_cases):
        """Estimates the possibly infected people"""
        return float(reported_cases * 10)

    @staticmethod
    def estimateWorstCase(reported_cases):
        """Estimates the severe possibility of infected people"""
        return float(reported_cases * 50)

    @staticmethod
    def estimateCasesByTime(days, currently_infected):
        """Estimates the number of infections in specified days"""
        # calculates the factor

        factor = int(days / 3)

        # calculates the estimate of infections after specified days

        infenctions_after_specified_days = currently_infected * (2**factor)

        return float(infenctions_after_specified_days)

    @staticmethod
    def estimatesevereCasesByRequestedTime(infections_by_requested_time):
        """Estimates the percentage of positive cases that are severe"""
        severe_positive_cases = (15/100) * infections_by_requested_time
        return severe_positive_cases

    @staticmethod
    def estimateAvailableHospitalBeds(hospital_beds, severe_positive_cases):
        """Estimates hospital beds available for severe positive cases"""
        # calculates 90% hospital beds capacity utilized

        hospital_beds_utilized = (90/100) * hospital_beds

        # calculates the hospital beds available for severe cases

        available_hospital_beds = (35/100) * hospital_beds_utilized

        # if severe cases are higher than available beds return a,
        # negative number. Else return the available beds.

        if(severe_positive_cases > available_hospital_beds):
            return available_hospital_beds - severe_positive_cases
        else:
            return available_hospital_beds
