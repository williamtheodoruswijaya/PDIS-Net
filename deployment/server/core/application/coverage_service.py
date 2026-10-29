from core.domain.constants import LOW_TO_MODERATE, MODERATE_TO_HIGH

'''
For now, we hardcode the recommendation first ya
'''
RECOMMENDATIONS = {
    "none": "No plastic detected in this photo.",
    "low": "A little plastic. Check this spot again on the next routine flight.",
    "moderate": "Visible plastic patches. Add this spot to the next cleanup round.",
    "high": "Among the most plastic-covered spots in FloPWD. Prioritise it for cleanup.",
}

def coverage_level(coverage_pct):
    if coverage_pct == 0:
        return "none"
    if coverage_pct < LOW_TO_MODERATE:
        return "low"
    if coverage_pct < MODERATE_TO_HIGH:
        return "moderate"
    return "high"