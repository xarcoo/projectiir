<?php
session_start();

require_once __DIR__ . '/vendor/autoload.php';
include_once('simple_html_dom.php');

use Phpml\FeatureExtraction\TokenCountVectorizer;
use Phpml\Tokenization\WhitespaceTokenizer;
use Phpml\FeatureExtraction\TfIdfTransformer;

$i = 0;
$data_crawling = array();
$sample_data = array();

// $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
// $results_per_page = 5; // Jumlah hasil per halaman
// $offset = ($page - 1) * $results_per_page;

if (isset($_POST['crawl'])) {
    foreach ($_POST['source'] as $src) {
        if ($src == 'YT') {
            $keyword = escapeshellarg($_POST['keyword']);
            $maxResults = 10;
            $pythonScript = 'crawler_youtube.py';

            $command = escapeshellcmd("python $pythonScript $keyword $maxResults 2&>1");
            $output = shell_exec($command);

            $lines = explode("\n", htmlspecialchars($output));
            foreach ($lines as $line) {
                if (!empty(trim($line))) {
                    $preprocessScript = 'preprocessXYt.py';
                    $preprocessCommand = escapeshellcmd("python $preprocessScript " . escapeshellarg(str_replace(" ", "@@", $line)));
                    $preprocessedOutput = shell_exec("$preprocessCommand");

                    array_push($data_crawling, array('source' => 'YouTube', 'original' => $line, 'preprocessed' => $preprocessedOutput, 'similarity' => 0.0));
                    array_push($sample_data, $preprocessedOutput);
                }
            }
        } elseif ($src == 'X') {
            $keyword = escapeshellarg($_POST['keyword']);
            $maxResults = 10;
            $pythonScript = 'crawler_twitter.py';

            $command = escapeshellcmd("python $pythonScript $keyword $maxResults 2&>1");
            $output = shell_exec($command);

            $lines = explode("\n", htmlspecialchars($output));

            foreach ($lines as $line) {
                if (!empty(trim($line))) {
                    $preprocessScript = 'preprocessXYt.py';
                    $preprocessCommand = escapeshellcmd("python $preprocessScript " . escapeshellarg(str_replace(" ", "@@", $line)));
                    $preprocessedOutput = shell_exec("$preprocessCommand");

                    array_push($data_crawling, array('source' => 'Twitter', 'original' => $line, 'preprocessed' => $preprocessedOutput, 'similarity' => 0.0));
                    array_push($sample_data, $preprocessedOutput);
                }
            }
        } elseif ($src == 'IG') {
            $keyword = escapeshellarg($_POST['keyword']);
            $pythonScript = 'insta_crawler.py';
        
            // Jalankan skrip Python untuk mengcrawl data Instagram
            $command = escapeshellcmd("python $pythonScript 2>&1");
            $output = shell_exec($command);
        
            // Pisahkan output menjadi baris-baris
            $lines = explode("\n", htmlspecialchars($output));
        
            // Variabel untuk menghindari duplikasi
            $dupe = null;
        
            foreach ($lines as $line) {
                // Periksa apakah ini adalah duplikat dari sebelumnya
                if ($line === $dupe) {
                    continue; // Lewati baris jika duplikat
                }
        
                // Set baris saat ini sebagai duplikat untuk iterasi berikutnya
                $dupe = $line;
        
                // Proses hanya jika baris tidak kosong
                if (!empty(trim($line))) {
                    $preprocessScript = 'preprocess.py';
        
                    // Gunakan file sementara untuk menyimpan data besar
                    $temp_file = tempnam(sys_get_temp_dir(), 'data_');
                    file_put_contents($temp_file,  $line);
        
                    // Buat perintah Python dengan file sementara
                    $preprocessCommand = escapeshellcmd("python $preprocessScript " . escapeshellarg($temp_file));
                    $preprocessedOutput = shell_exec($preprocessCommand);
        
                    // Hapus file sementara setelah selesai
                    unlink($temp_file);
        
                    // Tambahkan hasil ke array data_crawling
                    array_push($data_crawling, array('source' => 'Instagram', 'original' => $line, 'preprocessed' => $preprocessedOutput, 'similarity' => 0.0));
                    array_push($sample_data, $preprocessedOutput);
                }
            }
        }
        
        // elseif ($src == 'IG') {
        //     $keyword = escapeshellarg($_POST['keyword']);
        //     $pythonScript = 'insta_crawler.py';

        //     $command = escapeshellcmd("python $pythonScript 2&>1");
        //     $output = shell_exec($command);

        //     $lines = explode("\n", htmlspecialchars($output));

        //     foreach ($lines as $line) {
        //         if (isset($dupe)) {
        //             if ($line == $dupe) {
        //                 $dupe = $line;
        //             } else {
        //                 if (!empty(trim($line))) {
        //                     $preprocessScript = 'preprocess.py';
        //                     $preprocessCommand = escapeshellcmd("python $preprocessScript " . escapeshellarg(str_replace(" ", "@@", $line)));
        //                     $preprocessedOutput = shell_exec("$preprocessCommand");

        //                     array_push($data_crawling, array('source' => 'Instagram', 'original' => $line, 'preprocessed' => $preprocessedOutput, 'similarity' => 0.0));
        //                     array_push($sample_data, $preprocessedOutput);
        //                 }
        //             }
        //         } else {
        //             if (!empty(trim($line))) {
        //                 $preprocessScript = 'preprocess.py';
        //                 $preprocessCommand = escapeshellcmd("python $preprocessScript " . escapeshellarg(str_replace(" ", "@@", $line)));
        //                 $preprocessedOutput = shell_exec("$preprocessCommand");

        //                 array_push($data_crawling, array('source' => 'Instagram', 'original' => $line, 'preprocessed' => $preprocessedOutput, 'similarity' => 0.0));
        //                 array_push($sample_data, $preprocessedOutput);
        //             }
        //         }
        //     }
        // }
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

            $data_crawling[$i]['similarity'] = $result;
        }
        // $_SESSION['data_crawling'] = $data_crawling;
    }
    // if (isset($_SESSION['data_crawling'])) {
    //     $data_crawling = $_SESSION['data_crawling'];
    //     $total_results = count($data_crawling);
    //     $paged_results = array_slice($data_crawling, $offset, $results_per_page); // Ambil hasil untuk halaman ini

    //     // Tampilkan hasil paging
    //     if (!empty($paged_results)) {
    //         foreach ($paged_results as $row) {
    //             echo "<b><u>Source:</u></b> " . $row['source'] . "<br>";
    //             echo "<b><u>Original Text:</u></b><br>" . $row['original'] . "<br>";
    //             echo "<b><u>Preprocessing Result:</u></b><br>" . $row['preprocessed'] . "<br>";
    //             echo "<b><u>Similarity:</u></b> " . round($row["similarity"], 5);
    //             echo "<hr>";
    //         }
    //     } else {
    //         echo "No results to display.";
    //     }

    //     // Tampilkan navigasi paging
    //     $total_pages = ceil($total_results / $results_per_page);

    //     echo '<div style="text-align:center;">';
    //     if ($page > 1) {
    //         echo '<a href="?page=' . ($page - 1) . '">Previous</a> ';
    //     }
    //     for ($i = 1; $i <= $total_pages; $i++) {
    //         if ($i == $page) {
    //             echo '<strong>' . $i . '</strong> ';
    //         } else {
    //             echo '<a href="?page=' . $i . '">' . $i . '</a> ';
    //         }
    //     }
    //     if ($page < $total_pages) {
    //         echo '<a href="?page=' . ($page + 1) . '">Next</a>';
    //     }
    //     echo '</div>';
    // }
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project IIR - Search</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f0f4f8;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        .container {
            margin-top: 50px;
            max-width: 1000px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
        }

        .header h1 {
            color: #007bff;
            font-size: 2.5rem;
        }

        .header p {
            color: #6c757d;
            font-size: 1.2rem;
        }

        .form-label {
            font-weight: bold;
            color: #343a40;
        }

        .center-placeholder {
            text-align: center;
        }

        .center-placeholder::placeholder {
            text-align: center;
        }

        .aligntextcenter {
            text-align: center;
        }

        .method {
            justify-items: center;
        }

        .btn-primary {
            background-color: #007bff;
            border: none;
            transition: background-color 0.3s;
        }

        .btn-primary:hover {
            background-color: #0056b3;
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            border: 1px solid #007bff;
            border-radius: 5px;
            background-color: #e9f7ff;
        }

        .result p {
            text-align: center;
        }

        .similarity {
            font-weight: bold;
            color: #28a745;
        }

        .footer {
            text-align: center;
            padding-top: 20px;
            color: #6c757d;
        }
    </style>
