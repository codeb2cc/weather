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
  $scope.cityInfo = NS.cityInfo
  $scope.views = []

  $scope.cityOption = ''

  $scope.citySelect = function (evt, code) {
    var oldEl = $('#weather_orbit li:first')[0]

    $('.accordion section.active').removeClass('active')
    $('#weather_orbit').hide()

    if (code !== undefined) {
      $scope.cityOption = ''
      $('#city_' + code).addClass('active')
    } else {
      code = $scope.cityOption
    }

    updateViews(code)

    // Hide orbit until new nodes rendered
    var interval = setInterval(function () {
      if ($('#weather_orbit li:first')[0] != oldEl) {
        $('#weather_orbit').show()
        NS.weatherOrbit._goto(0, true)
        clearInterval(interval)
      }
    }, 300)

    evt.preventDefault()
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
  cityInfo: [
    { label_ZH: '北京', label_EN: 'Beijing', code: 'Z9010', major: true },
    { label_ZH: '天津', label_EN: 'Tianjin', code: 'Z9220', major: false },
    { label_ZH: '石家庄', label_EN: 'Shijiazhuang', code: 'Z9311', major: false },
    { label_ZH: '秦皇岛', label_EN: 'Qinhuangdao', code: 'Z9335', major: false },
    { label_ZH: '张北', label_EN: 'Zhangbei', code: 'Z9313', major: false },
    { label_ZH: '沧州', label_EN: 'Cangzhou', code: 'Z9317', major: false },
    { label_ZH: '承德', label_EN: 'Chende', code: 'Z9314', major: false },
    { label_ZH: '太原', label_EN: 'Taiyuan', code: 'Z9351', major: false },
    { label_ZH: '大同', label_EN: 'Datong', code: 'Z9352', major: false },
    { label_ZH: '临汾', label_EN: 'Linfen', code: 'Z9357', major: false },
    { label_ZH: '长治', label_EN: 'Changzhi', code: 'Z9355', major: false },
    { label_ZH: '呼和浩特', label_EN: 'Huhehaote', code: 'Z9471', major: false },
    { label_ZH: '赤峰', label_EN: 'Chifeng', code: 'Z9476', major: false },
    { label_ZH: '鄂尔多斯', label_EN: 'Eerduosi', code: 'Z9477', major: false },
    { label_ZH: '海拉尔', label_EN: 'Hailaer', code: 'Z9470', major: false },
    { label_ZH: '临河', label_EN: 'Linhe', code: 'Z9478', major: false },
    { label_ZH: '加格达齐', label_EN: 'Jiagedaqi', code: 'Z9457', major: false },
    { label_ZH: '沈阳', label_EN: 'Shenyang', code: 'Z9240', major: false },
    { label_ZH: '大连', label_EN: 'Dalian', code: 'Z9411', major: false },
    { label_ZH: '营口', label_EN: 'Yingkou', code: 'Z9417', major: false },
    { label_ZH: '长春', label_EN: 'Changchun', code: 'Z9431', major: false },
    { label_ZH: '白山', label_EN: 'Baishan', code: 'Z9439', major: false },
    { label_ZH: '白城', label_EN: 'Baicheng', code: 'Z9436', major: false },
    { label_ZH: '佳木斯', label_EN: 'Jiamusi', code: 'Z9454', major: false },
    { label_ZH: '齐齐哈尔', label_EN: 'Qiqihaer', code: 'Z9452', major: false },
    { label_ZH: '牡丹江', label_EN: 'Mudanjiang', code: 'Z9453', major: false },
    { label_ZH: '建三江', label_EN: 'Jiansanjiang', code: 'Z9085', major: false },
    { label_ZH: '哈尔滨', label_EN: 'Haerbin', code: 'Z9451', major: false },
    { label_ZH: '上海', label_EN: 'Shanghai', code: 'Z9210', major: true },
    { label_ZH: '南京', label_EN: 'Nanjing', code: 'Z9250', major: false },
    { label_ZH: '连云港', label_EN: 'Lianyungang', code: 'Z9518', major: false },
    { label_ZH: '徐州', label_EN: 'Xuzhou', code: 'Z9516', major: false },
    { label_ZH: '南通', label_EN: 'Nantong', code: 'Z9513', major: false },
    { label_ZH: '盐城', label_EN: 'Yancheng', code: 'Z9515', major: false },
    { label_ZH: '常州', label_EN: 'Changzhou', code: 'Z9519', major: false },
    { label_ZH: '衢州', label_EN: 'Quzhou', code: 'Z9570', major: false },
    { label_ZH: '宁波', label_EN: 'Ningbo', code: 'Z9574', major: false },
    { label_ZH: '温州', label_EN: 'Wenzhou', code: 'Z9577', major: false },
    { label_ZH: '杭州', label_EN: 'Hangzhou', code: 'Z9571', major: true },
    { label_ZH: '金华', label_EN: 'Jinhua', code: 'Z9579', major: false },
    { label_ZH: '舟山', label_EN: 'Danshan', code: 'Z9580', major: false },
    { label_ZH: '马鞍山', label_EN: 'Maanshan', code: 'Z9555', major: false },
    { label_ZH: '合肥', label_EN: 'Hefei', code: 'Z9551', major: false },
    { label_ZH: '阜阳', label_EN: 'Fuyang', code: 'Z9558', major: false },
    { label_ZH: '蚌埠', label_EN: 'Bengbu', code: 'Z9552', major: false },
    { label_ZH: '安庆', label_EN: 'Anqin', code: 'Z9556', major: false },
    { label_ZH: '黄山', label_EN: 'Huangshan', code: 'Z9559', major: false },
    { label_ZH: '建阳', label_EN: 'Jianyang', code: 'Z9599', major: false },
    { label_ZH: '龙岩', label_EN: 'Longyan', code: 'Z9597', major: false },
    { label_ZH: '福州', label_EN: 'Fuzhou', code: 'Z9591', major: false },
    { label_ZH: '厦门', label_EN: 'Xiamen', code: 'Z9592', major: false },
    { label_ZH: '上饶', label_EN: 'Shangrao', code: 'Z9793', major: false },
    { label_ZH: '南昌', label_EN: 'Nanchang', code: 'Z9791', major: false },
    { label_ZH: '九江', label_EN: 'Jiujiang', code: 'Z9792', major: false },
    { label_ZH: '赣州', label_EN: 'Ganzhou', code: 'Z9797', major: false },
    { label_ZH: '吉安', label_EN: 'Jian', code: 'Z9796', major: false },
    { label_ZH: '济南', label_EN: 'Jinan', code: 'Z9531', major: false },
    { label_ZH: '烟台', label_EN: 'Yantai', code: 'Z9535', major: false },
    { label_ZH: '青岛', label_EN: 'Qingdao', code: 'Z9532', major: false },
    { label_ZH: '泰山', label_EN: 'Taishan', code: 'Z9538', major: false },
    { label_ZH: '滨州', label_EN: 'Binzhou', code: 'Z9543', major: false },
    { label_ZH: '商丘', label_EN: 'Shangqiu', code: 'Z9370', major: false },
    { label_ZH: '南阳', label_EN: 'Nanyang', code: 'Z9377', major: false },
    { label_ZH: '郑州', label_EN: 'Zhengzhou', code: 'Z9371', major: false },
    { label_ZH: '洛阳', label_EN: 'Luoyang', code: 'Z9379', major: false },
    { label_ZH: '驻马店', label_EN: 'Zhumadian', code: 'Z9396', major: false },
    { label_ZH: '三门峡', label_EN: 'Sanmenxia', code: 'Z9398', major: false },
    { label_ZH: '濮阳', label_EN: 'Puyang', code: 'Z9393', major: false },
    { label_ZH: '随州', label_EN: 'Suizhou', code: 'Z9722', major: false },
    { label_ZH: '恩施', label_EN: 'Enshi', code: 'Z9718', major: false },
    { label_ZH: '十堰', label_EN: 'Shiyan', code: 'Z9719', major: false },
    { label_ZH: '荆州', label_EN: 'Jingzhou', code: 'Z9716', major: false },
    { label_ZH: '武汉', label_EN: 'Wuhan', code: 'Z9270', major: false },
    { label_ZH: '宜昌', label_EN: 'Yichang', code: 'Z9717', major: false },
    { label_ZH: '长沙', label_EN: 'Changsha', code: 'Z9731', major: false },
    { label_ZH: '邵阳', label_EN: 'Shaoyang', code: 'Z9739', major: false },
    { label_ZH: '岳阳', label_EN: 'Yueyang', code: 'Z9730', major: false },
    { label_ZH: '常德', label_EN: 'Changde', code: 'Z9736', major: false },
    { label_ZH: '永州', label_EN: 'Yongzhou', code: 'Z9746', major: false },
    { label_ZH: '怀化', label_EN: 'Huaihua', code: 'Z9745', major: false },
    { label_ZH: '广州', label_EN: 'Guangzhou', code: 'Z9200', major: true },
    { label_ZH: '韶关', label_EN: 'Shaoguan', code: 'Z9751', major: false },
    { label_ZH: '阳江', label_EN: 'Yangjiang', code: 'Z9662', major: false },
    { label_ZH: '梅州', label_EN: 'Meizhou', code: 'Z9753', major: false },
    { label_ZH: '汕头', label_EN: 'Shantou', code: 'Z9754', major: false },
    { label_ZH: '汕尾', label_EN: 'Shanwei', code: 'Z9660', major: false },
    { label_ZH: '河源', label_EN: 'Heyuan', code: 'Z9762', major: false },
    { label_ZH: '湛江', label_EN: 'Zhanjiang', code: 'Z9759', major: false },
    { label_ZH: '深圳', label_EN: 'Shenzhen', code: 'Z9755', major: true },
    { label_ZH: '南宁', label_EN: 'Naning', code: 'Z9771', major: false },
    { label_ZH: '北海', label_EN: 'Beihai', code: 'Z9779', major: false },
    { label_ZH: '柳州', label_EN: 'Liuzhou', code: 'Z9772', major: false },
    { label_ZH: '河池', label_EN: 'Hechi', code: 'Z9778', major: false },
    { label_ZH: '百色', label_EN: 'Baise', code: 'Z9776', major: false },
    { label_ZH: '梧州', label_EN: 'Wuzhou', code: 'Z9774', major: false },
    { label_ZH: '桂林', label_EN: 'Guilin', code: 'Z9773', major: false },
    { label_ZH: '海口', label_EN: 'Haikou', code: 'Z9898', major: false },
    { label_ZH: '三亚', label_EN: 'Sanya', code: 'Z9070', major: false },
    { label_ZH: '西沙', label_EN: 'Xisha', code: 'Z9071', major: false },
    { label_ZH: '成都', label_EN: 'Chengdu', code: 'Z9280', major: false },
    { label_ZH: '绵阳', label_EN: 'Mianyang', code: 'Z9816', major: false },
    { label_ZH: '乐山', label_EN: 'Leshan', code: 'Z9839', major: false },
    { label_ZH: '南充', label_EN: 'Nanchong', code: 'Z9817', major: false },
    { label_ZH: '宜宾', label_EN: 'Yibin', code: 'Z9831', major: false },
    { label_ZH: '达州', label_EN: 'Dazhou', code: 'Z9818', major: false },
    { label_ZH: '西昌', label_EN: 'Xichang', code: 'Z9834', major: false },
    { label_ZH: '黔江', label_EN: 'Qianjiang', code: 'Z9091', major: false },
    { label_ZH: '重庆', label_EN: 'Chongqin', code: 'Z9230', major: false },
    { label_ZH: '万县', label_EN: 'Wanxian', code: 'Z9090', major: false },
    { label_ZH: '遵义', label_EN: 'Zunyi', code: 'Z9852', major: false },
    { label_ZH: '兴义', label_EN: 'Xingyi', code: 'Z9859', major: false },
    { label_ZH: '毕节', label_EN: 'Bijie', code: 'Z9857', major: false },
    { label_ZH: '都匀', label_EN: 'Duyun', code: 'Z9854', major: false },
    { label_ZH: '文山', label_EN: 'Wenshan', code: 'Z9876', major: false },
    { label_ZH: '昭通', label_EN: 'Shaotong', code: 'Z9870', major: false },
    { label_ZH: '思茅', label_EN: 'Simao', code: 'Z9879', major: false },
    { label_ZH: '昆明', label_EN: 'Kunming', code: 'Z9871', major: false },
    { label_ZH: '徳宏', label_EN: 'Dehong', code: 'Z9692', major: false },
    { label_ZH: '丽江', label_EN: 'Lijiang', code: 'Z9888', major: false },
    { label_ZH: '拉萨', label_EN: 'Lasha', code: 'Z9891', major: false },
    { label_ZH: '日喀则', label_EN: 'Rikaze', code: 'Z9892', major: false },
    { label_ZH: '那曲', label_EN: 'Naqu', code: 'Z9896', major: false },
    { label_ZH: '西安', label_EN: 'Xian', code: 'Z9290', major: false },
    { label_ZH: '延安', label_EN: 'Yanan', code: 'Z9911', major: false },
    { label_ZH: '安康', label_EN: 'Ankang', code: 'Z9915', major: false },
    { label_ZH: '榆林', label_EN: 'Yulin', code: 'Z9912', major: false },
    { label_ZH: '汉中', label_EN: 'Hanzhong', code: 'Z9916', major: false },
    { label_ZH: '宝鸡', label_EN: 'Baoji', code: 'Z9917', major: false },
    { label_ZH: '兰州', label_EN: 'Lanzhou', code: 'Z9931', major: false },
    { label_ZH: '张掖', label_EN: 'Zhangye', code: 'Z9936', major: false },
    { label_ZH: '酒泉', label_EN: 'Jiuquan', code: 'Z9937', major: false },
    { label_ZH: '天水', label_EN: 'Tianshui', code: 'Z9938', major: false },
    { label_ZH: '西峰', label_EN: 'Xifeng', code: 'Z9934', major: false },
    { label_ZH: '西宁', label_EN: 'Xining', code: 'Z9971', major: false },
    { label_ZH: '海北', label_EN: 'Haibei', code: 'Z9970', major: false },
    { label_ZH: '银川', label_EN: 'Yinchuan', code: 'Z9951', major: false },
    { label_ZH: '固原', label_EN: 'Guyuan', code: 'Z9954', major: false },
    { label_ZH: '乌鲁木齐', label_EN: 'Wulumuqi', code: 'Z9991', major: false },
    { label_ZH: '阿克苏', label_EN: 'Akesu', code: 'Z9997', major: false },
    { label_ZH: '库尔勒', label_EN: 'Kuerle', code: 'Z9996', major: false },
    { label_ZH: '克拉玛依', label_EN: 'Kelamayi', code: 'Z9990', major: false },
    { label_ZH: '喀什', label_EN: 'Kashi', code: 'Z9998', major: false },
    { label_ZH: '伊宁', label_EN: 'Yining', code: 'Z9999', major: false },
    { label_ZH: '石河子', label_EN: 'Shihezi', code: 'Z9993', major: false },
    { label_ZH: '五家渠', label_EN: 'Wujiaqu', code: 'Z9081', major: false },
    { label_ZH: '奎屯', label_EN: 'Quantun', code: 'Z9080', major: false }
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

