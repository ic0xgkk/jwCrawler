CREATE DATABASE jwData;

USE jwData;


CREATE TABLE course(
  jx0404id VARCHAR(64) NOT NULL , -- ti jiao id
  xf TINYINT  , -- xue fen
  dwmc VARCHAR(64)  , -- kai ke xue yuan
  jx02id VARCHAR(128)  , -- ke cheng hao
  xkrs INT  , -- xuan ke ren shu
  zxs INT  ,  -- zong xue shi
  sksj VARCHAR(512) , -- shang ke shi jian
  xxrs INT ,  --  ke cheng rong liang
  szkcflmc VARCHAR(32) , -- lei bie
  syrs INT , -- sheng yu ren shu
  kcmc VARCHAR(64), -- ke cheng ming
  skls VARCHAR(256) , -- shang ke lao shi
  skdd VARCHAR(512), -- shang ke di dian
  kindName VARCHAR(16), -- lei xing ming cheng
  classKind VARCHAR(32), -- ke cheng lei xing
  insertedTime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(jx0404id, kindName, classKind)
);

