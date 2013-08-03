function orbitInit(ns) {
  // Bind Orbit object for later use
  $('#weather_orbit').on('orbit:ready', function (evt, orbit) {
    // May lead to memory leak!
    ns['weatherOrbit'] = orbit
  })

  $(document).foundation('orbit', {
    animation: 'fade',
    timer_speed: 2500,
    pause_on_hover: true,
    resume_on_mouseout: true,
    animation_speed: 500,
    stack_on_small: false,
    navigation_arrows: true,
    slide_number: true,
    bullets: false,
    timer: true,
    variable_height: false,
    before_slide_change: function(){},
    after_slide_change: function(){}
  })
}

function sectionInit() {
  $(document).foundation('section', {
    one_up: false
  })
}

function chosenInit() {
  $('select').show().chosen({
    placeholder_text_single: "其他地区",
    no_results_text: "没有该地区数据……"
  })
}

function AppCtrl($scope) {
  $scope.mainCity = NS.mainCity
  $scope.otherCity = NS.otherCity
  $scope.views = []

  $scope.cityOption = ''

  $scope.citySelect = function (idx) {
    angular.forEach($scope.mainCity, function (k, v) { k['active'] = '' })

    var oldEl = $('#weather_orbit li:first')[0]

    $('#weather_orbit').hide()
    if (idx !== undefined) {
      $scope.cityOption = ''
      $scope.mainCity[idx]['active'] = 'active'
      updateViews($scope.mainCity[idx]['code'])
    } else {
      updateViews($scope.cityOption)
    }

    // Hide orbit until new nodes rendered
    var interval = setInterval(function () {
      if ($('#weather_orbit li:first')[0] != oldEl) {
        $('#weather_orbit').show()
        NS.weatherOrbit._goto(0, true)
        clearInterval(interval)
      }
    }, 300)
  }

  var updateViews = function (code) {
    var datetime = moment.utc()
    var frames = 12

    datetime.subtract('minutes', 10 * (frames + 1))

    var dateFmt1 = datetime.format('YYYY/MM/DD')
    var dateFmt2 = datetime.format('YYYYMMDD')
    var srcPrefix = '/mocimg/radar/image/' + code + '/QREF/' + dateFmt1 + '/' + code + '.QREF000.' + dateFmt2 + '.'

    datetime.minutes(Math.floor(datetime.minutes() / 10) * 10)
    datetime.seconds(0)

    $scope.views = []
    for (var i = 0; i < frames; i++) {
      $scope.views.push({
        src: srcPrefix + datetime.format('HHmmss') + '.GIF',
        text: 'UTC ' + datetime.format('YYYY-MM-DD HH:mm:ss')
      })
      datetime.add('minutes', 10)
    }
  }
}

NS = {
  weatherOrbit: null,
  mainCity: [
    { label_ZH: '北京', label_EN: 'Beijing', code: 'Z9010', active: '' },
    { label_ZH: '上海', label_EN: 'Shanghai', code: 'Z9210', active: '' },
    { label_ZH: '广州', label_EN: 'Guangzhou', code: 'Z9200', active: '' },
    { label_ZH: '沈阳', label_EN: 'Shenyang', code: 'Z9240', active: '' },
    { label_ZH: '杭州', label_EN: 'Hangzhou', code: 'Z9571', active: '' },
    { label_ZH: '深圳', label_EN: 'Shenzhen', code: 'Z9755', active: '' }
  ],
  otherCity: [
    { label_ZH: '天津', label_EN: 'Tianjin', code: 'Z9220', active: '' },
    { label_ZH: '大连', label_EN: 'Dalian', code: 'Z9411', active: '' },
    { label_ZH: '哈尔滨', label_EN: 'Haerbin', code: 'Z9451', active: '' },
    { label_ZH: '南京', label_EN: 'Nanjing', code: 'Z9250', active: '' },
    { label_ZH: '厦门', label_EN: 'Xiamen', code: 'Z9592', active: '' },
    { label_ZH: '武汉', label_EN: 'Wuhan', code: 'Z9270', active: '' },
    { label_ZH: '长沙', label_EN: 'Changsha', code: 'Z9731', active: '' },
    { label_ZH: '海口', label_EN: 'Haikou', code: 'Z9898', active: '' },
    { label_ZH: '成都', label_EN: 'Chengdu', code: 'Z9280', active: '' },
    { label_ZH: '重庆', label_EN: 'Chongqing', code: 'Z9230', active: '' },
    { label_ZH: '昆明', label_EN: 'Kunming', code: 'Z9871', active: '' },
    { label_ZH: '西安', label_EN: 'Xian', code: 'Z9290', active: '' },
    { label_ZH: '榆林', label_EN: 'Yulin', code: 'Z9912', active: '' },
    { label_ZH: '西宁', label_EN: 'Xining', code: 'Z9971', active: '' },
    { label_ZH: '乌鲁木齐', label_EN: 'Wulumuqi', code: 'Z9991', active: '' },
    { label_ZH: '拉萨', label_EN: 'Lasa', code: 'Z9891', active: '' }
  ]
}

angular.element(document).ready(function () {
  angular.bootstrap(document)

  sectionInit()
  chosenInit()

  $('.accordion').show()
  $('.accordion section:first').click()

  orbitInit(NS)
})

