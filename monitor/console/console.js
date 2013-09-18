$('.image-a').on('click', function (evt) {
  $('#modal_title').html(evt.target.title)
  $('#modal_image').attr('src', evt.target.src)
})

$('.pagination').on('click', 'li', function (evt) {
  var idx = $(this).data('idx')
  var timestamp = (new Date()).getTime()

  $('.pagination li.active').removeClass('active')
  $(this).addClass('active')

  $('#origin_image').attr('src', 'img/origin-' + idx + '.gif?_t=' + timestamp)
  $('#bi_image').attr('src', 'img/bi-' + idx + '.jpeg?_t=' + timestamp)
  $('#extract_image').attr('src', 'img/extract-' + idx + '.jpeg?_t=' + timestamp)
  $('#path_image').attr('src', 'img/path-' + idx + '.jpeg?_t=' + timestamp)
  $('#area_image').attr('src', 'img/area-' + idx + '.jpeg?_t=' + timestamp)
})
