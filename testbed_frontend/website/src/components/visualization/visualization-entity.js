const deviceProperty = {
  width: 200,
  height: 80,
  offsetX: 100,
  offsetY: 100,
  marginLeft: 100,
  paddingX: 10
};

const topicProperty = {
  width: 100,
  height: 10,
  offsetX: 100,
  offsetY: 240,
  marginTop: 60
};

const publisherProperty = {
  offsetY: 60,
  marginRight: 20
};

const dataWriterProperty = {
  offsetY: 70,
  marginRight: 20
};

const subscriberProperty = {
  offsetY: 60,
  marginLeft: 20
};

const dataReaderProperty = {
  offsetY: 70,
  marginLeft: 20
};

class CanvasObjectCreater {
  constructor(dataSetting) {
    this.dataSetting = dataSetting;
    this.devicesCanvasObjects = [];
    this.topicsCanvasObject = [];
  }

  createTopicCanvasObjects() {
    const topicWidth = this.devicesCanvasObjects.reduce((a, b) => {
      return a + b.width + b.additionalWidth + deviceProperty.offsetX;
    }, 0);

    // let topicWidth =
    //   this.dataSetting["device"].length *
    //   (deviceProperty.width + deviceProperty.offsetX);
    console.log(this.devicesCanvasObjects);
    this.topicsCanvasObject = this.dataSetting["topic"].map((t, i) => {
      return new Topic({
        name: t["name"],
        width: topicWidth,
        startPosition: new Vec2(
          topicProperty.offsetX,
          i * topicProperty.marginTop + topicProperty.offsetY
        )
      });
    });
    return this.topicsCanvasObject;
  }

  createDeviceCanvasObjects() {
    this.dataSetting["device"].forEach((d, i) => {
      // calculate additional width by counting the number of entities
      const addtionalWidth = this.calculateAdditionalWidth(d);
      const width = deviceProperty.width + addtionalWidth;

      let startX =
        i * (deviceProperty.width + deviceProperty.marginLeft) +
        deviceProperty.offsetX;
      // Check if current device has additional width, then, update the start position x.
      if (this.devicesCanvasObjects.length > 0) {
        // Get the addtional width of last device object
        const n = this.devicesCanvasObjects.length - 1;
        startX += this.devicesCanvasObjects[n].addtionalWidth;
      }
      const startY = deviceProperty.offsetY;

      const newDevice = new Device({
        name: d["name"],
        addtionalWidth: addtionalWidth,
        width: width,
        startPosition: new Vec2(startX, startY)
      });

      this.devicesCanvasObjects.push(newDevice);
    });
    return this.devicesCanvasObjects;
  }

  updateDeviceWidth(deviceCanvasObjects) {
    this.dataSetting["device"].forEach(d => {
      let device = deviceCanvasObjects.find(dco => dco.name === d.name);
      device.additionalWidth = this.calculateAdditionalWidth(d);
      device.width = deviceProperty.width + device.additionalWidth;
    });
  }

  /**
   * calculate additional width by counting the number of publishers and subscribers.
   */
  calculateAdditionalWidth(device) {
    let entityNum = this.getNumOfPubAndSub(device["domain"][0]["partition"]);

    let additionalWidth = 0;
    if (entityNum.pubNum > 4) {
      additionalWidth += (entityNum.pubNum - 4) * publisherProperty.marginRight;
    }
    if (entityNum.subNum > 4) {
      additionalWidth += (entityNum.subNum - 4) * subscriberProperty.marginLeft;
    }
    return additionalWidth;
  }

  getNumOfPubAndSub(partitions) {
    let pubNum = 0;
    let subNum = 0;
    partitions.forEach(p => {
      // Check if the partition has publishers
      if (Array.isArray(p["publisher"])) {
        pubNum += p["publisher"].reduce(
          (len, pub) => len + pub["dataWriter"].length,
          0
        );
      }
      // Check if the partition has subscribers
      if (Array.isArray(p["subscriber"])) {
        subNum += p["subscriber"].reduce(
          (len, pub) => len + pub["dataReader"].length,
          0
        );
      }
    });

    return { pubNum, subNum };
  }

  createPublisherCanvasObjects() {
    this.dataSetting["device"].forEach(d => {
      const publishers = [];

      const deviceCanvasObject = this.devicesCanvasObjects.find(
        dcb => dcb.name === d.name
      );

      d["domain"][0]["partition"].forEach(partition => {
        const p = this.generatePublisherCanvasObjects(
          partition,
          deviceCanvasObject
        );
        publishers.push(...p);
      });
      deviceCanvasObject.publishers = publishers;
    });
  }

