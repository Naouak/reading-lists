<template>
  <div class="card-content">
    <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
          <p class="control has-icons-left">
            <VSelect :value="value.available_online"
                     :options="availableOptions"
                     @input="updateFilters('available_online',$event)"></VSelect>
          </p>
        </div>
      </div>
    </div>
    <div class="field is-horizontal">
      <div class="field-body">
        <div class="field">
          <p class="control has-icons-left">
            <select :value="value.ordering" @input="updateFilters('ordering', $event.target.value)">
              <option value="-created_date">Creation (Newest first)</option>
              <option value="created_date">Creation (Oldest first)</option>
              <option value="-pub_date">Publication (Newest first)</option>
              <option value="pub_date">Publication (Oldest first)</option>
              <option value="-availability_date">Availability (Newest first)</option>
              <option value="availability_date">Availability (Oldest first)</option>
              <option value="-availability_last_check">Found (Newest first)</option>
              <option value="availability_last_check">Found (Oldest first)</option>
            </select>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import VSelect from "~/components/VSelect.vue";

export default {
  name: "BookFiltersCard",
  components: { VSelect },
  props: {
    value: {},
    available_online: {},
    ordering: {}
  },
  data() {
    return {
      availableOptions: [
        {value: null, text: "All"},
        {value: 1, text: "Only Available"},
        {value: 0, text: "Only non Available"},
      ]
    };
  },
  methods: {
    updateFilters(field, value) {
      this.$emit("input", {
        ...this.value,
        [field]: value
      });
    }
  }
};
</script>
