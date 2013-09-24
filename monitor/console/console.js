$(function () {
  var currentPage = 0
  var totalPage = 12

  $('#current_page').text(currentPage + 1)
  $('#total_page').text(totalPage)

  $('.image-a').on('click', function (evt) {
    $('#modal_title').html(evt.target.title)
    $('#modal_image').attr('src', evt.target.src)
  })

  $('.pager').on('click', 'li', function (evt) {
    evt.stopPropagation()

    if (currentPage > 0 && $(this).hasClass('previous')) {
      currentPage -= 1
    } else if (currentPage < totalPage - 1 && $(this).hasClass('next')) {
      currentPage += 1
    } else {
      return false
    }

    if (currentPage > 0) {
      $('.pager .previous').removeClass('disabled')
    } else {
      $('.pager .previous').addClass('disabled')
    }
    if (currentPage < totalPage - 1) {
      $('.pager .next').removeClass('disabled')
    } else {
      $('.pager .next').addClass('disabled')
    }

    var timestamp = (new Date()).getTime()

    $('#current_page').text(currentPage + 1)

    $('#raw_image').attr('src', 'img/raw-' + currentPage + '.gif?_t=' + timestamp)
    $('#bi_image').attr('src', 'img/bi-' + currentPage + '.jpeg?_t=' + timestamp)
    $('#extract_image').attr('src', 'img/extract-' + currentPage + '.jpeg?_t=' + timestamp)
    $('#path_image').attr('src', 'img/path-' + currentPage + '.jpeg?_t=' + timestamp)
    $('#zone_image').attr('src', 'img/zone-' + currentPage + '.jpeg?_t=' + timestamp)
  })

})