  generatePublisherCanvasObjects(partition, deviceCanvasObject) {
    // Check if the parition has publishers
    if (!Array.isArray(partition["publisher"])) return [];

    const publishers = [];
    partition["publisher"].forEach(({ id, dataWriter }) => {
      const dataWriterNum = dataWriter.length;

      // Get last publisher position
      let lastPubOffsetX = 0;
      if (publishers.length > 0) {
        const lastPubPositionX =
          publishers[publishers.length - 1].startPosition.x;
        lastPubOffsetX = deviceCanvasObject.width / 2 - lastPubPositionX;
      }

      const startX =
        deviceCanvasObject.width / 2 -
        dataWriterNum * dataWriterProperty.marginRight -
        lastPubOffsetX;
      const startY = publisherProperty.offsetY;

      const newPub = new Publisher({
        id,
        device: deviceCanvasObject,
        startPosition: new Vec2(startX, startY),
        width: (dataWriterNum - 1) * dataWriterProperty.marginRight
      });

      publishers.push(newPub);
    });

    return publishers;
  }

  createSubscriberCanvasObjects() {
    let subscribers = [];

    this.dataSetting["device"].forEach(d => {
      subscribers = [];
      let deviceCanvasObject = this.devicesCanvasObjects.find(
        dcb => dcb.name === d.name
      );

      d["domain"][0]["partition"].forEach(partition => {
        subscribers.push(
          ...this.getSubscriberObject(partition, deviceCanvasObject)
        );
      });
      deviceCanvasObject.subscribers = subscribers;
    });
  }

  getSubscriberObject(partition, deviceCanvasObject) {
    let subscribers = [];

    // Check if the parition has subscribers
    if (Array.isArray(partition["subscriber"])) {
      partition["subscriber"].forEach(({ id, dataReader }) => {
        const dataReaderNum = dataReader.length;

        // Get last subscriber position and computer offset
        let lastSubOffsetX = 0;
        if (subscribers.length > 0) {
          const lastSubPositionX =
            subscribers[subscribers.length - 1].startPosition.x +
            subscribers[subscribers.length - 1].width;
          lastSubOffsetX = lastSubPositionX - deviceCanvasObject.width / 2;
        }

        const startX =
          deviceCanvasObject.width / 2 +
          dataReaderProperty.marginLeft +
          lastSubOffsetX;
        const startY = subscriberProperty.offsetY;

        const newPub = new Subscriber({
          id: id,
          device: deviceCanvasObject,
          startPosition: new Vec2(startX, startY),
          width: (dataReaderNum - 1) * dataReaderProperty.marginLeft
        });
        subscribers.push(newPub);
      });
    }
    return subscribers;
  }

  createDataWriterCanvasObjects() {
    let dataWriters = [];

    this.dataSetting["device"].forEach(({ domain, name }) => {
      let deviceCanvasObject = this.devicesCanvasObjects.find(
        dcb => dcb.name === name
      );
      domain[0]["partition"].forEach(({ publisher }) => {
        if (!Array.isArray(publisher)) {
          return;
        }
        publisher.forEach(({ id, dataWriter }) => {
          dataWriters = [];

          // Get last publisher position and computer offset
          const pubIndex = deviceCanvasObject.publishers.findIndex(
            pub => pub.id === id
          );

          let lastPubOffsetX = 0;
          if (pubIndex > 0) {
            const lastPubPositionX =
              deviceCanvasObject.publishers[pubIndex - 1].startPosition.x;
            lastPubOffsetX = deviceCanvasObject.width / 2 - lastPubPositionX;
          }

          dataWriter.forEach((dw, index) => {
            const dstTopic = this.getPubDstTopic(dw.dstTopic);

            const startX =
              deviceCanvasObject.width / 2 -
              (index + 1) * dataWriterProperty.marginRight -
              lastPubOffsetX;
            const startY = dataWriterProperty.offsetY;
            const endX =
              deviceCanvasObject.width / 2 -
              (index + 1) * dataWriterProperty.marginRight -
              lastPubOffsetX;
            const endY = dstTopic.startPosition.y - deviceProperty.offsetY;

            const newDataWriter = new DataWriter({
              startPosition: new Vec2(startX, startY),
              endPosition: new Vec2(endX, endY)
            });
            dataWriters.push(newDataWriter);
          });
          const publisherCanvasObject = deviceCanvasObject.publishers[pubIndex];
          publisherCanvasObject.dataWriters = dataWriters;
        });
      });
    });
  }

  getPubDstTopic(dstTopicName) {
    return this.topicsCanvasObject.find(t => t.name === dstTopicName);
  }

