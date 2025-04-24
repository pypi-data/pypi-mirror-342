aioasyncsqlite provides a friendly, async interface to sqlite databases.

It replicates the standard ``sqlite3`` module, but with async versions
of all the standard connection and cursor methods, plus context managers for
automatically closing connections and cursors:

.. code-block:: python

    async with aioasyncsqlite.connect(...) as db:
        await db.execute("INSERT INTO some_table ...")
        await db.commit()

        async with db.execute("SELECT * FROM some_table") as cursor:
            async for row in cursor:
                ...

It can also be used in the traditional, procedural manner:

.. code-block:: python

    db = await aioasyncsqlite.connect(...)
    cursor = await db.execute('SELECT * FROM some_table')
    row = await cursor.fetchone()
    rows = await cursor.fetchall()
    await cursor.close()
    await db.close()

aioasyncsqlite also replicates most of the advanced features of ``sqlite3``:

.. code-block:: python

    async with aioasyncsqlite.connect(...) as db:
        db.row_factory = aioasyncsqlite.Row
        async with db.execute('SELECT * FROM some_table') as cursor:
            async for row in cursor:
                value = row['column']

        await db.execute('INSERT INTO foo some_table')
        assert db.total_changes > 0


Install
-------

aioasyncsqlite is compatible with Python 3.8 and newer.
You can install it from PyPI:

.. code-block:: console

    $ pip install aioasyncsqlite


Details
-------

aioasyncsqlite allows interaction with SQLite databases on the main AsyncIO event
loop without blocking execution of other coroutines while waiting for queries
or data fetches.  It does this by using a single, shared thread per connection.
This thread executes all actions within a shared request queue to prevent
overlapping actions.

Connection objects are proxies to the real connections, contain the shared
execution thread, and provide context managers to handle automatically closing
connections.  Cursors are similarly proxies to the real cursors, and provide
async iterators to query results.
