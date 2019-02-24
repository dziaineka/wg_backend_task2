import numpy
import psycopg2


COLORS = (
   'black',
   'white',
   'black & white',
   'red',
   'red & white',
   'red & black & white',
)

AVERAGE_KINDS = (
    'mean',
    'median',
    'mode',
)

MEASUREMENTS = (
    'tail',
    'whiskers',
)

db_connection = None
cur = None


def get_values(measurement):
    cur.execute('SELECT ' + measurement + '_length ' +
                'FROM cats')

    lenghts = cur.fetchall()
    values = []

    for lenght in lenghts:
        values.append(lenght[0])

    return values


def calc_mode(values):
    moda = []

    arr = numpy.array(values)
    counts = numpy.bincount(arr)

    moda.append(numpy.argmax(counts))

    for index, number in enumerate(moda):
        moda[index] = int(number)

    return moda


def get_fullname(measurement, kind):
    return measurement + '_length_' + kind


def write_info(statistics):
    field_names = '('
    placeholders = '('
    values = []

    for field in statistics:
        print('{} - {}'.format(field, statistics[field]))

        field_names += field + ', '
        placeholders += '%s, '
        values.append(statistics[field])

    field_names = field_names[:-2] + ')'
    placeholders = placeholders[:-2] + ')'

    try:
        cur.execute('INSERT INTO cats_stat ' + field_names + ' ' +
                    'VALUES ' + placeholders, values)
    except psycopg2.IntegrityError:
        cur.execute("ROLLBACK")


def main():
    statistics = {}

    for measurement in MEASUREMENTS:
        values = get_values(measurement)

        field_name = get_fullname(measurement, AVERAGE_KINDS[0])
        statistics[field_name] = numpy.mean(values)

        field_name = get_fullname(measurement, AVERAGE_KINDS[1])
        statistics[field_name] = numpy.median(values)

        field_name = get_fullname(measurement, AVERAGE_KINDS[2])
        statistics[field_name] = calc_mode(values)

    write_info(statistics)


if __name__ == "__main__":
    db_connection = psycopg2.connect(host="postgreDB",
                                     database="wg_forge_db",
                                     user="wg_forge",
                                     password="42a")

    cur = db_connection.cursor()

    main()

    db_connection.commit()

    cur.close()
    db_connection.close()
