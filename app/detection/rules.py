def is_malicious(data):
    score = data["data"]["abuseConfidenceScore"]
    return score > 70