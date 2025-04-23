import convomeld.validators
import doctest


def test_validator_doctests():
    failed, attempted = doctest.testmod(convomeld.validators)
    assert attempted > 0 and failed == 0


EXAMPLE_CONVOGRAPH = [
    {
        "name": "start",
        "convo_name": "botnar_microgrants",
        "convo_description": "grant_demo",
        "nlp": "keyword",
        "level": 0,
        "actions": {
            "en": [
                "Hi, I'm a chatbot at Fondation Botnar.",
                "We want to help urban youth around the world.",
            ]
        },
        "triggers": {"en": {"__next__": "microgrant_ideas"}},
    },
    {
        "name": "microgrant_ideas",
        "actions": {"en": ["Do you have any microgrant project ideas?"]},
        "triggers": {
            "en": {
                "I would like to start a youth training center for young girls in math.": "math_education",
                "youth": "math_education",
                "girls": "math_education",
                "math": "math_education",
                "__default__": "math_education",
            }
        },
    },
    {
        "name": "math_education",
        "actions": {
            "en": [
                "Excellent!",
                "This combines two of Fondation Botnar's focus areas - education and gender equity.",
                "Where are you located?",
            ]
        },
        "triggers": {
            "en": {"Kenya": "eastern_africa", "__default__": "eastern_africa"}
        },
    },
    {
        "name": "eastern_africa",
        "actions": {
            "en": [
                "Here is a link to some resources about math education in Kenya",
                '<a href="https://www.fondationbotnar.org/">Fondation Botnar website</a>',
            ]
        },
        "triggers": {"en": {"__default__": "stop"}},
    },
    {
        "name": "stop",
        "actions": {
            "en": [
                "Thank you!😇 We look forward to reading your application on our [website](https://www.fondationbotnar.org/)"
            ]
        },
        "triggers": {"en": {"__default__": "start"}},
    },
]


def test_is_valid():
    validator = convomeld.validators.ConvographValidator(EXAMPLE_CONVOGRAPH)
    assert validator.is_valid()
