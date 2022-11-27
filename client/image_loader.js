var db_img;
var missing_load = 10000;

var load_db = function () {
  db_img = {};
  missing_load = images.length;
  for (const elem of images) {
    img_name = elem.split("/").slice(-1)[0].split(".")[0];

    var tmp_img = new Image();
    tmp_img.onload = function () {
      missing_load--;
    };
    tmp_img.src = elem;
    db_img[img_name] = tmp_img;
  }
};

const interval = setInterval(function () {
  if (missing_load != 0) {
    console.log("Missing " + missing_load + " img to load;");
  }
}, 1000);

load_db();
