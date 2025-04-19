# A lightweight application for consistent handling of kafka events

This application was developed to be a universal api endpoint for microservices that process kafka events.

# Installation

```
pip install kafka-python-app
```

# Usage

## Configure and create application instance.

Configuration parameters:

- **app_name [OPTIONAL]**: application name.
- **bootstrap_servers**: list of kafka bootstrap servers addresses 'host:port'.
- **producer_config [OPTIONAL]**: kafka producer configuration (
  see [kafka-python documentation](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html)).

```python
# Default producer config
producer_config = {
    'key_serializer': lambda x: x.encode('utf-8') if x else x,
    "value_serializer": lambda x: json.dumps(x).encode('utf-8')
}
```

- **consumer_config [OPTIONAL]**: kafka consumer configuration (
  see [kafka-python documentation](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)).

```python
# Default consumer config
conf = {
    'group_id': str(uuid.uuid4()),
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': False,
    'key_deserializer': lambda x: x.decode('utf-8') if x else x,
    'value_deserializer': lambda x: json.loads(x.decode('utf-8')),
    'session_timeout_ms': 25000
}
```

- **listen_topics**: list of subscribed topics.
- **message_key_as_event [OPTIONAL]**: set to True if using kafka message key as event name.

> **_NOTE_** When setting ***message_key_as_event*** to True,
> make sure to specify valid **key_deserializer** in **consumer_config**.

- **message_value_cls [OPTIONAL]**: dictionary {"topic_name": dataclass_type} that maps message dataclass 
type to specific topic.
The application uses this mapping to create specified dataclass from kafka message.value.
- **middleware_message_cb [OPTIONAL]**: if provided, this callback will be executed with raw 
kafka message argument before calling any handler.
- **emit_with_response_options [OPTIONAL]**: configuration that supports use of the
**emit_with_response** method
- **pipelines_map [OPTIONAL]**: Dict[str, MessagePipeline] - provides mapping of a pipelint to 
event name or "topic.event" combination.
- **max_concurrent_tasks [OPTIONAL]**: int - number of individual event handlers executed concurrently
- **max_concurrent_pipelines [OPTIONAL]**: int - number of pipelines executed concurrently
- **logger [OPTIONAL]**: any logger with standard log methods. If not provided, the standard python logger is used.

```python
from kafka_python_app.app import AppConfig, KafkaApp


# Setup kafka message payload:
class MyMessage(pydantic.BaseModel):
    event: str
    prop1: str
    prop2: int


# This message type is specific for "test_topic3" only. 
class MyMessageSpecific(pydantic.BaseModel):
    event: str
    prop3: bool
    prop4: float


# Create application config
config = AppConfig(
    app_name='Test application',
    bootstrap_servers=['localhost:9092'],
    consumer_config={
        'group_id': 'test_app_group'
    },
    listen_topics=['test_topic1', 'test_topic2', 'test_topic3'],
    message_value_cls={
        'test_topic1': MyMessage,
        'test_topic2': MyMessage,
        'test_topic3': MyMessageSpecific
    }
)

# Create application
app = KafkaApp(config)
```

## Create event handlers using **@app.on** decorator:

```python
# This handler will handle 'some_event' no matter which topic it comes from
@app.on(event='some_event')
def handle_some_event(message: MyMessage, **kwargs):
    print('Handling event: {}..'.format(message.event))
    print('prop1: {}\n'.format(message.prop1))
    print('prop2: {}\n'.format(message.prop2))


# This handler will handle 'another_event' from 'test_topic2' only.
# Events with this name but coming from another topic will be ignored.
@app.on(event='another_event', topic='test_topic2')
def handle_some_event(message: MyMessage, **kwargs):
    print('Handling event: {}..'.format(message.event))
    print('prop1: {}\n'.format(message.prop1))
    print('prop2: {}\n'.format(message.prop2))


# This handler will handle 'another_event' from 'test_topic3' only.
@app.on(event='another_event', topic='test_topic3')
def handle_some_event(message: MyMessageSpecific, **kwargs):
    print('Handling event: {}..'.format(message.event))
    print('prop3: {}\n'.format(message.prop3))
    print('prop4: {}\n'.format(message.prop4))
```

