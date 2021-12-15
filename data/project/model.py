from __future__ import annotations
from dataclasses import field, dataclass
import random
from typing import Type, cast

from faker import Faker
from faker_music import MusicProvider
from data.project.base import Dataset, Entity

# import faker.providers.credit_card
fake = Faker()


# TODO replace this module with your own types

@dataclass
class RentalDataset(Dataset):
    people: list[Person]
    creditcards: list[CreditCard]
    songs: list[Music]
    transactions: list[Transaction]

    @staticmethod
    def entity_types() -> list[Type[Entity]]:
        return [Person, CreditCard, Music, Transaction]

    @staticmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        return RentalDataset(
            cast(list[Person], entities[0]),
            cast(list[CreditCard], entities[1]),
            cast(list[Music], entities[2]),
            cast(list[Transaction], entities[3])
        )

    def entities(self) -> dict[Type[Entity], list[Entity]]:
        res = dict()
        res[Person] = self.people
        res[CreditCard] = self.creditcards
        res[Music] = self.songs
        res[Transaction] = self.transactions

        return res

    @staticmethod
    def generate(
            count_of_customers: int,
            count_of_creditcards: int,
            count_of_songs: int,
            count_of_transactions: int):

        def generate_people(n: int, male_ratio: float = 0.5, locale: str = "en_US",
                            unique: bool = False, min_age: int = 15, max_age: int = 100) -> list[Person]:
            assert n > 0
            assert 0 <= male_ratio <= 1
            assert 0 <= min_age <= max_age

            fake = Faker(locale)
            people = []
            for i in range(n):
                male = random.random() < male_ratio
                generator = fake if not unique else fake.unique
                people.append(Person(
                    "P-" + (str(i).zfill(6)),
                    generator.name_male() if male else generator.name_female(),
                    random.randint(min_age, max_age),
                    male))

            return people

        def generate_songs(n: int) -> list[Music]:
            assert n > 0

            fake = Faker()
            fake.add_provider(MusicProvider)

            musics = []
            for i in range(n):
                x = Music(fake.music_genre(),
                          fake.music_subgenre(),
                          fake.music_instrument(),
                          fake.music_instrument_category()
                          )
                musics.append(x)
            return musics

        def generate_creditcards(n: int) -> list[CreditCard]:
            assert n > 0

            cards = []
            for i in range(n):
                try:
                    card = CreditCard(
                        fake.credit_card_number(),
                        fake.credit_card_provider(),
                        fake.credit_card_expire(),
                        fake.credit_card_security_code()
                    )
                    cards.append(card)
                except:
                    break
            return cards

        def generate_transactions(n: int, people: list[Person], creditcards: list[CreditCard], songs: list[Music]) -> \
        list[
            Transaction]:
            assert n > 0
            assert len(people) > 0
            assert len(creditcards) > 0
            assert len(songs) > 0

            trips = []
            for i in range(n):
                person = random.choice(people)
                card = random.choice(creditcards)
                music = random.choice(songs)
                trips.append(
                    Transaction(f'T-{str(i).zfill(6)}', person.id, card.credit_card_number, music.music_genre,
                                random.randint(100, 1000)))
            return trips

        people = generate_people(count_of_customers)
        creditcards = generate_creditcards(count_of_creditcards)
        songs = generate_songs(count_of_songs)
        transactions = generate_transactions(count_of_transactions, people, creditcards, songs)
        return RentalDataset(people, creditcards, songs, transactions)


@dataclass
class Transaction(Entity):
    id: str = field(hash=True)
    music: str = field(repr=True, compare=False)
    person: str = field(repr=True, compare=False)
    card: str = field(repr=True, compare=False)
    length: int = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Transaction:
        return Transaction(seq[0], seq[1], seq[2], seq[3], int(seq[4]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.music, self.person, self.card, str(self.length)]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "music", "person", "card", "length"]

    @staticmethod
    def collection_name() -> str:
        return "transactions"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Transaction.collection_name()} (
            id VARCHAR(30) NOT NULL PRIMARY KEY,
            music CHAR(30) NOT NULL,
            person VARCHAR(30) NOT NULL,
            card VARCHAR(50) NOT NULL,
            length SMALLINT,

            FOREIGN KEY (music) REFERENCES {Music.collection_name()}(music_genre),
            FOREIGN KEY (person) REFERENCES {Person.collection_name()}(id),
            FOREIGN KEY (card) REFERENCES {CreditCard.collection_name()}(credit_card_number)
        );
        """


@dataclass
class Music(Entity):
    music_genre: str = field(hash=True)
    music_subgenre: str = field(repr=True, compare=False)
    music_instrument: str = field(repr=True, compare=False)
    music_instrument_category: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Music:
        return Music(seq[0], seq[1], seq[2], seq[3])

    def to_sequence(self) -> list[str]:
        return [self.music_genre, self.music_subgenre, self.music_instrument, self.music_instrument_category]

    @staticmethod
    def field_names() -> list[str]:
        return ["music_genre", "music_subgenre", "music_instrument", "music_instrument_category"]

    @staticmethod
    def collection_name() -> str:
        return "songs"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Music.collection_name()} (
            music_genre CHAR(30) NOT NULL PRIMARY KEY,
            music_subgenre VARCHAR(100),
            music_instrument VARCHAR(50),
            music_instrument_category VARCHAR(50),

        );
        """


@dataclass
class CreditCard(Entity):
    credit_card_number: str = field(hash=True)
    credit_card_provider: str = field(repr=True, compare=False)
    credit_card_expire: str = field(repr=True, compare=False)
    credit_card_security_code: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> CreditCard:
        return CreditCard(seq[0], seq[1], str(seq[2]), str(seq[3]))

    def to_sequence(self) -> list[str]:
        return [self.credit_card_number, self.credit_card_provider, self.credit_card_expire,
                self.credit_card_security_code]

    @staticmethod
    def field_names() -> list[str]:
        return ["credit_card_number", "credit_card_provider", "credit_card_expire", "credit_card_security_code"]

    @staticmethod
    def collection_name() -> str:
        return "creditcards"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {CreditCard.collection_name()} (
            credit_card_number VARCHAR(30) NOT NULL PRIMARY KEY,
            credit_card_provider VARCHAR(30),
            credit_card_expire VARCHAR(30),
            credit_card_security_code VARCHAR(30)

        );
        """


@dataclass
class Person(Entity):
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Person:
        return Person(seq[0], seq[1], int(seq[2]), bool(seq[3]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.name, str(self.age), str(int(self.male))]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "name", "age", "male"]

    @staticmethod
    def collection_name() -> str:
        return "people"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Person.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            name VARCHAR(50),
            age TINYINT,
            male BOOLEAN
        );
        """