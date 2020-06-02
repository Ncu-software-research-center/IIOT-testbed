<template>
  <div
    id="dsal-viewer"
    class="modal fade bd-example-modal-xl"
    tabindex="-1"
    role="dialog"
    aria-labelledby="myExtraLargeModalLabel"
    aria-hidden="true"
  >
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header cm-bg-gray">
          <h5 class="modal-title h5" id="myExtraLargeModalLabel">
            DSAL Viewer
            <span class="badge badge-primary ml-2 mb-1">VIEW</span>
          </h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">×</span>
          </button>
        </div>
        <div class="modal-body code-body p-0">
          <codemirror v-model="code" :options="cmOptions"></codemirror>
        </div>
      </div>
    </div>
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

export default {
  components: {
    codemirror
  },
  props: ["dsal"],
  data() {
    return {
      code: "",
      cmOptions: {
        // codemirror options
        tabSize: 2,
        mode: "yaml",
        lineNumbers: true,
        line: true,
        readOnly: "nocursor"
      }
    };
  },
  watch: {
    dsal() {
      if (this.dsal) {
        this.code = this.dsal.dsalContent;
      }
    }
  }
};
</script>

<style lang="sass" scoped>
.code-body
  & /deep/ .cm-bg-gray
    background-color: rgb(244, 245, 247)

  & /deep/ .CodeMirror
    font-size: 14px

  & /deep/ .vue-codemirror, & /deep/ .CodeMirror
    height: calc(100vh - 200px)
    border-bottom-left-radius: 0.3rem
    border-bottom-right-radius: 0.3rem

  & /deep/ .CodeMirror-gutter
    padding-left: 4px

  & /deep/ .CodeMirror-linenumber
    padding-left: 32px

  & /deep/ .CodeMirror-line
    padding-left: 16px !important
</style>
