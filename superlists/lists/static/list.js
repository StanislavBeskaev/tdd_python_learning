window.Superlists = {}
window.Superlists.initialize = () => {
  $('input[name="text"]').on('keypress', () => $('.has-error').hide())
}
