<template>
  <div>
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex align-items-center justify-content-between">
        <h6 class="m-0 py-2 font-weight-bold text-primary">QoS Optimization</h6>
      </div>
      <div class="card-body mx-2" valign="top">
        <div class="alert alert-danger" role="alert">
          <b>
            Warning:
            DDS won't guarantee that all selected links will give 0% loss rate. But all the selected links will get the loss rate reduced.
          </b>
        </div>
        <h5>QoS Suggestion:</h5>
        <codemirror v-model="qosOptimizationResult" :options="cmOptions"></codemirror>
      </div>
    </div>

    <!-- <EmulationDsalVisualization :dsal="dsal" :data-setting="dataSetting" /> -->

    <!-- Report Table-->
    <ReportDetail :report="report" />
  </div>
</template>

<script>
// require component
import { codemirror } from "vue-codemirror";

// require styles
import "codemirror/lib/codemirror.css";

// language js
import "codemirror/mode/javascript/javascript.js";
import "codemirror/mode/yaml/yaml.js";

import EmulationDsalVisualization from "@/components/TestbedPage/EmulationPage/EmulationDsalVisualization.vue";
import ReportDetail from "@/components/TestbedPage/ReportPage/ReportDetail";

export default {
  components: {
    codemirror,
    EmulationDsalVisualization,
    ReportDetail
  },
  data() {
    return {
      qosOptimizationResult:
        "History QoS:\n\tkind: keep_all\nResource Limit QoS:\n\tmax_sample: 1\n\tmax_instances: -1\n\tmax_samples_per_instances: 1\nReliability:\n\tkind: reliable\n\tmax_blocking_time: 5 sec",
      cmOptions: {
        // codemirror options
        tabSize: 2,
        mode: "yaml",
        lineNumbers: true,
        line: true,
        readOnly: "nocursor"
      },
      dsal: {
        dsalFilename: "1v1",
        dsalContent:
          "# This is a sample configuration for DSAL.\n# Check our guides at ...\n# Only use spaces to indent your .yml configuration.\n# -----\ndsal:\n  version: 1.0.0\n  define_qos:\n    - name: qos1\n      qos:\n        reliability:\n          kind: best_effort\n          max_blocking_time:\n            sec: 10\n            nanosec: 100\n  define_topic:\n    - name: topic1\n      qos: qos1\n  define_data_writer:\n    - name: dw_1\n      qos: qos1\n      dst_topic: topic1\n  define_data_reader:\n    - name: dr_1\n      qos: qos1\n      src_topic: topic1\n  profile_name: profile1\n  devices:\n    - name: device1\n      domains:\n        - qos: qos1\n          partitions:\n            - name: part1\n              publishers:\n                - qos: qos1\n                  data_writers:\n                    - name: dw_1\n              subscribers:\n                - qos: qos1\n                  data_readers:\n                    - name: dr_1",
        dsalUpdated: "2020-02-17T04:07:01.485670Z",
        dsalHash:
          "dea6ffb8a83557980f76e6b2ddc2803dd20e34b3de8f93e2ad248f5ffe8fce39"
      },
      dataSetting: {
        device: [
          {
            name: "device1",
            domain: [
              {
                id: 0,
                domainQos: {
                  reliability: {
                    kind: "best_effort",
                    maxBlockingTime: { sec: 10, nanosec: 100 }
                  },
                  userData: { value: "" },
                  topicData: { value: "" },
                  groupData: { value: "" },
                  transportPriority: { value: 0 },
                  lifespan: {
                    duration: { sec: 2147483647, nanosec: 2147483647 }
                  },
                  presentation: {
                    kind: "instance",
                    coherentAccess: false,
                    orderedAccess: false
                  },
                  ownershipStrength: { value: 0 },
                  timeBasedFilter: {
                    minimumSeparation: { sec: 0, nanosec: 0 }
                  },
                  entityFactory: { autoenableCreatedEntities: true },
                  writerDataLifecycle: {
                    autodisposeUnregisteredInstances: true,
                    autopurgeSuspendedSamplesDelay: {
                      sec: 2147483647,
                      nanosec: 2147483647
                    },
                    autounregisterInstanceDelay: {
                      sec: 2147483647,
                      nanosec: 2147483647
                    }
                  },
                  readerDataLifecycle: {
                    kind: "minimum_invalid_samples",
                    autopurgeDisposeAll: false,
                    autopurgeNowriterSamplesDelay: {
                      sec: 2147483647,
                      nanosec: 2147483647
                    },
                    autopurgeDisposedSamplesDelay: {
                      sec: 2147483647,
                      nanosec: 2147483647
                    }
                  },
                  durabilityService: {
                    kind: "keep_last",
                    depth: 1,
                    maxSamples: -1,
                    maxInstances: -1,
                    maxSamplesPerInstance: -1,
                    serviceCleanupDelay: { sec: 0, nanosec: 0 }
                  },
                  deadline: {
                    period: { sec: 2147483647, nanosec: 2147483647 }
                  },
                  destinationOrder: { kind: "by_reception_timestamp" },
                  durability: { kind: "volatile" },
                  history: { kind: "keep_last", depth: 1 },
                  latencyBudget: { duration: { sec: 0, nanosec: 0 } },
                  liveliness: {
                    kind: "automatic",
                    leaseDuration: { sec: 2147483647, nanosec: 2147483647 }
                  },
                  ownership: { kind: "shared" },
                  resourceLimits: {
                    maxSamples: -1,
                    maxInstances: -1,
                    maxSamplesPerInstance: -1
                  }
                },
                partition: [
                  {
                    name: "part1",
                    publisher: [
                      {
                        id: 1,
                        pubQos: {
                          reliability: {
                            kind: "best_effort",
                            maxBlockingTime: { sec: 10, nanosec: 100 }
                          },
                          userData: { value: "" },
                          topicData: { value: "" },
                          groupData: { value: "" },
                          transportPriority: { value: 0 },
                          lifespan: {
                            duration: { sec: 2147483647, nanosec: 2147483647 }
                          },
                          presentation: {
                            kind: "instance",
                            coherentAccess: false,
                            orderedAccess: false
                          },
                          ownershipStrength: { value: 0 },
                          timeBasedFilter: {
                            minimumSeparation: { sec: 0, nanosec: 0 }
                          },
                          entityFactory: { autoenableCreatedEntities: true },
                          writerDataLifecycle: {
                            autodisposeUnregisteredInstances: true,
                            autopurgeSuspendedSamplesDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            },
                            autounregisterInstanceDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            }
                          },
                          readerDataLifecycle: {
                            kind: "minimum_invalid_samples",
                            autopurgeDisposeAll: false,
                            autopurgeNowriterSamplesDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            },
                            autopurgeDisposedSamplesDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            }
                          },
                          durabilityService: {
                            kind: "keep_last",
                            depth: 1,
                            maxSamples: -1,
                            maxInstances: -1,
                            maxSamplesPerInstance: -1,
                            serviceCleanupDelay: { sec: 0, nanosec: 0 }
                          },
                          deadline: {
                            period: { sec: 2147483647, nanosec: 2147483647 }
                          },
                          destinationOrder: { kind: "by_reception_timestamp" },
                          durability: { kind: "volatile" },
                          history: { kind: "keep_last", depth: 1 },
                          latencyBudget: { duration: { sec: 0, nanosec: 0 } },
                          liveliness: {
                            kind: "automatic",
                            leaseDuration: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            }
                          },
                          ownership: { kind: "shared" },
                          resourceLimits: {
                            maxSamples: -1,
                            maxInstances: -1,
                            maxSamplesPerInstance: -1
                          }
                        },
                        dataWriter: [
                          {
                            dstTopic: "topic1",
                            id: 0,
                            dwQos: {
                              reliability: {
                                kind: "best_effort",
                                maxBlockingTime: { sec: 10, nanosec: 100 }
                              },
                              userData: { value: "" },
                              topicData: { value: "" },
                              groupData: { value: "" },
                              transportPriority: { value: 0 },
                              lifespan: {
                                duration: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              presentation: {
                                kind: "instance",
                                coherentAccess: false,
                                orderedAccess: false
                              },
                              ownershipStrength: { value: 0 },
                              timeBasedFilter: {
                                minimumSeparation: { sec: 0, nanosec: 0 }
                              },
                              entityFactory: {
                                autoenableCreatedEntities: true
                              },
                              writerDataLifecycle: {
                                autodisposeUnregisteredInstances: true,
                                autopurgeSuspendedSamplesDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                },
                                autounregisterInstanceDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              readerDataLifecycle: {
                                kind: "minimum_invalid_samples",
                                autopurgeDisposeAll: false,
                                autopurgeNowriterSamplesDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                },
                                autopurgeDisposedSamplesDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              durabilityService: {
                                kind: "keep_last",
                                depth: 1,
                                maxSamples: -1,
                                maxInstances: -1,
                                maxSamplesPerInstance: -1,
                                serviceCleanupDelay: { sec: 0, nanosec: 0 }
                              },
                              deadline: {
                                period: { sec: 2147483647, nanosec: 2147483647 }
                              },
                              destinationOrder: {
                                kind: "by_reception_timestamp"
                              },
                              durability: { kind: "volatile" },
                              history: { kind: "keep_last", depth: 1 },
                              latencyBudget: {
                                duration: { sec: 0, nanosec: 0 }
                              },
                              liveliness: {
                                kind: "automatic",
                                leaseDuration: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              ownership: { kind: "shared" },
                              resourceLimits: {
                                maxSamples: -1,
                                maxInstances: -1,
                                maxSamplesPerInstance: -1
                              }
                            },
                            size: 1,
                            cycletime: 1
                          }
                        ]
                      }
                    ],
                    subscriber: [
                      {
                        id: 1,
                        subQos: {
                          reliability: {
                            kind: "best_effort",
                            maxBlockingTime: { sec: 10, nanosec: 100 }
                          },
                          userData: { value: "" },
                          topicData: { value: "" },
                          groupData: { value: "" },
                          transportPriority: { value: 0 },
                          lifespan: {
                            duration: { sec: 2147483647, nanosec: 2147483647 }
                          },
                          presentation: {
                            kind: "instance",
                            coherentAccess: false,
                            orderedAccess: false
                          },
                          ownershipStrength: { value: 0 },
                          timeBasedFilter: {
                            minimumSeparation: { sec: 0, nanosec: 0 }
                          },
                          entityFactory: { autoenableCreatedEntities: true },
                          writerDataLifecycle: {
                            autodisposeUnregisteredInstances: true,
                            autopurgeSuspendedSamplesDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            },
                            autounregisterInstanceDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            }
                          },
                          readerDataLifecycle: {
                            kind: "minimum_invalid_samples",
                            autopurgeDisposeAll: false,
                            autopurgeNowriterSamplesDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            },
                            autopurgeDisposedSamplesDelay: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            }
                          },
                          durabilityService: {
                            kind: "keep_last",
                            depth: 1,
                            maxSamples: -1,
                            maxInstances: -1,
                            maxSamplesPerInstance: -1,
                            serviceCleanupDelay: { sec: 0, nanosec: 0 }
                          },
                          deadline: {
                            period: { sec: 2147483647, nanosec: 2147483647 }
                          },
                          destinationOrder: { kind: "by_reception_timestamp" },
                          durability: { kind: "volatile" },
                          history: { kind: "keep_last", depth: 1 },
                          latencyBudget: { duration: { sec: 0, nanosec: 0 } },
                          liveliness: {
                            kind: "automatic",
                            leaseDuration: {
                              sec: 2147483647,
                              nanosec: 2147483647
                            }
                          },
                          ownership: { kind: "shared" },
                          resourceLimits: {
                            maxSamples: -1,
                            maxInstances: -1,
                            maxSamplesPerInstance: -1
                          }
                        },
                        dataReader: [
                          {
                            srcTopic: "topic1",
                            id: 0,
                            drQos: {
                              reliability: {
                                kind: "best_effort",
                                maxBlockingTime: { sec: 10, nanosec: 100 }
                              },
                              userData: { value: "" },
                              topicData: { value: "" },
                              groupData: { value: "" },
                              transportPriority: { value: 0 },
                              lifespan: {
                                duration: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              presentation: {
                                kind: "instance",
                                coherentAccess: false,
                                orderedAccess: false
                              },
                              ownershipStrength: { value: 0 },
                              timeBasedFilter: {
                                minimumSeparation: { sec: 0, nanosec: 0 }
                              },
                              entityFactory: {
                                autoenableCreatedEntities: true
                              },
                              writerDataLifecycle: {
                                autodisposeUnregisteredInstances: true,
                                autopurgeSuspendedSamplesDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                },
                                autounregisterInstanceDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              readerDataLifecycle: {
                                kind: "minimum_invalid_samples",
                                autopurgeDisposeAll: false,
                                autopurgeNowriterSamplesDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                },
                                autopurgeDisposedSamplesDelay: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              durabilityService: {
                                kind: "keep_last",
                                depth: 1,
                                maxSamples: -1,
                                maxInstances: -1,
                                maxSamplesPerInstance: -1,
                                serviceCleanupDelay: { sec: 0, nanosec: 0 }
                              },
                              deadline: {
                                period: { sec: 2147483647, nanosec: 2147483647 }
                              },
                              destinationOrder: {
                                kind: "by_reception_timestamp"
                              },
                              durability: { kind: "volatile" },
                              history: { kind: "keep_last", depth: 1 },
                              latencyBudget: {
                                duration: { sec: 0, nanosec: 0 }
                              },
                              liveliness: {
                                kind: "automatic",
                                leaseDuration: {
                                  sec: 2147483647,
                                  nanosec: 2147483647
                                }
                              },
                              ownership: { kind: "shared" },
                              resourceLimits: {
                                maxSamples: -1,
                                maxInstances: -1,
                                maxSamplesPerInstance: -1
                              }
                            }
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ],
        topic: [
          {
            name: "topic1",
            topicQos: {
              reliability: {
                kind: "best_effort",
                maxBlockingTime: { sec: 10, nanosec: 100 }
              },
              userData: { value: "" },
              topicData: { value: "" },
              groupData: { value: "" },
              transportPriority: { value: 0 },
              lifespan: { duration: { sec: 2147483647, nanosec: 2147483647 } },
              presentation: {
                kind: "instance",
                coherentAccess: false,
                orderedAccess: false
              },
              ownershipStrength: { value: 0 },
              timeBasedFilter: { minimumSeparation: { sec: 0, nanosec: 0 } },
              entityFactory: { autoenableCreatedEntities: true },
              writerDataLifecycle: {
                autodisposeUnregisteredInstances: true,
                autopurgeSuspendedSamplesDelay: {
                  sec: 2147483647,
                  nanosec: 2147483647
                },
                autounregisterInstanceDelay: {
                  sec: 2147483647,
                  nanosec: 2147483647
                }
              },
              readerDataLifecycle: {
                kind: "minimum_invalid_samples",
                autopurgeDisposeAll: false,
                autopurgeNowriterSamplesDelay: {
                  sec: 2147483647,
                  nanosec: 2147483647
                },
                autopurgeDisposedSamplesDelay: {
                  sec: 2147483647,
                  nanosec: 2147483647
                }
              },
              durabilityService: {
                kind: "keep_last",
                depth: 1,
                maxSamples: -1,
                maxInstances: -1,
                maxSamplesPerInstance: -1,
                serviceCleanupDelay: { sec: 0, nanosec: 0 }
              },
              deadline: { period: { sec: 2147483647, nanosec: 2147483647 } },
              destinationOrder: { kind: "by_reception_timestamp" },
              durability: { kind: "volatile" },
              history: { kind: "keep_last", depth: 1 },
              latencyBudget: { duration: { sec: 0, nanosec: 0 } },
              liveliness: {
                kind: "automatic",
                leaseDuration: { sec: 2147483647, nanosec: 2147483647 }
              },
              ownership: { kind: "shared" },
              resourceLimits: {
                maxSamples: -1,
                maxInstances: -1,
                maxSamplesPerInstance: -1
              }
            }
          }
        ]
      },
      report: {
        reportContent: {
          report: Array.from({ length: 5 }).map((_, i) => ({
            selected: i % 2 === 0,
            partition: "part1",
            publisher: "device1",
            pubCpuUsgae: 0.6687018844958892,
            pubMemoryUsgae: 17.814074211800964,
            pubBandwidthReceive: 0,
            pubBandwidthTransmit: 0,
            topic: "topic1",
            letency: 0.00007810874477500975,
            lossRate: 0,
            subscriber: "device1",
            subCpuUsgae: 0.6687018844958892,
            subMemoryUsgae: 17.814074211800964,
            subBandwidthReceive: 0,
            subBandwidthTransmit: 0
          }))
        }
      }
    };
  }
};
</script>

<style lang="sass">
.vue-codemirror
  border: 1px solid #d6d6d6

.vue-codemirror, .CodeMirror
  font-size: 14px
  border-radius: 0.3rem

.CodeMirror-gutters
  background: #fff !important

.CodeMirror-gutter
  padding-left: 14px
  background: #fff

.CodeMirror-linenumber
  padding-left: 24px

.CodeMirror-line
  padding-left: 20px !important

.code-card
  height: 100%

.card-body
  & /deep/ .vue-CodeMirror
    height: 100%
  & /deep/ .CodeMirror
    height: 100%
</style>
