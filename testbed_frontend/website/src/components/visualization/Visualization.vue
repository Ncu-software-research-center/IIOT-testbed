<template>
  <canvas id="visualization" style="border:1px solid #d3d3d3;"></canvas>
</template>

<script>
import {
  CanvasObjectCreater,
  CanvasObjectUpdater,
  CanvasDrawer
} from "./visualization-entity";

export default {
  props: ["dataSetting"],
  data() {
    return {
      updateFPS: 1000 / 120,
      canvas: null,
      ctx: null,
      drawer: null,
      topicCanvasObjects: null,
      deviceCanvasObjects: null
    };
  },
  mounted() {
    if (this.dataSetting) {
      this.init();
    }
  },
  methods: {
    init() {
      this.initCanvas();
      this.initCanvasContext();

      this.creater = new CanvasObjectCreater(this.dataSetting);
      this.createCanvasObject();

      this.updater = new CanvasObjectUpdater(this.dataSetting);

      this.drawer = new CanvasDrawer(this.ctx);

      this.render();
    },
    initCanvas() {
      this.canvas = document.getElementById("visualization");
      this.canvas.width = 900;
      this.canvas.height = 900;
      this.canvas.addEventListener("mousemove", this.mousemove);
      this.canvas.addEventListener("mouseup", this.mouseup);
      this.canvas.addEventListener("mousedown", this.mousedown);
    },
    mousemove() {},
    mouseup() {},
    mousedown() {},
    initCanvasContext() {
      this.ctx = this.canvas.getContext("2d");
      this.ctx.arrowLine = (v1, v2) => {
        this.ctx.beginPath();
        let angle = Math.atan2(v2.y - v1.y, v2.x - v1.x);
        let headlen = 10;
        this.ctx.moveTo(v1.x, v1.y);
        let arrowHeight = headlen * Math.cos(Math.PI / 7);
        let deltaX = arrowHeight * Math.cos(angle);
        let deltaY = arrowHeight * Math.sin(angle);
        this.ctx.lineTo(v2.x - deltaX, v2.y - deltaY);
        this.ctx.lineTo(
          v2.x - headlen * Math.cos(angle - Math.PI / 7),
          v2.y - headlen * Math.sin(angle - Math.PI / 7)
        );
        this.ctx.lineTo(v2.x, v2.y);
        this.ctx.lineTo(
          v2.x - headlen * Math.cos(angle + Math.PI / 7),
          v2.y - headlen * Math.sin(angle + Math.PI / 7)
        );
        this.ctx.lineTo(v2.x - deltaX, v2.y - deltaY);
      };
    },
    createCanvasObject() {
      this.deviceCanvasObjects = this.creater.createDeviceCanvasObjects();
      this.topicCanvasObjects = this.creater.createTopicCanvasObjects();

      this.creater.createPublisherCanvasObjects();
      this.creater.createSubscriberCanvasObjects();
      this.creater.createDataWriterCanvasObjects();
      this.creater.createDataReaderCanvasObjects();
    },
    render() {
      // Clear previous drawing
      this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

      this.update();
      this.draw();
    },
    update() {
      this.updateCanvasWidth();
    },
    updateCanvasWidth() {
      let hitWallDevice = this.deviceCanvasObjects.find(d => {
        return (
          d.startPosition.x + d.width + d.additionalWidth + 100 >=
          this.canvas.width
        );
      });

      while (hitWallDevice !== undefined) {
        while (
          hitWallDevice.startPosition.x +
            hitWallDevice.width +
            hitWallDevice.additionalWidth >=
          this.canvas.width
        ) {
          this.canvas.width = this.canvas.width * 2;
        }
        hitWallDevice = this.deviceCanvasObjects.find(d => {
          return (
            d.startPosition.x + d.width + d.additionalWidth + 100 >=
            this.canvas.width
          );
        });
      }
    },
    draw() {
      this.drawer.drawDevices(this.deviceCanvasObjects);
      this.drawer.drawTopics(this.topicCanvasObjects);
      this.drawer.drawPublishers(this.deviceCanvasObjects);
      this.drawer.drawSubscribers(this.deviceCanvasObjects);
      this.drawer.drawDataWriters(this.deviceCanvasObjects);
      this.drawer.drawDataReaders(this.deviceCanvasObjects);
    }
  },
  watch: {
    dataSetting() {
      console.log("watch");
      this.init();
    }
  }
};
</script>

<style>
</style>
