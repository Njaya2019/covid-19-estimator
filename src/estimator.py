from json import loads

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

    output_data = {
        "data": data,
        "impact": {
            "currentlyInfected": bestCase,
            "infectionsByRequestedTime": bestCase_byTime
        },
        "severeImpact": {
            "currentlyInfected": worstCase,
            "infectionsByRequestedTime": worstCase_byTime
        }
    }
    return output_data

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
