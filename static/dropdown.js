document.addEventListener('alpine:init', () => {
  Alpine.data('dropdown', () => ({
    open: false,
    init() {
      window.addEventListener('dropdown-open', this.onDropdownOpen);
      window.addEventListener('htmx:beforeRequest', this.close);
    },
    destroy() {
      window.removeEventListener('dropdown-open', this.onDropdownOpen);
      window.removeEventListener('htmx:beforeRequest', this.close);
    },
    onDropdownOpen(e) {
      if (e.target !== this.$el) this.close();
    },
    toggle() {
      this.open = !this.open;
      if (this.open) this.$dispatch('dropdown-open');
    },
    close() { this.open = false; },
  }));
});
