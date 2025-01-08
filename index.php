<?php
require_once __DIR__ . '/vendor/autoload.php';
include_once('simple_html_dom.php');

use Phpml\FeatureExtraction\TokenCountVectorizer;
use Phpml\Tokenization\WhitespaceTokenizer;
use Phpml\FeatureExtraction\TfIdfTransformer;

echo "PROJECT IIR <br>";
echo "KEPO.COM";
echo '<form action="index.php" method="POST">';
echo '<b>Keyword :</b> <input type="text" name="keyword"><br><br>';
echo '<b>Source :</b> ';
echo '<input type="checkbox" name="source[]" value="X" checked/>X ';
echo '<input type="checkbox" name="source[]" value="IG"/>Instagram';
echo '<input type="checkbox" name="source[]" value="YT"/>Youtube<br>';
echo '<b>Similarity Method :</b> ';
echo '<input type="radio" name="method" value="Asymetric" checked/>Asymetric ';
echo '<input type="radio" name="method" value="Overlap"/>Overlap<br><br>';
echo '<input type="submit" name="crawl" value="Search"> ';
echo '</form>';

$proxy = '';

echo "<b><a href='index.php'>< Back to Home</a></b><br><br>";
$i = 0;
$data_crawling = array();
$sample_data = array();

if (isset($_POST['crawl'])) {
    foreach ($_POST['source'] as $src) {
        if ($src == 'YT') {
            $keyword = escapeshellarg($_POST['keyword']);
            $maxResults = 10; // Batasi jumlah hasil YouTube jika tidak diatur
            $pythonScript = 'crawler_youtube.py';
            
            // Perintah untuk menjalankan Python
            $command = escapeshellcmd("python $pythonScript $keyword $maxResults");
            $output = shell_exec($command);

            echo "<h2>Hasil dari Python (YouTube):</h2>";
            echo "<div style='font-family: Arial, sans-serif; line-height: 1.6;'>";

            $lines = explode("\n", htmlspecialchars($output));
            foreach ($lines as $line) {
                if (!empty(trim($line))) {
                    // Preprocessing menggunakan preprocess.py
                    $preprocessScript = 'preprocess.py';
                    $preprocessCommand = escapeshellcmd("python $preprocessScript " . escapeshellarg(str_replace(" ", "@@", $line)));
                    $preprocessedOutput = shell_exec($preprocessCommand);

                    // Tampilkan hasil awal dan hasil preprocessing
                    echo "<div style='margin-bottom: 10px;'><b>Original:</b> $line</div>";
                    echo "<div style='margin-bottom: 10px;'><b>Preprocessed:</b> $preprocessedOutput</div>";
                    array_push($data_crawling, array('source' => 'YouTube', 'original' => $line, 'preprocessed' => $preprocessedOutput));
                }
            }
            echo "</div>";
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
    foreach ($data_crawling as $row) {
        echo "<b><u>Source:</u></b> " . $row[0] . "<br>";
        echo "<b><u>Original Text:</u></b><br>" . $row[1] . "<br>";
        echo "<b><u>Preprocessing Result:</u></b><br>" . $row[2] . "<br>";
        echo "<b><u>Similarity:</u></b> " . $row["similarity"];
        echo "<hr>";
    }
}
