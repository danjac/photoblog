document.addEventListener('alpine:init', () => {
  Alpine.data('dropdown', () => ({
    open: false,
    init() {
      this._dropdownId = this.$id('dropdown');
      this._onDropdownOpen = this.onDropdownOpen.bind(this);
      this._close = this.close.bind(this);
      window.addEventListener('dropdown-open', this._onDropdownOpen);
      window.addEventListener('htmx:beforeRequest', this._close);
    },
    destroy() {
      window.removeEventListener('dropdown-open', this._onDropdownOpen);
      window.removeEventListener('htmx:beforeRequest', this._close);
    },
    onDropdownOpen(e) {
      if (e.detail.id !== this._dropdownId) this.close();
    },
    toggle() {
      this.open = !this.open;
      if (this.open) this.$dispatch('dropdown-open', { id: this._dropdownId });
    },
    close() { this.open = false; },
  }));
});