</head>

<body>
    <div class="container">
        <div class="header">
            <h1>PROJECT IIR</h1>
            <p class="text-muted">KEPO.COM</p>
        </div>

        <form action="index.php" method="POST" class="p-4 border rounded bg-white shadow">
            <div class="mb-3 aligntextcenter">
                <label for="keyword" class="form-label">Keyword</label>
                <input type="text" class="form-control center-placeholder" id="keyword" name="keyword" placeholder="Enter your keyword" required>
            </div>

            <div class="mb-3 aligntextcenter">
                <label class="form-label">Source</label><br>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="checkbox" name="source[]" id="sourceX" value="X">
                    <label class="form-check-label" for="sourceX">X</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="checkbox" name="source[]" id="sourceIG" value="IG">
                    <label class="form-check-label" for="sourceIG">Instagram</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="checkbox" name="source[]" id="sourceYT" value="YT">
                    <label class="form-check-label" for="sourceYT">YouTube</label>
                </div>
            </div>

            <div class="mb-3 method">
                <label class="form-label">Similarity Method</label><br>
                <div class="radio">
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="method" id="methodAsym" value="Asymetric">
                        <label class="form-check-label" for="methodAsym">Asymmetric</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="method" id="methodOverlap" value="Overlap">
                        <label class="form-check-label" for="methodOverlap">Overlap</label>
                    </div>
                </div>
            </div>

            <button type="submit" name="crawl" class="btn btn-primary w-100">Search</button>
        </form>

        <div class="result">
            <?php
            echo "<hr>";
            if (!empty($data_crawling)) {
                $columns = array_column($data_crawling, 'similarity');
                array_multisort($columns, SORT_DESC, $data_crawling);
                foreach ($data_crawling as $row) {
                    echo "<b><u>Source:</u></b> " . $row['source'] . "<br>";
                    echo "<b><u>Original Text:</u></b><br>" . $row['original'] . "<br>";
                    echo "<b><u>Preprocessing Result:</u></b><br>" . $row['preprocessed'] . "<br>";
                    echo "<b><u>Similarity:</u></b> " . round($row["similarity"], 5);
                    echo "<hr>";
                }
            } else {
                echo '<p>No data found (Please search for a keyword)</p>';
                echo "<hr>";
            }
            ?>
        </div>
    </div>

    <div class="footer">
        <p>Kelompok 2</p>
        <p>160421048 - Satya Aryaputra Wigiyanto</p>
        <p>160421050 - Archie Euaggelion Oematan</p>
        <p>160421078 - Vinsent Farrel Eka Setyawan</p>
        <p>160421125 - Timothy Dewanto Suwarno</p>
        <p>160421144 - Theodorus Riady Hoesin</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>