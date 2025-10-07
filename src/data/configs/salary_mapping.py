SALARY_RANGES = {
    'Intern': {
        'typical_range': (300, 600),         # стажери або часткова зайнятість
        'acceptable': (200, 800),
        'outlier_range': (150, 1000),        # нижче 150 або вище 1000 — підозріло
        'critical_range': (100, 1200),       # явно нереалістичні значення
        'note': 'Стажери, студенти, початкова практика'
    },

    'Junior': {
        'typical_range': (700, 1500),        # типовий джун
        'acceptable': (500, 1800),
        'outlier_range': (400, 2200),        # нижче 400 або вище 2200 — підозріло
        'critical_range': (300, 2500),       # поза межами цього — нереалістично
        'note': 'Джуни, які мають базовий досвід продакшн'
    },

    'Middle': {
        'typical_range': (1600, 3000),       # основна маса мідлів
        'acceptable': (1300, 3800),
        'outlier_range': (1000, 4500),       # нижче 1k або вище 4.5k — підозріло
        'critical_range': (800, 5500),       # явна помилка
        'note': 'Фахівці середнього рівня (Middle Engineer / Analyst)'
    },

    'Senior': {
        'typical_range': (3000, 5500),       # сеньйори
        'acceptable': (2500, 7000),
        'outlier_range': (2000, 8500),       # нижче 2k або вище 8.5k — червоний прапорець
        'critical_range': (1500, 10000),
        'note': 'Досвідчені розробники або технічні експерти'
    },

    'Lead': {
        'typical_range': (4500, 7500),       # тімліди, техліди
        'acceptable': (3500, 9000),
        'outlier_range': (2500, 10000),      # нижче 2.5k або вище 10k — підозріло
        'critical_range': (2000, 12000),
        'note': 'Технічні лідери, керівники команд'
    },

    'Staff+': {
        'typical_range': (6000, 9500),       # архітектори, експерти
        'acceptable': (5000, 12000),
        'outlier_range': (4000, 14000),      # нижче 4k або вище 14k — підозріло
        'critical_range': (3000, 16000),
        'note': 'Архітектори, Staff/Principal Engineers, експерти високого рівня'
    },

    'Management': {
        'typical_range': (5000, 9000),       # Engineering Manager, Head of Dept.
        'acceptable': (4000, 11000),
        'outlier_range': (3000, 13000),      # нижче 3k або вище 13k — дивно
        'critical_range': (2500, 15000),
        'note': 'Керівники команд, Delivery або Engineering Managers'
    },

    'C-level': {
        'typical_range': (9000, 18000),      # CTO, CIO, CDO, CEO у тех-компаніях
        'acceptable': (7000, 22000),
        'outlier_range': (5000, 25000),      # нижче 5k або вище 25k — підозріло
        'critical_range': (4000, 30000),
        'note': 'ТОП-менеджмент компаній або засновники із техбекграундом'
    }
}
