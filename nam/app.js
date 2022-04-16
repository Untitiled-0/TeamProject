// const res = require("express/lib/response");
// const http = require("http");
// const app = http.createServer((req,res) => {
//     res.writeHead(200, { "content-Type": "text/html; charset=utf-8"});
//     if(req.url === "/") { res.end("여기는 루트입니다."); }
//     else if(req.url === "/login") { res.end("여기는 로그인입니다."); }
// });

// app.listen(3001, () => {
//     console.log("http로 가동된 서버입니다.");
// });
"use strict";

const express = require("express");
const app = express();

const port = 3000;

//라우터
const home = require("./routes/home");

//어플 셋팅
app.set("views", "./views");
app.set("view engine", "ejs");

app.use("/", home); // use -> 미들 웨어를 등록해주는 메서드