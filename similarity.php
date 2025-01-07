<?php
require_once __DIR__ . '/vendor/autoload.php';

//import class class TF-Raw
use Phpml\FeatureExtraction\TokenCountVectorizer;
use Phpml\Tokenization\WhitespaceTokenizer;

//import class untuk menghitung TF-IDF
use Phpml\FeatureExtraction\TfIdfTransformer;
$tf = new TokenCountVectorizer(new WhitespaceTokenizer());
$tf->fit($sample_data);
$tf->transform($sample_data);

$tfidf = new TfIdfTransformer($sample_data);
$tfidf->transform($sample_data);

$total = count($sample_data);
echo "<br><b><u>Asymmetric</u></b><br>";
for($i=0;$i<$total-1;$i++){
    $numerator = 0.0;
    $denom_wkq = 0.0;
    for($x=0;$x<count($sample_data[$i]);$x++){
        $numerator += min($sample_data[$total-1][$x], $sample_data[$i][$x]);
        $denom_wkq += $sample_data[$total-1][$x];
    }
    if(($denom_wkq) != 0){
        $result = $numerator / $denom_wkq;
    }
    else $result = 0;

    echo "
    D".($i+1)." dan Q = ".round($result,2)."<br>";
}
echo "<br><b><u>Overlap</u></b><br>";
for($i=0;$i<$total-1;$i++){
    $numerator = 0.0;
    $denom_wkq = 0.0;
    $denom_wkj = 0.0;
    for($x=0;$x<count($sample_data[$i]);$x++){
        $numerator += $sample_data[$total-1][$x] * $sample_data[$i][$x];
        $denom_wkq += pow($sample_data[$total-1][$x],2);
        $denom_wkj += pow($sample_data[$i][$x],2);
    }
    if(($denom_wkq+$denom_wkj) != 0){
        $result = $numerator / min($denom_wkq,$denom_wkj);
    }
    else $result = 0;

    echo "D".($i+1)." dan Q = ".round($result,2)."<br>";
}
?>