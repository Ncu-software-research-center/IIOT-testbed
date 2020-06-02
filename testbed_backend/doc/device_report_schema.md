# Device Report Schema

## Device Report File Name

<device_name>.json

## Basic Data Type

```c++
id            = integer
msg_id        = integer
pub_id        = integer
sub_id        = integer
pub_msg_count = integer
sub_msg_count = integer
bytes         = integer
sec           = double
percentage    = double
name          = string
partition     = string
dst_device    = string
dst_topic     = string
src_device    = string
src_topic     = string

```

## Device Report

```c++
report       = { name, data_writers, data_readers, resource }
data_writers = { [data_writer] }
data_writer  = { id, pub_id, partition, dst_device, dst_topic, pub_msg_count, latency}
latency      = { [sec] }
data_readers = { [data_reader] }
data_reader  = { id, sub_id, partition, src_device, src_topic, sub_msg_count, sub_msg_id }
sub_msg_id   = { [msg_id] }
resource     = { cpu, memory, rx, tx }
cpu          = { [percentage] }
memory       = { [percentage] }
rx           = { [bytes] }
tx           = { [bytes] }
```

## Example

```json
{
    "name": "sample",
    "data_writers": [
        {
            "id": 1,
            "pub_id": 1,
            "partition": "part1",
            "dst_device": "sample",
            "dst_topic": "topic1",
            "pub_msg_count": 5,
            "latency": [
                0.000000001,
                0.000000002
            ]
        }
    ],
    "data_readers": [
        {
            "id": 1,
            "sub_id": 1,
            "partition": "part1",
            "src_device": "sample",
            "src_topic": "topic1",
            "sub_msg_count": 5,
            "sub_msg_id": [
                0,
                1,
                2,
                3,
                4,
            ]
        }
    ],
    "resource": {
        "cpu": [
            15.6,
            20.5
        ],
        "memory": [
            30.6,
            28.3
        ],
        "rx": [
            312,
            523
        ],
        "tx": [
            345,
            543
        ]
    }
}
```
