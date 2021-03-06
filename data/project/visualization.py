import math

from data.project.model import RentalDataset
import numpy as np
import matplotlib.pyplot as plt


def number_of_entries(dataset: RentalDataset) -> None:
    properties = ["Person.name", "CreditCard.credit_card_number"]
    values = [
        [person.name for person in dataset.people],
        [card.credit_card_number for card in dataset.creditcards]
    ]

    total_length = [len(value) for value in values]
    unique_length = [len(set(value)) for value in values]

    x = np.arange(len(properties))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    series_total = ax.bar(x - width / 2, total_length, width, label="Total")
    series_unique = ax.bar(x + width / 2, unique_length, width, label="Unique")

    ax.set_ylabel("Number of entities")
    ax.set_title("Number of total and unique values")
    ax.set_xticks(x)
    ax.set_xticklabels(properties)
    ax.legend()

    ax.bar_label(series_total, padding=3)
    ax.bar_label(series_unique, padding=3)

    fig.tight_layout()

    plt.show()


def cards_by_providers(dataset: RentalDataset) -> None:
    cards = list({card.credit_card_provider for card in dataset.creditcards})
    values = [0 for _ in cards]
    for card in dataset.creditcards:
        values[cards.index(card.credit_card_provider)] += 1

    x = np.arange(len(cards))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    series = ax.bar(x - width / 2, values, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Number of cards")
    ax.set_title("Number of providers per cards")
    ax.set_xticks(x)
    ax.set_xticklabels(cards, rotation=90)
    ax.bar_label(series)

    ax.tick_params(axis="both", which="major", labelsize=10)

    fig.tight_layout()

    plt.show()


def genres_by_songs(dataset: RentalDataset) -> None:
    genre = list({music.music_genre for music in dataset.songs})
    values = [0 for _ in genre]
    for music in dataset.songs:
        values[genre.index(music.music_genre)] += 1

    x = np.arange(len(genre))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    series = ax.bar(x - width / 2, values, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Number of genres")
    ax.set_title("Number of songs per genres")
    ax.set_xticks(x)
    ax.set_xticklabels(genre, rotation=90)
    ax.bar_label(series)

    ax.tick_params(axis="both", which="major", labelsize=10)

    fig.tight_layout()

    plt.show()

def distances_by_types_with_limit(dataset: RentalDataset) -> None:
    types = list({car.type for car in dataset.cars})
    values = [0 for _ in types]
    for transaction in dataset.transactions:
        car = next(car for car in dataset.cars if car.plate == transaction.car)
        values[types.index(car.type)] += transaction.length

    limit = 0.05

    total_length = sum([transaction.length for transaction in dataset.transactions])
    filtered_labels = [types[i] for i in range(len(types)) if values[i] >= total_length * limit]
    filtered_values = [values[i] for i in range(len(types)) if values[i] >= total_length * limit]
    other_length = 0
    for transaction in dataset.transactions:
        car = next(car for car in dataset.cars if car.plate == transaction.car)
        if car.type not in filtered_labels:
            other_length += transaction.length

    filtered_labels.append("other")
    filtered_values.append(other_length)

    explode = [0.2 if label == "other" else 0 for label in filtered_labels]

    fig1, ax1 = plt.subplots()
    ax1.pie(filtered_values, labels=filtered_labels, explode=explode, autopct="%1.1f%%", startangle=90,
            rotatelabels=True, pctdistance=0.7)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax1.tick_params(axis="both", which="major", labelsize=10)

    plt.show()


def genders_by_ages_heatmap(dataset: RentalDataset) -> None:
    genders = ["males", "females"]
    ages = [f"{i * 10}-{(i + 1) * 10 - 1}" for i in range(11)]
    values = np.zeros((len(genders), len(ages)))
    for person in dataset.people:
        values[0 if person.male else 1, person.age // 10] += 1

    fig, ax = plt.subplots()
    im = ax.imshow(values)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(ages)))
    ax.set_yticks(np.arange(len(genders)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(ages)
    ax.set_yticklabels(genders)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(genders)):
        for j in range(len(ages)):
            text = ax.text(j, i, int(values[i, j]), ha="center", va="center", color="w")

    ax.set_title("Heatmap of genders and ages")
    fig.tight_layout()
    plt.show()


def distances_by_countries_and_sexes(dataset: RentalDataset) -> None:
    countries = list({airport.country for airport in dataset.airports})
    values_male = [0 for _ in countries]
    values_female = [0 for _ in countries]

    for transaction in dataset.transactions:
        airport = next(airport for airport in dataset.airports if airport.code == transaction.airport)
        person = next(person for person in dataset.people if person.id == transaction.person)
        country_index = countries.index(airport.country)
        if person.male:
            values_male[country_index] += transaction.length
        else:
            values_female[country_index] += transaction.length

    non_zero_indices = {i for i in range(len(countries)) if values_male[i] + values_female[i] > 0}
    countries = [countries[i] for i in non_zero_indices]
    values_male = [values_male[i] for i in non_zero_indices]
    values_female = [values_female[i] for i in non_zero_indices]

    x = np.arange(len(countries))  # the label locations
    width = 0.3  # the width of the bars

    fig, ax = plt.subplots()
    series_males = ax.bar(x - width / 2, values_male, width, label="Males")
    series_females = ax.bar(x + width / 2, values_female, width, label="Females")

    ax.set_ylabel("Total distance")
    ax.set_title("Countries of airports")
    ax.set_xticks(x)
    ax.set_xticklabels(countries, rotation=90)
    ax.legend()

    # ax.bar_label(series_males, padding=3)
    # ax.bar_label(series_females, padding=3)

    fig.tight_layout()

    plt.show()