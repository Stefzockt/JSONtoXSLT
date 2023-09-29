def buildData(projectdetails:str):
    """
    Generates the README.md file for the project
    """
    with open(f"./output/{projectdetails['project_namespace']}/README.md","w") as f:
        f.write(f"# {projectdetails['name']}\n")
        f.write(f"## Beschreibung\n{projectdetails['description']}\n")
        f.write(f"### {projectdetails['creation_date']}\n")
        f.close()

