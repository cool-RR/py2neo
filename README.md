# Py2neo 2.0.beta

Py2neo is a comprehensive toolkit for working with Neo4j from within Python applications or from the command line. The library has no external dependencies and has been carefully designed to be easy and intuitive to use.


## Requirements

- Python 2.7, 3.3 or 3.4
- Neo4j 1.8, 1.9, 2.0 or 2.1 (latest point release of each version is recommended)


## Installation

To install from GitHub, run:

```bash
$ git clone git@github.com:nigelsmall/py2neo.git
$ cd py2neo
$ git checkout beta/2.0
$ pip install .
```


## Getting Connected

The simplest way to try out a connection to the Neo4j server is via a Python console. Within a new session, enter the following:

```python
>>> from py2neo import Graph
>>> graph = Graph()
```

This code imports the `Graph` class from py2neo and creates a new instance for the default server URI. Unless altered by the server configuration, this URI will be <http://localhost:7474/db/data/>.

To connect to a server at an alternative address, simply pass in the URI value as a string argument to the `Graph` constructor:

```python
>>> remote_graph = Graph("http://remotehost.com:6789/db/data/")
```

**Note: Remember to include a trailing slash at the end of a graph database URI or py2neo will not be able to operate correctly.**

For a database behind a secure proxy, a user name and password can also be supplied to the constructor URI. These credentials will then be applied to any subsequent HTTP requests made to the host and port combination specified.

```python
>>> secure_graph = Graph("https://arthur:excalibur@camelot:1150/db/data/")
```

The Graph object provides a basis for most of the interaction with a Neo4j server and to that end, the database URI is generally the only one that needs to be provided explicitly.


## Nodes & Relationships

Nodes and relationships are the fundamental data containers in Neo4j and both have a corresponding class in py2neo. Assuming we've already established a connection to the server (as above) let's build a simple graph with two nodes and one relationship:


```python
>>> from py2neo import Node, Relationship
>>> alice = Node("Person", name="Alice")
>>> bob = Node("Person", name="Bob")
>>> alice_knows_bob = Relationship(alice, "KNOWS", bob)
>>> graph.create(alice_knows_bob)
```

When first created, `Node` and `Relationship` objects exist only in the client; nothing has been written to the server. The `Graph.create` method shown above creates corresponding server objects and automatically binds each local object to its remote counterpart. Within py2neo, binding is the process of applying a URI to a client object, which allows future synchonisation operations to occur. 

**Note: Entity binding can be managed directly by using the `bind` and `unbind` methods and observed through the `bound` boolean property.**


## Pushing & Pulling

Client-server communication over REST can be chatty if not carried out in a considered way. Whenever possible, py2neo attempts to minimise the amount of chatter between the client and the server by batching and lazily retrieving data. Most read and write operations are explicit, allowing the Python application developer a high degree of control over network traffic.

**Note: Previous versions of py2neo have synchronised data between client and server automatically, such as when setting a single property value. Py2neo 2.0 will not carry out updates to client or server objects until this is explicitly requested.**

To illustrate synchronisation, let's give Alice and Bob an age property each. Longhand, this is done as follows:

```python
>>> alice.properties["age"] = 33
>>> bob.properties["age"] = 44
>>> alice.push()
>>> bob.push()
```

Here, we add a new property to each of the two nodes and `push` each in turn, resulting in two separate HTTP calls being made. These calls can be seen more clearly with the debugging function, `watch`:

```python
>>> from py2neo import watch
>>> watch("httpstream")
>>> alice.push()
> POST http://localhost:7474/db/data/batch [146]
< 200 OK [119]
>>> bob.push()
> POST http://localhost:7474/db/data/batch [146]
< 200 OK [119]
```

**Note: The watch function comes with the embedded httpstream library and simply dumps log entries to standard output.**

To squash these two separate `push` operations into one, use the `Graph.push` method instead:

```python
>>> graph.push(alice, bob)
> POST http://localhost:7474/db/data/batch [289]
< 200 OK [237]
```

This not only reduces the activity down to a single HTTP call but wraps both updates in a single atomic transaction.

Pulling updates from server to client is similar: either call the `pull` method on an individual entity or batch together several updates by using `Graph.pull`.

