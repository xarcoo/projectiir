<?php

require_once __DIR__ . '/vendor/autoload.php';
include_once('simple_html_dom.php');
$i = 0;
// $html = file_get_html('https://www.youtube.com/');
// foreach ($html->find('div[class="style-scope ytd-rich-item-renderer"]') as $posts) {
//     if ($i > 9) break;
//     else {
//         $text = $posts->find('a[clas="yt-simple-endpoint style-scope ytd-playlist-thumbnail"]', 0)->href;
//         echo ($text + "<br>");
//     }
//     $i++;
// }

$html = file_get_html('https://x.com/home/');
foreach ($html->find('div[class="r-18u37iz"]') as $posts) {
    echo "test";
    if ($i > 9) break;
    else {
        $text = $posts->find('span[clas="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3"]', 0)->innertext;
        echo "$text <br>";
    }
    $i++;
}

// $html = file_get_html('https://www.instagram.com/');

// $html = file_get_html('https://www.kompas.com/');
// foreach ($html->find('div[class="wSpec-item"]') as $news) {
//     if ($i > 9) break;
//     else {
//         $newsTitle = $news->find('h4[class="wSpec-title"]', 0)->innertext;
//         $newsLink = $news->find('a', 0)->href;
//         echo "$newsTitle";
//     }
//     $i++;
// }
