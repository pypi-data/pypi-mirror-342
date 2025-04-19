__version__ = '4.2.0'
__about__ = ""


def about() -> str:
    global __about__
    if __about__:
        return __about__

    import requests
    info = requests.get('https://pypi.org/pypi/phystool/json').json()['info']
    latest_version = info['version']
    current_version = __version__

    can_update = any(
        latest > current
        for latest, current in zip(
            latest_version.split('.'),
            current_version.split('.')
        )
    )

    __about__ = "<h4>{}</h4><h4>{}</h4><ul>{}</ul>".format(
        f"{current_version}: version actuelle",
        (
            f"{latest_version}: version disponible "
            if can_update
            else "Pas de nouvelle version"
        ),
        "".join([
            f"<li><a href='{value}'>{key}</a></li>"
            for key, value in info['project_urls'].items()
        ])
    )
    return __about__
