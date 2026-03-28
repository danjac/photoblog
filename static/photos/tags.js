document.addEventListener('alpine:init', () => {
  Alpine.data('tagWidget', (initial) => ({
    tags: initial ? initial.trim().split(/\s+/) : [],

    onInput(event) {
      const value = event.target.value;
      if (!value.endsWith(' ')) return;
      const tag = value.trim().toLowerCase();
      event.target.value = '';
      if (tag && !this.tags.includes(tag)) {
        this.tags = [...this.tags, tag];
      }
    },

    addTag() {
      const tag = this.$refs.tagInput.value.trim().toLowerCase();
      this.$refs.tagInput.value = '';
      if (tag && !this.tags.includes(tag)) {
        this.tags = [...this.tags, tag];
      }
    },

    removeTag(tag) {
      this.tags = this.tags.filter((t) => t !== tag);
    },

    removeLastTag() {
      if (this.tags.length > 0) {
        this.tags = this.tags.slice(0, -1);
      }
    },
  }));
});
