# формування діапазонів для перевіки на коректність даних
EXPERIENCE_RANGES = {
    'Intern': {
        'typical_range': (0, 1),
        'acceptable': (0, 2),
        'outlier_threshold': 3,        # 3+ років досвіду для інтерна — малоймовірно
        'critical_outlier': 4,
        'note': 'Стажери, студенти, випускники без комерційного досвіду'
    },

    'Junior': {
        'typical_range': (0.5, 2.5),
        'acceptable': (0, 3.5),
        'outlier_threshold': 4,        # 4+ років для джуна — підозріло
        'critical_outlier': 5,
        'note': 'Початковий рівень із базовим продакшн-досвідом'
    },

    'Middle': {
        'typical_range': (2, 5),
        'acceptable': (1.5, 7),
        'outlier_threshold': 8,        # 8+ років без росту — нетипово
        'critical_outlier': 10,
        'note': 'Фахівці середнього рівня, автономна робота над фічами'
    },

    'Senior': {
        'typical_range': (4, 9),
        'acceptable': (3, 12),
        'outlier_threshold': 2,        # менше 3 років досвіду — підозріло
        'critical_outlier': 1,
        'max_outlier': 20,             # більше 20 років — теж дивно
        'note': 'Досвідчені інженери, менторство, відповідальність за модулі/команди'
    },

    'Lead': {
        'typical_range': (6, 12),
        'acceptable': (5, 15),
        'outlier_threshold': 3,        # лід із 3 роками — фейк
        'critical_outlier': 2,
        'max_outlier': 20,
        'note': 'Технічні лідери, відповідальні за команду або архітектуру'
    },

    'Staff+': {
        'typical_range': (8, 15),
        'acceptable': (6, 18),
        'outlier_threshold': 5,
        'critical_outlier': 3,
        'max_outlier': 25,
        'note': 'Висококваліфіковані експерти, архітектори, технічні радники'
    },

    'Management': {
        'typical_range': (7, 15),
        'acceptable': (5, 18),
        'outlier_threshold': 4,
        'critical_outlier': 3,
        'max_outlier': 25,
        'note': 'Керівники команд, delivery/engineering managers'
    },

    'C-level': {
        'typical_range': (12, 25),
        'acceptable': (10, 30),
        'outlier_threshold': 7,        # C-level з 7 роками — підозріло
        'critical_outlier': 5,
        'max_outlier': 40,
        'note': 'ТОП-менеджмент: CTO, CIO, CDO, CEO у технічних компаніях'
    }
}
