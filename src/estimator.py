def estimator(data):
    bestCase = Covid19Cases.estimateImpactCurrentlyInfected(
        data['reportedCases'])

    output_data = {
        "data": data,
        "impact": {
            "currentlyInfected": bestCase,
            "infectionsByRequestedTime": Covid19Cases.estimateInfectionsByTime(
                data['timeToElapse'], 
                Covid19Cases.estimateImpactCurrentlyInfected(
                    data['reportedCases']))},
        "severeImpact": {
            "currentlyInfected": Covid19Cases.estimateSevereCurrentlyInfected(
                data['reportedCases']),
            "infectionsByRequestedTime": Covid19Cases.estimateInfectionsByTime(
                data['timeToElapse'], 
                Covid19Cases.estimateSevereCurrentlyInfected(
                    data['reportedCases'])),
        },
    }
    return output_data

# A class containing all functions to estimate covid 19 cases


class Covid19Cases():

    @staticmethod
    def estimateImpactCurrentlyInfected(reported_cases):
        """Estimates the possibly infected people"""
        return float(reported_cases * 10)

    @staticmethod
    def estimateSevereCurrentlyInfected(reported_cases):
        """Estimates the severe possibility of infected people"""
        return float(reported_cases * 50)

    @staticmethod
    def estimateInfectionsByTime(days, currently_infected):
        """Estimates the number of infections in specified days"""
        # calculates the factor

        factor = int(days / 3)

        # calculates the estimate of infections in the specified days

        infenctions_after_specified_days = currently_infected * (2**factor)

        return float(infenctions_after_specified_days)
