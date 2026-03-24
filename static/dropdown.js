document.addEventListener('alpine:init', () => {
  let _nextId = 0;

  Alpine.store('dropdown', { activeId: null });

  document.addEventListener('htmx:beforeRequest', () => {
    Alpine.store('dropdown').activeId = null;
  });

  Alpine.data('dropdown', () => ({
    _id: ++_nextId,
    get open() { return Alpine.store('dropdown').activeId === this._id; },
    toggle() { Alpine.store('dropdown').activeId = this.open ? null : this._id; },
    close() { if (this.open) Alpine.store('dropdown').activeId = null; },
  }));
});
