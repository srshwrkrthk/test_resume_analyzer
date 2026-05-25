def analyze_resume(text, role_data):

    text = text.lower()

    mandatory_found = []
    preferred_found = []
    bonus_found = []

    mandatory_missing = []
    preferred_missing = []

    mandatory_skills = role_data["mandatory"]
    preferred_skills = role_data["preferred"]
    bonus_skills = role_data["bonus"]


    for skill in mandatory_skills:

        if skill.lower() in text:
            mandatory_found.append(skill)

        else:
            mandatory_missing.append(skill)


    for skill in preferred_skills:

        if skill.lower() in text:
            preferred_found.append(skill)

        else:
            preferred_missing.append(skill)


    for skill in bonus_skills:

        if skill.lower() in text:
            bonus_found.append(skill)


    mandatory_score = (
        len(mandatory_found) / len(mandatory_skills)
    ) * 70

    preferred_score = (
        len(preferred_found) / len(preferred_skills)
    ) * 20

    bonus_score = (
        len(bonus_found) / len(bonus_skills)
    ) * 10

    final_score = (
        mandatory_score +
        preferred_score +
        bonus_score
    )

    return {

        "mandatory_found": mandatory_found,
        "preferred_found": preferred_found,
        "bonus_found": bonus_found,

        "mandatory_missing": mandatory_missing,
        "preferred_missing": preferred_missing,

        "match_score": round(final_score, 2)
    }