# Device Input Schema

## Basic Data Type

```c++
autoenable_created_entities        = boolean
autodispose_unregistered_instances = boolean
autopurge_dispose_all              = boolean
coherent_access                    = boolean
ordered_access                     = boolean
id                                 = integer // (0~2,147,483,647)
size                               = integer // data size (0~2,147,483,647)
cycletime                          = integer // data cycletime (0~2,147,483,647)
experiment_time                    = integer // (0~2,147,483,647)
measure_count                      = integer // measure latency time after countdown to zero (0~2,147,483,647)
value                              = integer // (0~2,147,483,647)
sec                                = integer // (0~2,147,483,647)
nanosec                            = integer // (0~999,999,999)
depth                              = integer // (0~2,147,483,647)
max_samples                        = integer // (0~2,147,483,647, -1 means unlimited)
max_instances                      = integer // (0~2,147,483,647, -1 means unlimited)
max_samples_per_instance           = integer // (0~2,147,483,647, -1 means unlimited)
kind                               = integer // (>=0)
name                               = string
dst_topic                          = string
src_topic                          = string
partition                          = string
data                               = string // unsigned char array
duration                           = { sec,
                                       nanosec }
autounregister_instance_delay      = duration
autopurge_disposed_samples_delay   = duration
autopurge_nowriter_samples_delay   = duration
autopurge_suspended_samples_delay  = duration
max_blocking_time                  = duration // max {2147483647, 999999999}
minimum_separation                 = duration
period                             = duration
service_cleanup_delay              = duration 
lease_duration                     = duration 
```

## DDS QoS

```c++
user_data             = { data }
topic_data            = { data }
group_data            = { data }
entity_factory        = { autoenable_created_entities }
transport_priority    = { value }
lifespan              = { duration }
durability            = { kind } // kind： (default, 0)VOLATILE < (1)TRANSIENT_LOCAL < (2)TRANSIENT < (3)PERSISTENT
deadline              = { period }
latency_budget        = { duration }
ownership             = { kind } // kind: (default, 0)SHARED < (1)EXCLUSIVE
ownership_strength    = { value }
liveliness            = { kind, lease_duration } // kind: (default, 0)AUTOMATIC, (1)MANUAL_BY_PARTICIPANT, (2)MANUAL_BY_TOPIC
reliability           = { kind
                          max_blocking_time } // kind: (default, 0)BEST_EFFORT, (1)RELIABLE
destination_order     = { kind } // kind: (default, 0)BY_RECEPTION_TIMESTAMP, (1)BY_SOURCE_TIMESTAMP
history               = { kind,
                          depth } // kind: (default, 0)KEEP_LAST, (1)KEEP_ALL
resource_limits       = { max_samples,
                          max_instances,
                          max_samples_per_instance }
durability_service    = { service_cleanup_delay,
                          kind,
                          depth,
                          max_samples,
                          max_instances,
                          max_samples_per_instance } // kind: (default, 0)KEEP_LAST, (1)KEEP_ALL
presentation          = { kind,
                          coherent_access,
                          ordered_access } // kind: (default, 0)INSTANCE, (1)TOPIC, (2)GROUP
writer_data_lifecycle = { autodispose_unregistered_instances,
                          autopurge_suspended_samples_delay,
                          autounregister_instance_delay }
time_based_filter     = { minimum_separation }
reader_data_lifecycle = { autopurge_nowriter_samples_delay,
                          autopurge_disposed_samples_delay,
                          autopurge_dispose_all,
                          kind } // kind: (0)NO_INVALID_SAMPLES, (default, 1)MINIMUM_INVALID_SAMPLES, (2)ALL_INVALID_SAMPLES
```

## Device Input

```c++
device      = { name,
                experiment_time,
                measure_count,
                domain }
domain      = { domain_qos,
                [topic],
                [partition] }
domain_qos  = { user_data,
                entity_factory }
topic       = { name,
                topic_qos }
topic_qos   = { topic_data,
                transport_priority,
                lifespan,
                durability,
                deadline,
                latency_budget,
                ownership,
                liveliness,
                reliability,
                destination_order,
                history,
                resource_limits,
                durability_service }
partition   = { name,
                [publisher],
                [subscriber] }
publisher   = { id,
                pub_qos,
                [data_writer] }
pub_qos     = { group_data,
                presentation,
                entity_factory }
data_writer = { id,
                dst_topic,
                dw_qos,
                size,
                cycletime }
dw_qos      = { user_data,
                transport_priority,
                lifespan,
                durability,
                deadline,
                latency_budget,
                ownership,
                ownership_strength,
                liveliness,
                reliability,
                destination_order,
                history,
                resource_limits,
                writer_data_lifecycle }
subscriber  = { id,
                sub_qos,
                [data_reader] }
data_reader = { id,
                src_topic,
                dr_qos  }
sub_qos     = { group_data,
                presentation,
                entity_factory }
dr_qos      = { user_data,
                durability,
                deadline,
                latency_budget,
                ownership,
                liveliness,
                time_based_filter,
                reliability,
                destination_order,
                history,
                resource_limits,
                reader_data_lifecycle }
```

## Example

