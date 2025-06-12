var createFlagChecker = _ => {};
createFlagChecker = () => {
  var MI4MI4YI1 = 123;
  var MI4MI4ER4 = 45;
  var MI4MI4SAN1 = 67;
  var MI4MI4SI4 = 89;
  var checkFlag = _ => {};
  checkFlag = flag => {
    var checksum = 1337;
    var i = 0;
    while (true) {
      const _ans1 = flag.length;
      var JI3XIN1 = false;
      if (i < _ans1) {
        JI3XIN1 = true;
      };
      if (JI3XIN1 == 0) {
        break;
      };
      var ZI3CHEN2 = _ => {};
      ZI3CHEN2 = _a0 => {
        return flag.charCodeAt(_a0, );
      };
      const _ans2 = ZI3CHEN2(i);
      var ZI4YUAN2DAI4MA3 = _ans2;
      const _ans3 = i % 4;
      var XU1SHI2 = _ans3;
      if (XU1SHI2 == 0) {
        const _ans4 = ZI4YUAN2DAI4MA3 * 7;
        var ZI3CHEN2BA1 = _ans4;
        const _ans5 = ZI3CHEN2BA1 + 3;
        var HAI4WU4 = _ans5;
        const _ans6 = HAI4WU4 % 256;
        ZI4YUAN2DAI4MA3 = _ans6;
      };
      const _ans7 = i % 4;
      var SI4WU3 = _ans7;
      if (SI4WU3 == 1) {
        const _ans8 = ZI4YUAN2DAI4MA3 * 3;
        var REN2CHEN2 = _ans8;
        const _ans9 = REN2CHEN2 + 5;
        var JI3WU3 = _ans9;
        const _ans10 = JI3WU3 % 256;
        ZI4YUAN2DAI4MA3 = _ans10;
      };
      const _ans11 = i % 4;
      var ER4CHEN2 = _ans11;
      if (ER4CHEN2 == 2) {
        const _ans12 = ZI4YUAN2DAI4MA3 * 11;
        var ER4SHEN1 = _ans12;
        const _ans13 = ER4SHEN1 - 7;
        var WU4JIA3 = _ans13;
        const _ans14 = WU4JIA3 % 256;
        ZI4YUAN2DAI4MA3 = _ans14;
      };
      const _ans15 = i % 4;
      var YI3WU3 = _ans15;
      if (YI3WU3 == 3) {
        const _ans16 = ZI4YUAN2DAI4MA3 * 5;
        var GENG1YIN2 = _ans16;
        const _ans17 = GENG1YIN2 + 9;
        var ZHI1GENG1 = _ans17;
        const _ans18 = ZHI1GENG1 % 256;
        ZI4YUAN2DAI4MA3 = _ans18;
      };
      const _ans19 = i % 4;
      var CHEN2CHEN2 = _ans19;
      if (CHEN2CHEN2 == 0) {
        const _ans20 = ZI4YUAN2DAI4MA3 + MI4MI4YI1;
        var XU1WEI4 = _ans20;
        const _ans21 = XU1WEI4 % 256;
        ZI4YUAN2DAI4MA3 = _ans21;
      };
      const _ans22 = i % 4;
      var JI3YI3 = _ans22;
      if (JI3YI3 == 1) {
        const _ans23 = ZI4YUAN2DAI4MA3 + MI4MI4ER4;
        var BING3YI3 = _ans23;
        const _ans24 = BING3YI3 % 256;
        ZI4YUAN2DAI4MA3 = _ans24;
      };
      const _ans25 = i % 4;
      var YI3GENG1 = _ans25;
      if (YI3GENG1 == 2) {
        const _ans26 = ZI4YUAN2DAI4MA3 + MI4MI4SAN1;
        var CHOU3JIA3 = _ans26;
        const _ans27 = CHOU3JIA3 % 256;
        ZI4YUAN2DAI4MA3 = _ans27;
      };
      const _ans28 = i % 4;
      var GENG1MAO3 = _ans28;
      if (GENG1MAO3 == 3) {
        const _ans29 = ZI4YUAN2DAI4MA3 + MI4MI4SI4;
        var SI4XIN1 = _ans29;
        const _ans30 = SI4XIN1 % 256;
        ZI4YUAN2DAI4MA3 = _ans30;
      };
      const _ans31 = checksum * 31;
      var DI4WEI4 = _ans31;
      const _ans32 = DI4WEI4 + ZI4YUAN2DAI4MA3;
      var SI4REN2 = _ans32;
      const _ans33 = SI4REN2 % 65521;
      checksum = _ans33;
      const _ans34 = i + 1;
      i = _ans34;
    };
    var _ans35 = 63740;
    var REN2YIN2 = false;
    if (checksum == _ans35) {
      REN2YIN2 = true;
    };
    return REN2YIN2;
  };
  return checkFlag;
};
const _ans36 = createFlagChecker();
var verifyFlag = _ans36;
const _ans37 = verifyFlag("bcactf{FAKE_FLAG}");
var result = _ans37;
var _ans38 = "Flag check result:";
var _ans39 = result;
console.log(_ans38, _ans39);