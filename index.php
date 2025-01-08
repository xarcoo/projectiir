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
