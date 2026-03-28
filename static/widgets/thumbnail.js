document.addEventListener('alpine:init', () => {
  Alpine.data('thumbnailWidget', () => ({
    previewUrl: null,

    onFileChange(event) {
      const file = event.target.files[0];
      this.previewUrl = file ? URL.createObjectURL(file) : null;
    },
  }));
});
