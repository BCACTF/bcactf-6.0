var JIAN4LI4JIAN3CHA2QI4 = _ => {};
JIAN4LI4JIAN3CHA2QI4 = () => {
  var GUAN1JIAN4YI1 = 11;
  var GUAN1JIAN4ER4 = 22;
  var GUAN1JIAN4SAN1 = 33;
  var GUAN1JIAN4SI4 = 44;
  var ef = [];
  ef.push(109, 121, 130, 143, 127, 124, 156, 153, 132, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 84, 96, 66, 117, 87, 158, 62, 74, 88, 139, 65, 136, 85, 154, 111, 124, 85, 99, 115, 73, 147, 139, 123, 136, 81, 98, 125, 74, 142, 153, 62, 122, 128, 99, 115, 71, 86, 169);
  var BIAN1MA3BIAO1ZHI4 = _ => {};
  BIAN1MA3BIAO1ZHI4 = f => {
    var JIE2GUO3 = [];
    var i = 0;
    while (true) {
      const _ans1 = f.length;
      var CHEN2DING1 = false;
      if (i < _ans1) {
        CHEN2DING1 = true;
      };
      if (CHEN2DING1 == 0) {
        break;
      };
      var JIA3SHI2 = _ => {};
      JIA3SHI2 = _a0 => {
        return f.charCodeAt(_a0, );
      };
      const _ans2 = JIA3SHI2(i);
      var ZI4YUAN2DAI4MA3 = _ans2;
      var e = {};
      const _ans3 = i % 4;
      var XIN1SI4 = _ans3;
      if (XIN1SI4 == 0) {
        const _ans4 = ZI4YUAN2DAI4MA3 + GUAN1JIAN4YI1;
        var JI3GENG1 = _ans4;
        const _ans5 = JI3GENG1 % 256;
        e = _ans5;
      } else {
        const _ans6 = i % 4;
        var DI4SHI2 = _ans6;
        if (DI4SHI2 == 1) {
          const _ans7 = ZI4YUAN2DAI4MA3 + GUAN1JIAN4ER4;
          var CHEN2GUI3 = _ans7;
          const _ans8 = CHEN2GUI3 % 256;
          e = _ans8;
        } else {
          const _ans9 = i % 4;
          var YIN2WU3 = _ans9;
          if (YIN2WU3 == 2) {
            const _ans10 = ZI4YUAN2DAI4MA3 + GUAN1JIAN4SAN1;
            var GENG1BING3 = _ans10;
            const _ans11 = GENG1BING3 % 256;
            e = _ans11;
          } else {
            const _ans12 = ZI4YUAN2DAI4MA3 + GUAN1JIAN4SI4;
            var ZI3XU1 = _ans12;
            const _ans13 = ZI3XU1 % 256;
            e = _ans13;
          };
        };
      };
      JIE2GUO3.push(e);
      const _ans14 = i + 1;
      i = _ans14;
    };
    return JIE2GUO3;
  };
  var JIAN3CHA2BIAO1ZHI4 = _ => {};
  JIAN3CHA2BIAO1ZHI4 = f => {
    const _ans15 = BIAN1MA3BIAO1ZHI4(f);
    e = _ans15;
    var YIN2YIN2 = _ => {};
    YIN2YIN2 = () => {
      return e.toString();
    };
    const _ans16 = YIN2YIN2();
    var WU4YI3 = _ans16;
    var MAO3WEI4 = _ => {};
    MAO3WEI4 = () => {
      return ef.toString();
    };
    const _ans17 = MAO3WEI4();
    var WEI4ER4 = false;
    if (WU4YI3 == _ans17) {
      WEI4ER4 = true;
    };
    return WEI4ER4;
  };
  return JIAN3CHA2BIAO1ZHI4;
};
const _ans18 = JIAN4LI4JIAN3CHA2QI4();
var BIAO1ZHI4JIAN3CHA2QI4 = _ans18;
const _ans19 = BIAO1ZHI4JIAN3CHA2QI4("bcactf{FAKE_FLAG}");
JIE2GUO3 = _ans19;
var _ans20 = "標誌檢查結果:";
var _ans21 = JIE2GUO3;
console.log(_ans20, _ans21);