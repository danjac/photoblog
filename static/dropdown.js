document.addEventListener('alpine:init', () => {
  Alpine.data('dropdown', () => ({
    open: false,
    toggle() {
      this.open = !this.open;
      if (this.open) this.$dispatch('dropdown-open');
    },
    close() { this.open = false; },
  }));
});
