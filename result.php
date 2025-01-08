<?php
require_once __DIR__ . '/vendor/autoload.php';
include_once('simple_html_dom.php');

use Phpml\FeatureExtraction\TokenCountVectorizer;
use Phpml\Tokenization\WhitespaceTokenizer;
use Phpml\FeatureExtraction\TfIdfTransformer;

#Bingung coy gimana cara gabungin semua prosesnya, dari crawling->preprocessing->TF-IDF->Similarity
echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
$i = 0;
$data_crawling = array();
$sample_data = array();;

if (isset($_POST['crawl'])) {
	foreach ($_POST['source'] as $src) {
		if ($src == 'YT') {
			$html = file_get_html('https://www.youtube.com/');
			$i = 0;
			$html = new simple_html_dom();
			$html->load($result['message']);
			foreach ($html->find('div[class="style-scope ytd-rich-item-renderer"]') as $posts) {
				if ($i > 9) break;
				else {
					$text = $posts->find('a[clas="yt-simple-endpoint style-scope ytd-playlist-thumbnail"]', 0)->href;
					$sendText = str_replace(" ", "@@", $text);
					$stopText = shell_exec("python preprocess.py $sendText");

					array_push($data_crawling, array($src, $text, $stopText, 'similarity' => 0.0));
					array_push($sample_data, $stopText);
				}
				$i++;
			}
		} elseif ($src == 'X') {
			$html = file_get_html('https://x.com/');
			$i = 0;
			$html = new simple_html_dom();
			$html->load($result['message']);
			foreach ($html->find('div[class="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3"]') as $posts) {
				if ($i > 9) break;
				else {
					$text = $posts->find('span[clas="css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3"]', 0)->innertext;
					$sendText = str_replace(" ", "##", $text);
					$stopText = shell_exec("python preprocess.py $sendText");

					array_push($data_crawling, array($src, $text, $stopText, 'similarity' => 0.0));
					array_push($sample_data, $stopText);
				}
				$i++;
			}
		} elseif ($src == 'IG') {
			$html = file_get_html('https://www.instagram.com/');
			$i = 0;
			$html = new simple_html_dom();
			$html->load($result['message']);
		}
	}

	array_push($sample_data, $_POST['keyword']);

	$tf = new TokenCountVectorizer(new WhitespaceTokenizer());
	$tf->fit($sample_data);
	$tf->transform($sample_data);

	$tfidf = new TfIdfTransformer($sample_data);
	$tfidf->transform($sample_data);

	$total = count($sample_data);

	if ($_POST['method'] == 'Asymetric') {
		for ($i = 0; $i < $total - 1; $i++) {
			$numerator = 0.0;
			$denom_wkq = 0.0;
			for ($x = 0; $x < count($sample_data[$i]); $x++) {
				$numerator += min($sample_data[$total - 1][$x], $sample_data[$i][$x]);
				$denom_wkq += $sample_data[$total - 1][$x];
			}

			if ($denom_wkq != 0) {
				$result = $numerator / $denom_wkq;
			} else {
				$result = 0;
			}

			// echo "D" . ($i + 1) . " dan Q = " . round($result, 2) . "<br>";
			$data_crawling[$i]['similarity'] = $result;
		}
	} else {
		for ($i = 0; $i < $total - 1; $i++) {
			$numerator = 0.0;
			$denom_wkq = 0.0;
			$denom_wkj = 0.0;
			for ($x = 0; $x < count($sample_data[$i]); $x++) {
				$numerator += $sample_data[$total - 1][$x] * $sample_data[$i][$x];
				$denom_wkq += pow($sample_data[$total - 1][$x], 2);
				$denom_wkj += pow($sample_data[$i][$x], 2);
			}

			if (($denom_wkq * $denom_wkj) != 0) {
				$result = $numerator / min($denom_wkq, $denom_wkj);
			} else {
				$result = 0;
			}

			// echo "D" . ($i + 1) . " dan Q = " . round($result, 2) . "<br>";
			$data_crawling[$i]['similarity'] = $result;
		}
	}

	$columns = array_column($data_crawling, 'similarity');
	array_multisort($columns, SORT_DESC, $data_crawling);
	echo "<b>Search Results</b><br><br>";
	echo "<table border='1'>";
	echo "<tr>";
	echo "<th align='center'>Source</th>";
	echo "<th align='center'>Original Text</th>";
	echo "<th align='center'>Preprocessing Result</th>";
	echo "<th align='center'>Similarity</th>";
	echo "</tr>";
	foreach ($data_crawling as $row) {
		echo "<tr>";
		echo "<td>" . $row[0] . "</td>";
		echo "<td>" . $row[1] . "</td>";
		echo "<td>" . $row[2] . "</td>";
		echo "<td>" . round($row["similarity"], 5) . "</td>";
		echo "</tr>";
	}


	echo '</table>';
}
