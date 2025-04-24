spacyquery
=============================================================

SpacyQuery for CubicWeb

Installation
------------

Open the project in a terminal and run::

    pip install -e .

This will install the cube in your active virtual environment
as ``cubicweb-spacyquery``.

The following sections indicate additional steps when you
install this cube as a dependency or as an instance.

As a dependency
~~~~~~~~~~~~~~~

If you plan to use this cube as a dependency for your own cube,
add it to your ``__pkginfo__.py`` as follows::

    __depends__ = {
        # ... Your previous dependencies
        "cubicweb-spacyquery": None,
    }

If the target cube is already used as an instance, you need to migrate it
with the help of its python shell (replace ``YOUR_INSTANCE_NAME`` by your instance name)::

    cubicweb-ctl shell YOUR_INSTANCE_NAME

In the python prompt, enter the following command::

    add_cube("spacyquery")

Press ``Ctrl-D`` then restart your instance.
The cube should now be available in your instance.

As an instance
~~~~~~~~~~~~~~

If you plan to use this cube directly as an instance, create and start
your instance with the following commands (replace ``spacyquery-instance``
by the name of your choice)::

    cubicweb-ctl create spacyquery spacyquery-instance
    cubicweb-ctl start -D spacyquery-instance


Learn More
----------

Visit the `official documentation <https://cubicweb.readthedocs.io/en/4.5.2>`_
to learn more about CubicWeb.