> **_NOTE:_** If **topic** argument is provided to **@app.on** decorator,
> the decorated function is mapped to particular topic.event key that means
> an event that comes from a topic other than the specified
> will not be processed. Otherwise, event will be processed
> no matter which topic it comes from.

## Use message pipelines

The **@app.on** decorator is used to register a single handler for a message. 
However, now it is possible to pass a message through a sequence of handlers
by providing a **pipelines_map** option into the application config.
The **pipelines_map** is a dictionary of type **Dict[str, MessagePipeline]**.

**MessagePipeline** class has following properties:
- transactions: List[MessageTransaction]
- logger (optional): any object that has standard logging methods (debug, info, error, etc.)

**MessageTransaction** has properties:
- fnc: Callable - transaction function that takes message, somehow transforms it and returns it to next 
transaction in the pipeline. Every transaction function must have a signature: fnc(message, logger, **kwargs)
and has to return message of the same type.
> **_NOTE:_** Transaction function can be sync or async.
- args: Dict - a dictionary of keyword arguments for transaction function.
- pipe_result_options (optional): TransactionPipeWithReturnOptions - configuration to pipe message to 
another service (kafka app).

**TransactionPipeResultOptions** class properties:
- pipe_event_name: str - event name that will be sent
pipe_to_topic: str - destination topic
with_response_options (optional): TransactionPipeWithReturnOptions - this config is used when pipeline 
needs to wait response from another service before proceeding to next transaction.

**TransactionPipeWithReturnOptions** class properties:
- response_event_name: str - event name of the response
- response_from_topic: str - topic name that the response should come from
- cache_client: Any - client of any caching service that has methods **get** and **set**
> **get** method signature: get(key: str) -> bytes
> 
> **set** method signature: set(name: str, value: bytes, ex: int (record expiration in sec))
- return_event_timeout: int - timeout in seconds for returned event

**TransactionPipeResultOptionsCustom** class properties:

> **_NOTE:_** Use this if you need to implement custom logic after transaction function is executed.

- fnc: Callable - function that will be executed after transaction function is finished.

> Function **fnc** signature: fnc(app_id: str,
                                pipeline_name: str,
                                message: Dict,
                                emitter: [kafka app emit metod],
                                message_key_as_event: bool,
                                fnc_pipe_event,
                                fnc_pipe_event_with_response,
                                logger: [any logger supporting basic logging methods],
                                **kwargs)
> 
> > Function **fnc_pipe_event** signature: fnc(
                                pipeline_name: str,
                                message: Dict,
                                emitter: [kafka app emit metod],
                                message_key_as_event: bool,
                                options: TransactionPipeResultOptions
                                logger: [any logger supporting basic logging methods],
                                **kwargs)
> 
> > Function **fnc_pipe_event_with_response** signature: fnc(app_id: str,
                                pipeline_name: str,
                                message: Dict,
                                emitter: [kafka app emit metod],
                                message_key_as_event: bool,
                                options: TransactionPipeResultOptions
                                logger: [any logger supporting basic logging methods],
                                **kwargs)

- with_response_options: Optional[TransactionPipeWithReturnOptionsMultikey] - these option will be 
used by **kafka app** to register caching pipelines. This is the same as **TransactionPipeWithReturnOptions** 
buth instead of separate options **response_event_name** and **response_from_topic** there is a 
list of tuples **(response_from_topic, response_event_name)** called **response_event_topic_keys**.

#### Example:
Suppose we receive a string with each message and that string needs to be processed.
Let's say we need replace all commas with a custom symbol and then 
add a number to the end of the string that correspond to the number of some
substring occurrences.

