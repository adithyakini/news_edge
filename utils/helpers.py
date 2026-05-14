def filter_high_impact(results):

    filtered = []

    for r in results:

        if r["analysis"].get("high_impact") == True:
            filtered.append(r)

    return filtered
