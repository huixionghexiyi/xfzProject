var gulp = require("gulp");
var cssnano = require("gulp-cssnano");
var rename = require("gulp-rename");
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
// var cache = require('gulp-cache');
var imagemin = require("gulp-imagemin");
var bs = require("browser-sync").create();
var sass = require("gulp-sass");
var util = require("gulp-util");
//解决如果js出错，在浏览器中查看js错误调试时，js会经过压缩后的。该插件可以找到原始的js文件
var sourcemaps = require("gulp-sourcemaps");
var path = {
    'html': './templates/**/',//templates下的任意目录下的html
    'css': './src/css/**/',
    'js': './src/js/',
    'img': './src/img/',
    'css_dist': './dist/css/',
    'js_dist': './dist/js/',
    'img_dist': './dist/img/',
}

// //处理html
gulp.task("html", function () {
    gulp.src(path.html + "*.html")
        .pipe(bs.stream())
})

// 压缩css的任务
gulp.task("css", function () {
    gulp.src(path.css + "*.scss")
        .pipe(sass().on("error", sass.logError))//将scss转成css
        .pipe(cssnano())//压缩
        .pipe(rename({ "suffix": ".min" }))//重命名
        .pipe(gulp.dest(path.css_dist))//存储
        .pipe(bs.stream())//重新写入流中
});
//处理js文件的任务
gulp.task("js", function () {
    gulp.src(path.js + "*.js")
        .pipe(sourcemaps.init())//显示js源文件，而不是压缩后的
        .pipe(uglify().on("error", util.log))//丑化，也就是压缩
        .pipe(rename({ "suffix": ".min" }))//重命名
        .pipe(gulp.dest(path.js_dist))//存到dist/js下
        .pipe(bs.stream())
});

//处理img文件的任务
gulp.task("img", function () {
    gulp.src(path.img + "*.*")
        .pipe(cache(imagemin()))//压缩图片
        .pipe(gulp.dest(path.img_dist))//存储
        .pipe(bs.stream())
});

//定义监听文件修改的任务
gulp.task("watch", function () {
    gulp.watch(path.html + "*.html", ['html']);
    gulp.watch(path.css + "*.scss", ['css']);
    gulp.watch(path.js + "*.js", ['js']);
    gulp.watch(path.img + "*.*", ['img']);
});

//初始化browser-sync的任务
gulp.task("bs", function () {
    bs.init({
        'server': {
            'baseDir': './'
        }
    })
});

//创建一个默认任务,创建服务器，监听修改
//任务名为default，就可以直接用gulp，而不用使用gulp [任务名]
gulp.task("default", ['bs', 'watch']);
