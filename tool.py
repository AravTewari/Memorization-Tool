from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Flashcard(Base):
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)

    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


def add_flashcards():
    while True:
        reply = input('1. Add a new flashcard\n2. Exit\n')

        if reply == '1':
            question = get_proper_input('Question:\n')
            answer = get_proper_input('Answer:\n')

            new_flashcard = Flashcard(question=question, answer=answer, box=1)
            session.add(new_flashcard)

        elif reply == '2':
            session.commit()
            break

        else:
            print(f'{reply} is not an option')


def edit_flashcard(card):
    while True:
        reply = input('press "d" to delete the flashcard:\n'
                      'press "e" to edit the flashcard:\n')
        if reply == 'd' or 'e':
            break
        else:
            print(f'{reply} is not an option')

    if reply == 'e':
        print(f'current question: {card.question}')
        card.question = get_proper_input('please write a new question:\n')

        print(f'current answer: {card.answer}')
        card.answer = get_proper_input('please write a new answer:\n')

        session.commit()

    elif reply == 'd':
        session.delete(card)
        session.commit()


def check_answer(card):
    while True:
        reply = input('press "y" if your answer is correct:\npress "n" if your answer is wrong:\n')
        if reply == 'y' or 'n':
            break
        else:
            print(f'{reply} is not an option')

    if reply == 'y':
        card.box += 1
        if card.box == 3:
            session.delete(card)
        session.commit()

    elif reply == 'n':
        card.box -= 1
        if card.box < 1:
            card.box = 1
        session.commit()


def get_proper_input(prompt):
    reply = ''

    while not reply.strip():
        reply = input(prompt)

    return reply


def practice_flashcards():
    flashcards = session.query(Flashcard).all()

    if not flashcards:
        print('There is no flashcard to practice!')
        return

    for card in flashcards:
        reply = input(f'Question: {card.question}\n'
                      'press "y" to see the answer:\n'
                      'press "n" to skip:\n'
                      'press "u" to update:\n')

        if reply == 'y':
            print(f'Answer: {card.answer}')
            check_answer(card)

        elif reply == 'u':
            edit_flashcard(card)

        elif reply != 'n':
            print(f'{reply} is not an option')


def main():
    while True:
        reply = input('1. Add flashcards\n2. Practice flashcards\n3. Exit\n')

        if reply == '1':
            add_flashcards()

        elif reply == '2':
            practice_flashcards()

        elif reply == '3':
            print('Bye!')
            break

        else:
            print(f'{reply} is not an option')


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
main()