```json
{
  "name": "sample",
  "experiment_time": 5,
  "measure_count": 100,
  "domain": {
    "domain_qos": {
      "user_data": {
        "data": "sample"
      },
      "entity_factory": {
        "autoenable_created_entities": true
      }
    },
    "topic": [
      {
        "name": "topic1",
        "topic_qos": {
          "topic_data": {
            "data": "sample"
          },
          "transport_priority": {
            "value": 0
          },
          "lifespan": {
            "duration": {
              "sec": 2147483647,
              "nanosec": 2147483647
            }
          },
          "durability": {
            "kind": 0
          },
          "deadline": {
            "period": {
              "sec": 2147483647,
              "nanosec": 2147483647
            }
          },
          "latency_budget": {
            "duration": {
              "sec": 0,
              "nanosec": 0
            }
          },
          "ownership": {
            "kind": 0
          },
          "liveliness": {
            "kind": 0,
            "lease_duration": {
              "sec": 2147483647,
              "nanosec": 2147483647
            }
          },
          "reliability": {
            "kind": 0,
            "max_blocking_time": {
              "sec": 0,
              "nanosec": 100000000
            }
          },
          "destination_order": {
            "kind": 0
          },
          "history": {
            "kind": 0,
            "depth": 1
          },
          "resource_limits": {
            "max_samples": -1,
            "max_instances": -1,
            "max_samples_per_instance": -1
          },
          "durability_service": {
            "service_cleanup_delay": {
              "sec": 0,
              "nanosec": 0
            },
            "kind": 0,
            "depth": 1,
            "max_samples": -1,
            "max_instances": -1,
            "max_samples_per_instance": -1
          }
        }
      }
    ],
    "partition": [
      {
        "name": "part1",
        "publisher": [
          {
            "id": 0,
            "pub_qos": {
              "group_data": {
                "data": "sample"
              },
              "presentation": {
                "kind": 0,
                "coherent_access": false,
                "ordered_access": false
              },
              "entity_factory": {
                "autoenable_created_entities": true
              }
            },
            "data_writer": [
              {
                "id": 0,
                "dst_topic": "topic1",
                "dw_qos": {
                  "user_data": {
                    "data": "sample"
                  },
                  "transport_priority": {
                    "value": 0
                  },
                  "lifespan": {
                    "duration": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    }
                  },
                  "durability": {
                    "kind": 0
                  },
                  "deadline": {
                    "period": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    }
                  },
                  "latency_budget": {
                    "duration": {
                      "sec": 0,
                      "nanosec": 0
                    }
                  },
                  "ownership": {
                    "kind": 0
                  },
                  "ownership_strength": {
                    "value": 0
                  },
                  "liveliness": {
                    "kind": 0,
                    "lease_duration": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    }
                  },
                  "reliability": {
                    "kind": 0,
                    "max_blocking_time": {
                      "sec": 0,
                      "nanosec": 100000000
                    }
                  },
                  "destination_order": {
                    "kind": 0
                  },
                  "history": {
                    "kind": 0,
                    "depth": 1
                  },
                  "resource_limits": {
                    "max_samples": -1,
                    "max_instances": -1,
                    "max_samples_per_instance": -1
                  },
                  "writer_data_lifecycle": {
                    "autodispose_unregistered_instances": true,
                    "autopurge_suspended_samples_delay": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    },
                    "autounregister_instance_delay": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    }
                  }
                },
                "size": 1024,
                "cycletime": 1
              }
            ]
          }
        ],
        "subscriber": [
          {
            "id": 0,
            "sub_qos": {
              "group_data": {
                "data": "sample"
              },
              "presentation": {
                "kind": 0,
                "coherent_access": false,
                "ordered_access": false
              },
              "entity_factory": {
                "autoenable_created_entities": true
              }
            },
            "data_reader": [
              {
                "id": 0,
                "src_topic": "topic1",
                "dr_qos": {
                  "user_data": {
                    "data": "sample"
                  },
                  "durability": {
                    "kind": 0
                  },
                  "deadline": {
                    "period": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    }
                  },
                  "latency_budget": {
                    "duration": {
                      "sec": 0,
                      "nanosec": 0
                    }
                  },
                  "ownership": {
                    "kind": 0
                  },
                  "liveliness": {
                    "kind": 0,
                    "lease_duration": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    }
                  },
                  "time_based_filter": {
                    "minimum_separation": {
                      "sec": 0,
                      "nanosec": 0
                    }
                  },
                  "reliability": {
                    "kind": 0,
                    "max_blocking_time": {
                      "sec": 0,
                      "nanosec": 100000000
                    }
                  },
                  "destination_order": {
                    "kind": 0
                  },
                  "history": {
                    "kind": 0,
                    "depth": 1
                  },
                  "resource_limits": {
                    "max_samples": -1,
                    "max_instances": -1,
                    "max_samples_per_instance": -1
                  },
                  "reader_data_lifecycle": {
                    "autopurge_nowriter_samples_delay": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    },
                    "autopurge_disposed_samples_delay": {
                      "sec": 2147483647,
                      "nanosec": 2147483647
                    },
                    "autopurge_dispose_all": false,
                    "kind": 1
                  }
                }
              }
            ]
          }
        ]
      }
    ]
  }
}
```
