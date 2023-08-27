def get_categories_and_factors() -> tuple[list, list]:
    category_names = (
        "Начальство",
        "Коллеги",
        "Условия работы",
        "Личные факторы и здоровье",
    )
    categories = [dict(id=i, name=name) for i, name in enumerate(category_names)]

    manager_factor_names = """демонстрирует негативные (деструктивные) черты характера
    проявляет профессиональную некомпетентность
    не желает конструктивно взаимодействовать
    оказывает психологическое давление
    показывает неуважение
    отказывается решать проблемы
    принуждает к сверхнормативной работе
    другое""".split(
        "\n"
    )
    manager_factor_names = [n.strip() for n in manager_factor_names]
    manager_factors = [
        dict(category_id=0, name=name, type="text" if name == "другое" else "single")
        for name in manager_factor_names
    ]

    colleague_factor_names = """демонстрируют негативные (деструктивные) черты характера
    проявляют профессиональную некомпетентность
    не желают конструктивно взаимодействовать
    оказывают психологическое давление
    показывают неуважение
    отказываются сотрудничать
    другое""".split(
        "\n"
    )
    colleague_factor_names = [n.strip() for n in colleague_factor_names]
    colleague_factors = [
        dict(category_id=1, name=name, type="text" if name == "другое" else "single")
        for name in colleague_factor_names
    ]

    work_factor_names = """некомфортные условия (температура, запыленность, шум и т.п.)
    слишком высокая интенсивность работы
    высокий уровень стресса
    необходимость работать сверхурочно
    простой из-за поломки оборудования или оргтехники
    плохая организация рабочего процесса
    другое""".split(
        "\n"
    )
    work_factor_names = [n.strip() for n in work_factor_names]
    work_factors = [
        dict(category_id=2, name=name, type="text" if name == "другое" else "single")
        for name in work_factor_names
    ]

    personal_factor_names = """проблемы в личной жизни
    низкий уровень мотивации к работе
    усталость и упадок сил
    плохое физическое самочувствие (нездоровится)
    плохое эмоциональное самочувствие (переживания, нет настроения и т.п.)
    необходимость работать, несмотря на болезнь
    другое""".split(
        "\n"
    )
    personal_factor_names = [n.strip() for n in personal_factor_names]
    personal_factors = [
        dict(category_id=3, name=name, type="text" if name == "другое" else "single")
        for name in personal_factor_names
    ]
    return (
        categories,
        manager_factors + colleague_factors + work_factors + personal_factors,
    )


def get_states() -> tuple[dict, ...]:
    return (
        {
            "id": 1,
            "name": "Плохо",
            "value": 100,
        },
        {
            "id": 2,
            "name": "Средне",
            "value": 200,
        },
        {
            "id": 3,
            "name": "Хорошо",
            "value": 300,
        },
    )