  createDataReaderCanvasObjects() {
    let dataReaders = [];

    this.dataSetting["device"].forEach(({ domain, name }) => {
      let deviceCanvasObject = this.devicesCanvasObjects.find(
        dcb => dcb.name === name
      );
      domain[0]["partition"].forEach(({ subscriber }) => {
        if (!Array.isArray(subscriber)) {
          return;
        }
        subscriber.forEach(({ id, dataReader }) => {
          dataReaders = [];

          // Get last publisher position and computer offset
          const subIndex = deviceCanvasObject.subscribers.findIndex(
            pub => pub.id === id
          );

          let lastSubOffsetX = 0;
          if (subIndex > 0) {
            const lastSubPositionX =
              deviceCanvasObject.subscribers[subIndex - 1].startPosition.x +
              deviceCanvasObject.subscribers[subIndex - 1].width;
            lastSubOffsetX = lastSubPositionX - deviceCanvasObject.width / 2;
          }

          dataReader.forEach((dr, index) => {
            const srcTopic = this.getSubSrcTopics(dr.srcTopic);

            const startX =
              deviceCanvasObject.width / 2 +
              (index + 1) * dataReaderProperty.marginLeft +
              lastSubOffsetX;
            const startY = dataReaderProperty.offsetY;
            const endX =
              deviceCanvasObject.width / 2 +
              (index + 1) * dataReaderProperty.marginLeft +
              lastSubOffsetX;
            const endY = srcTopic.startPosition.y - deviceProperty.offsetY;

            const newDataReader = new DataReader({
              startPosition: new Vec2(startX, startY),
              endPosition: new Vec2(endX, endY)
            });

            dataReaders.push(newDataReader);
          });
          const subscriberCanvasObject =
            deviceCanvasObject.subscribers[subIndex];
          subscriberCanvasObject.dataReaders = dataReaders;
        });
      });
    });
  }

  getSubSrcTopics(srcTopicName) {
    return this.topicsCanvasObject.find(t => t.name === srcTopicName);
  }
}

class CanvasObjectUpdater {
  constructor(dataSetting) {
    this.dataSetting = dataSetting;
  }

  updateDevicePosition(devices) {}

  updatePublisherPosition(deviceCanvasObjects) {}

  updateSubscriberPosition(deviceCanvasObjects) {}

  updateDataWriterPosition() {}

  updateDataReaderPosition() {}
}

class CanvasDrawer {
  constructor(ctx) {
    this.ctx = ctx;
  }
  drawTopics(topicCanvasObjects) {
    this.ctx.font = "normal 16px Arial";
    topicCanvasObjects.map(t => {
      this.ctx.save();
      this.ctx.translate(t.startPosition.x, t.startPosition.y);

      this.ctx.strokeStyle = "#6C49B8";
      this.ctx.fillStyle = "#6C49B8";
      this.ctx.arrowLine(new Vec2(0, 0), new Vec2(t.width, 0));
      this.ctx.stroke();
      this.ctx.fill();

      this.ctx.font = "normal 16px Arial";
      this.ctx.textBaseline = "middle";
      this.ctx.fillStyle = "green";
      this.ctx.fillText(t.name, t.width + 10, 0);
      this.ctx.restore();
    });
  }
  drawDevices(deviceCanvasObjects) {
    deviceCanvasObjects.forEach(d => {
      this.ctx.save();
      this.ctx.translate(d.startPosition.x, d.startPosition.y);

      this.ctx.strokeStyle = "#6C49B8";
      this.ctx.fillStyle = "#fff";
      this.ctx.strokeRect(0, 0, d.width, d.height);
      this.ctx.fillRect(0, 0, d.width, d.height);
      this.ctx.stroke();
      this.ctx.fill();

      this.ctx.font = "lighter 16px Arial";
      this.ctx.textAlign = "center";
      this.ctx.textBaseline = "middle";
      this.ctx.fillStyle = "#000";
      this.ctx.fillText(d.name, d.width / 2, d.height / 2);
      this.ctx.restore();
    });
  }
  drawPublishers(deviceCanvasObjects) {
    deviceCanvasObjects.forEach(({ publishers }) => {
      publishers.forEach(pub => {
        this.ctx.save();
        this.ctx.translate(
          pub.device.startPosition.x,
          pub.device.startPosition.y
        );
        this.ctx.translate(pub.startPosition.x, pub.startPosition.y);

        this.ctx.strokeStyle = "#6C49B8";
        this.ctx.fillStyle = "#6C49B8";
        this.ctx.strokeRect(0, 0, pub.width, pub.height);
        this.ctx.fillRect(0, 0, pub.width, pub.height);
        this.ctx.stroke();
        this.ctx.fill();

        this.ctx.restore();
      });
    });
  }
  drawSubscribers(deviceCanvasObjects) {
    deviceCanvasObjects.forEach(({ subscribers }) => {
      subscribers.forEach(sub => {
        this.ctx.save();
        this.ctx.translate(
          sub.device.startPosition.x,
          sub.device.startPosition.y
        );
        this.ctx.translate(sub.startPosition.x, sub.startPosition.y);

        this.ctx.strokeStyle = "#6C49B8";
        this.ctx.fillStyle = "#6C49B8";
        this.ctx.strokeRect(0, 0, sub.width, sub.height);
        this.ctx.fillRect(0, 0, sub.width, sub.height);
        this.ctx.stroke();
        this.ctx.fill();

        this.ctx.restore();
      });
    });
  }

