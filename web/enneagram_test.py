from collections import Counter

VALID_CHOICES = frozenset("ABCDEFGHI")

ENNEATYPE_BY_LETTER = {
    "A": ("1", "Perfeccionista"),
    "B": ("2", "Ayudador"),
    "C": ("3", "Logrador"),
    "D": ("4", "Individualista"),
    "E": ("5", "Investigador"),
    "F": ("6", "Leal"),
    "G": ("7", "Entusiasta"),
    "H": ("8", "Desafiador"),
    "I": ("9", "Pacificador"),
}

QUESTIONS = [
    {
        "id": "q1",
        "text": "¿Qué te mueve más?",
        "options": [
            ("A", "Hacer lo correcto, mejorar, ser íntegra"),
            ("B", "Sentirte querida y necesaria"),
            ("C", "Lograr, destacarte, ser reconocida"),
            ("D", "Ser auténtica, especial, profunda"),
            ("E", "Entender, analizar, necesitar poco"),
            ("F", "Sentirte segura, prever riesgos"),
            ("G", "Disfrutar, evitar el dolor, experimentar"),
            ("H", "Tener control, ser fuerte, no depender"),
            ("I", "Estar en paz, evitar conflictos"),
        ],
    },
    {
        "id": "q2",
        "text": "¿Qué evitás más?",
        "options": [
            ("A", "Equivocarte / ser imperfecta"),
            ("B", "Ser rechazada o no querida"),
            ("C", "Fracasar o no valer"),
            ("D", "Ser común o superficial"),
            ("E", "Sentirte invadida o inútil"),
            ("F", "Quedarte sin apoyo o guía"),
            ("G", "Sufrir o sentir dolor emocional"),
            ("H", "Ser vulnerable o débil"),
            ("I", "El conflicto o la tensión"),
        ],
    },
    {
        "id": "q3",
        "text": "¿Cómo reaccionás bajo estrés?",
        "options": [
            ("A", "Me vuelvo más crítica y exigente"),
            ("B", "Me sobreinvolucro con otros"),
            ("C", "Me obsesiono con el rendimiento"),
            ("D", "Me pongo más emocional/intensa"),
            ("E", "Me aislo y me cierro"),
            ("F", "Me lleno de dudas y ansiedad"),
            ("G", "Escapo o evito con distracciones"),
            ("H", "Me pongo más controladora"),
            ("I", "Me desconecto o adormezco"),
        ],
    },
    {
        "id": "q4",
        "text": "¿Qué suelen decir de vos?",
        "options": [
            ("A", "Perfeccionista"),
            ("B", "Generosa"),
            ("C", "Exitosa"),
            ("D", "Sensible"),
            ("E", "Reservada"),
            ("F", "Responsable"),
            ("G", "Divertida"),
            ("H", "Fuerte"),
            ("I", "Tranquila"),
        ],
    },
]

OPTION_LABEL_BY_QUESTION = {
    q["id"]: {letter: label for letter, label in q["options"]} for q in QUESTIONS
}


def calculate_result(answers: dict[str, str]) -> dict:
    counts = Counter(answers.values())
    max_count = max(counts.values())
    winners = sorted(letter for letter, count in counts.items() if count == max_count)
    primary = winners[0]
    tipo_num, tipo_name = ENNEATYPE_BY_LETTER[primary]
    return {
        "counts": dict(counts),
        "primary_letter": primary,
        "tipo_num": tipo_num,
        "tipo_name": tipo_name,
        "winners": winners,
        "is_tie": len(winners) > 1,
    }


def build_enneagram_email_body(
    *,
    nombre: str,
    email: str,
    answers: dict[str, str],
    result: dict,
) -> str:
    lines = [
        "Nueva respuesta — Test rápido de Eneagrama (sitio web Miryam Barovero)",
        "",
    ]
    if nombre:
        lines.append(f"Nombre: {nombre}")
    if email:
        lines.append(f"Email: {email}")
    if nombre or email:
        lines.append("")

    for index, question in enumerate(QUESTIONS, start=1):
        letter = answers[question["id"]]
        label = OPTION_LABEL_BY_QUESTION[question["id"]][letter]
        lines.append(f"{index}. {question['text']}")
        lines.append(f"   → {letter}. {label}")
        lines.append("")

    lines.append("——— RESULTADO ———")
    if result["is_tie"]:
        tied = ", ".join(
            f"{ENNEATYPE_BY_LETTER[l][0]} ({ENNEATYPE_BY_LETTER[l][1]})"
            for l in result["winners"]
        )
        lines.append(f"Empate entre: {tied}")
        lines.append(
            f"Predominante (primer máximo): Tipo {result['tipo_num']} — {result['tipo_name']}"
        )
    else:
        lines.append(
            f"Eneatipo predominante: Tipo {result['tipo_num']} — {result['tipo_name']} "
            f"(letra {result['primary_letter']})"
        )

    lines.append("")
    lines.append("Conteo por letra:")
    for letter in "ABCDEFGHI":
        count = result["counts"].get(letter, 0)
        tipo_num, tipo_name = ENNEATYPE_BY_LETTER[letter]
        lines.append(f"  {letter} → {count} (Tipo {tipo_num}: {tipo_name})")

    return "\n".join(lines)


def get_enneagram_emailjs_params(
    *,
    nombre: str,
    email: str,
    answers: dict[str, str],
    result: dict,
    to_email: str,
) -> dict[str, str]:
    from_name = nombre.strip() or "Participante test Eneagrama"
    from_email = email.strip() or "sin-email@miryambarovero.com.ar"
    return {
        "from_name": from_name,
        "from_email": from_email,
        "company": "Miryam Barovero — Test Eneagrama",
        "message": build_enneagram_email_body(
            nombre=nombre,
            email=email,
            answers=answers,
            result=result,
        ),
        "to_email": to_email,
    }
