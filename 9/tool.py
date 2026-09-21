def getPersonalInfo(profileData):
    """Returns Sunan Rabbi's contact details, bio, links, and education."""
    return {
        "personal_info": profileData["personal_info"],
        "education": profileData["education"]
    }


def getSkills(profileData,category="all"):
    """
    Returns skills. Can filter by:
    'languages', 'frontend', 'backend', 'databases', 'cloud', 'monitoring', 'data_analysis', 'ai', or 'all'.
    """
    cat = category.lower().strip()
    skills = profileData["technical_skills"]

    category_mapping = {
        "language": skills["languages"],
        "frontend": skills["frontend"],
        "backend": skills["backend_and_api"],
        "database": skills["databases_and_caching"],
        "cloud": skills["cloud_and_devops"],
        "devops": skills["cloud_and_devops"],
        "monitoring": skills["monitoring_and_observability"],
        "data_analysis": skills["data_analysis_and_mining"],
        "ai": skills["ai_and_machine_learning"],
        "ml": skills["ai_and_machine_learning"]
    }

    for key, val in category_mapping.items():
        if key in cat:
            return {key: val}

    return skills


def getExperience(profileData,company="all"):
    """Returns professional work experience, achievements, and companies."""
    comp = company.lower().strip()
    if comp != "all":
        matched = [
            exp for exp in profileData["work_experience"]
            if comp in exp["company"].lower()
        ]
        if matched:
            return matched

    return profileData["work_experience"]


def getProjects(profileData,query="all"):
    """
    Returns project overviews and technical challenges solved.
    Accepts project keywords like 'prescription', 'healthcare', 'ticket', 'inventory', 'ecommerce', or 'all'.
    """
    q = query.lower().strip()
    if q != "all":
        matched = [
            p for p in profileData["projects"]
            if q in p["name"].lower() or q in p["id"].lower()
        ]
        if matched:
            return matched

    return profileData["projects"]


def getCertificationsAndLeadership(profileData):
    """Returns certifications, awards, competitions, and leadership activities."""
    return profileData["organizations_and_awards"]



tools = {
    "getPersonalInfo": getPersonalInfo,
    "getSkills": getSkills,
    "getExperience": getExperience,
    "getProjects": getProjects,
    "getCertificationsAndLeadership": getCertificationsAndLeadership
}