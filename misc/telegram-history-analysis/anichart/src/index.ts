import * as ANI from "anichart";

const stage = new ANI.Stage();
stage.options.fps = 60;
stage.options.sec = 40;

const userid: {[id: string]: string} = {
  'user1868166081': '桂',
}

// Bar chart
ANI.recourse.loadCSV("./output.csv", "data");
let bar = new ANI.BarChart({
  dateLabelOptions: {},
});

// Disable name display
bar.barInfoFormat = (id, meta, data) => ''
bar.showRankLabel = false
console.log(bar.data);


// Avatars
for (let key in userid) {
  let user = userid[key]
  ANI.recourse.loadImage(`./avatar/${user}.jpg`, user);
}

stage.canvas.width = 1920;
stage.canvas.height = 1080;
const rect = new ANI.Rect({
  shape: { width: 1920, height: 1080 },
  fillStyle: "#1e1e1e",
});
stage.addChild(rect);
stage.addChild(bar);

const center = new ANI.Text({ text: "uwu", font: 'Microsoft Yahei UI' })
center.fontSize = 90
stage.addChild(center);

stage.play();
stage.output = true;

// new ANI.MapChart({});