```python
from kafka_python_app.app import AppConfig, KafkaApp, MessagePipeline, MessageTransaction


# Define transaction functions
def txn_replace(message: str, symbol: str, logger=None):
  return message.replace(',', symbol)

def txn_add_count(message: str, substr: str, logger=None):
  return ' '.join([message, message.count(substr)])

# Define a pipeline
pipeline = MessagePipeline(
  transactions=[
    MessageTransaction(fnc=txn_replace, args={'symbol': '|'}),
    MessageTransaction(fnc=txn_add_count, args={'substr': 'foo'})
  ]
)

# Define a pipelines map
pipelines_map = {'some_event': pipeline}

# Create application config
config = AppConfig(
    app_name='Test application',
    bootstrap_servers=['localhost:9092'],
    consumer_config={
        'group_id': 'test_app_group'
    },
    listen_topics=['test_topic1'],
    pipelines_map=pipelines_map
)

# Create application
app = KafkaApp(config)
```

> **_NOTE:_** Define pipelines_map keys in a format 'topic.event' in order
> to restrict pipeline execution to events that come from a certain topic.

#### Use **app.emit()** method to send messages to kafka:

```python
from kafka_python_app import ProducerRecord

msg = ProducerRecord(
  key='my_message_key',
  value='my_payload'
)

app.emit(topic='some_topic', message=msg)
```

#### Use **app.emit_with_response()** method to send messages to kafka and wait for response event:
Specify **emit_with_response_options** in the application config.

**EmitWithResponseOptions** class properties:
- topic_event_list: list of tuples (topic_name: str, event_name: str) for returned events. 
This defines what events and from what topics should be cached as "response" events.
- cache_client: Any - client of any caching service that has methods **get** and **set**
> get method signature: get(key: str) -> bytes
> 
> set method signature: set(name: str, value: bytes, ex: int (record expiration in sec))
- return_event_timeout: int - timeout in seconds for returned event

```python
from kafka_python_app import KafkaApp, AppConfig, \
  EmitWithResponseOptions, ProducerRecord, 

# Create application config
config = AppConfig(
    app_name='Test application',
    bootstrap_servers=['localhost:9092'],
    consumer_config={
        'group_id': 'test_app_group'
    },
    listen_topics=['test_topic1'],
    emit_with_response_options=EmitWithReturnOptions(
        event_topic_list=[
            ("test_topic_2", "response_event_name")
        ],
        cache_client=redis_client,
        return_event_timeout=30
    ),
)

# Create application
app = KafkaApp(config)
msg = ProducerRecord(
  value={"event": "test_event_name": "payload": "Hello?"}
)

response = app.emit_with_response(topic='some_topic', message=msg)
```


## Start application:

```python
if __name__ == "__main__":
    asyncio.run(app.run())
```

# Use standalone kafka connector

The **KafkaConnector** class has two factory methods:

- **get_producer** method returns kafka-python producer.
- **get_listener** method returns instance of the **KafkaListener** class that wraps up kafka-python consumer and **
  listen()** method that starts consumption loop.

Use **ListenerConfig** class to create listener configuration:

```python
from kafka_python_app.connector import ListenerConfig

kafka_listener_config = ListenerConfig(
    bootstrap_servers=['ip1:port1', 'ip2:port2', ...],
    process_message_cb=my_process_message_func,
    consumer_config={'group_id': 'test_group'},
    topics=['topic1', 'topic2', ...],
    logger=my_logger
)
```

- **bootstrap_servers**: list of kafka bootstrap servers addresses 'host:port'.
- **process_message_cb**: a function that will be called on each message. 

```python
from kafka.consumer.fetcher import ConsumerRecord

def my_process_message_func(message: ConsumerRecord):
    print('Received kafka message: key: {}, value: {}'.format(
      message.key,
      message.value
    ))
```

> **_NOTE:_** Use async function for **process_message_cb** in order to process messages concurrently.

- **consumer_config [OPTIONAL]**: kafka consumer configuration (
  see [kafka-python documentation](https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html)).
- **topics**: list of topics to listen from.
- **logger [OPTIONAL]**: any logger with standard log methods. If not provided, the standard python logger is used.