.. image:: https://readthedocs.org/projects/aiolitesql/badge/?version=latest
   :target: https://aiolitesql.omnilib.dev/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://img.shields.io/pypi/v/aiolitesql.svg
   :target: https://pypi.org/project/aiolitesql
   :alt: PyPI Release
.. image:: https://img.shields.io/badge/change-log-blue
   :target: https://github.com/omnilib/aiolitesql/blob/master/CHANGELOG.md
   :alt: Changelog
.. image:: https://img.shields.io/pypi/l/aiolitesql.svg
   :target: https://github.com/omnilib/aiolitesql/blob/master/LICENSE
   :alt: MIT Licensed

aiolitesql provides a friendly, async interface to sqlite databases.

It replicates the standard ``sqlite3`` module, but with async versions
of all the standard connection and cursor methods, plus context managers for
automatically closing connections and cursors:

.. code-block:: python

    async with aiolitesql.connect(...) as db:
        await db.execute("INSERT INTO some_table ...")
        await db.commit()

        async with db.execute("SELECT * FROM some_table") as cursor:
            async for row in cursor:
                ...

It can also be used in the traditional, procedural manner:

.. code-block:: python

    db = await aiolitesql.connect(...)
    cursor = await db.execute('SELECT * FROM some_table')
    row = await cursor.fetchone()
    rows = await cursor.fetchall()
    await cursor.close()
    await db.close()

aiolitesql also replicates most of the advanced features of ``sqlite3``:

.. code-block:: python

    async with aiolitesql.connect(...) as db:
        db.row_factory = aiolitesql.Row
        async with db.execute('SELECT * FROM some_table') as cursor:
            async for row in cursor:
                value = row['column']

        await db.execute('INSERT INTO foo some_table')
        assert db.total_changes > 0


Install
-------

aiolitesql is compatible with Python 3.8 and newer.
You can install it from PyPI:

.. code-block:: console

    $ pip install aiolitesql


Details
-------

aiolitesql allows interaction with SQLite databases on the main AsyncIO event
loop without blocking execution of other coroutines while waiting for queries
or data fetches.  It does this by using a single, shared thread per connection.
This thread executes all actions within a shared request queue to prevent
overlapping actions.

Connection objects are proxies to the real connections, contain the shared
execution thread, and provide context managers to handle automatically closing
connections.  Cursors are similarly proxies to the real cursors, and provide
async iterators to query results.


License
-------

aiolitesql is copyright `Amethyst Reese <https://noswap.com>`_, and licensed under the
MIT license.  I am providing code in this repository to you under an open source
license.  This is my personal repository; the license you receive to my code
is from me and not from my employer. See the `LICENSE`_ file for details.

.. _LICENSE: https://github.com/omnilib/aiolitesql/blob/master/LICENSE
