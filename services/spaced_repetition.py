from datetime import datetime, timedelta


INTERVALS = [1, 3, 7, 15, 30, 60]


def next_review(correct_count):

    if correct_count < len(INTERVALS):

        return (
                datetime.now()
                + timedelta(
                    days=INTERVALS[correct_count]
                )
        )

    return (
            datetime.now()
            + timedelta(days=90)
    )