  drawDataWriters(deviceCanvasObjects) {
    deviceCanvasObjects.forEach(({ publishers, startPosition }) => {
      publishers.forEach(({ dataWriters }) => {
        dataWriters.forEach(dw => {
          this.ctx.save();
          this.ctx.translate(startPosition.x, startPosition.y);

          this.ctx.fillStyle = "#6C49B8";
          this.ctx.strokeStyle = "#6C49B8";
          this.ctx.arrowLine(dw.startPosition, dw.endPosition);
          this.ctx.stroke();
          this.ctx.fill();
          this.ctx.restore();
        });
      });
    });
  }

  drawDataReaders(deviceCanvasObjects) {
    deviceCanvasObjects.forEach(({ subscribers, startPosition }) => {
      subscribers.forEach(({ dataReaders }) => {
        dataReaders.forEach(dw => {
          this.ctx.save();
          this.ctx.translate(startPosition.x, startPosition.y);

          this.ctx.fillStyle = "#6C49B8";
          this.ctx.strokeStyle = "#6C49B8";
          this.ctx.arrowLine(dw.endPosition, dw.startPosition);
          this.ctx.stroke();
          this.ctx.fill();
          this.ctx.restore();
        });
      });
    });
  }
}

class Vec2 {
  constructor(x, y) {
    this.x = x || 0;
    this.y = y || 0;
  }
  set(v) {
    this.x = v.x;
    this.y = v.y;
  }
  move(x, y) {
    this.x += x;
    this.y += y;
  }
  add(v) {
    return new Vec2(this.x + v.x, this.y + v.y);
  }
  sub(v) {
    return new Vec2(this.x - v.x, this.y - v.y);
  }
  mul(s) {
    return new Vec2(this.x * s, this.y * s);
  }
  get length() {
    return Math.sqrt(this.x * this.x + this.y * this.y);
  }
  set length(nv) {
    let temp = this.unit.mul(nv);
    this.set(temp.x, temp.y);
  }
  clone() {
    return new Vec2(this.x, this.y);
  }
  toString() {
    return `(${this.x}, ${this.y})`;
  }
  equal(v) {
    return this.x === v.x && this.y === v.y;
  }
  get angle() {
    return Math.atan2(this.y, this.x);
  }
  get unit() {
    return this.mul(1 / this.length);
  }
}

class Device {
  constructor(args) {
    let def = {
      id: 0,
      name: "device",
      width: 200,
      height: 80,
      additionalWidth: 0,
      startPosition: new Vec2(),
      publishers: [],
      subscribers: []
    };
    Object.assign(def, args);
    Object.assign(this, def);
  }
}

class Topic {
  constructor(args) {
    let def = {
      id: 0,
      name: "topic",
      width: 100,
      height: 10,
      startPosition: new Vec2(),
      endPosition: new Vec2()
    };
    Object.assign(def, args);
    Object.assign(this, def);
  }
}

class Publisher {
  constructor(args) {
    let def = {
      id: 0,
      name: "publisher",
      width: 0,
      height: 10,
      device: null,
      dataWriters: [],
      startPosition: new Vec2()
    };
    Object.assign(def, args);
    Object.assign(this, def);
  }
}

class Subscriber {
  constructor(args) {
    let def = {
      id: 0,
      name: "subscriber",
      width: 0,
      height: 10,
      device: null,
      dataReaders: [],
      startPosition: new Vec2()
    };
    Object.assign(def, args);
    Object.assign(this, def);
  }
}

// eslint-disable-next-line
class DataWriter {
  constructor(args) {
    let def = {
      id: 0,
      name: "data writer",
      startPosition: new Vec2(),
      endPosition: new Vec2()
    };
    Object.assign(def, args);
    Object.assign(this, def);
  }
}

// eslint-disable-next-line
class DataReader {
  constructor(args) {
    let def = {
      id: 0,
      name: "data reader",
      startPosition: new Vec2(),
      endPosition: new Vec2()
    };
    Object.assign(def, args);
    Object.assign(this, def);
  }
}

export { CanvasObjectCreater, CanvasObjectUpdater, CanvasDrawer };
